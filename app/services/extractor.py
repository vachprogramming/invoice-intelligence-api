import json
import io
import os
import re
from pypdf import PdfReader
from huggingface_hub import InferenceClient
from app.schemas.invoice import InvoiceCreate
from dotenv import load_dotenv

# Forcing load env variables to be safe
load_dotenv()

class InvoiceExtractor:
    def __init__(self):
        # We use Llama-3.2-3B-Instruct because it supports chat_completion on HuggingFace
        token = os.getenv("HUGGINGFACE_API_KEY")
        if not token:
            raise ValueError("HUGGINGFACE_API_KEY is missing in .env")
            
        self.client = InferenceClient(
            model="meta-llama/Llama-3.2-3B-Instruct",
            token=token
        )

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Reads text from a Digital PDF.
        Limitation: Cannot read scanned images (requires OCR tools like Tesseract).
        """
        try:
            pdf = PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text[:3000] # Limit text size to avoid token limits
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""

    def _clean_json_string(self, raw_response: str) -> str:
        """
        LLMs like to chat. We need to cut out just the JSON part.
        Example: "Here is your data: ```json {...} ```" -> "{...}"
        """
        # Looking for content inside ```json ... ``` or just ``` ... ```
        if "```" in raw_response:
            # Use Regex to find the code block
            match = re.search(r"```(?:json)?(.*?)```", raw_response, re.DOTALL)
            if match:
                return match.group(1).strip()
        return raw_response.strip()

    def extract(self, file_content: bytes, filename: str) -> InvoiceCreate:
        # 1. Read the text
        text = self._extract_text_from_pdf(file_content)
        
        if not text.strip():
            print("Warning: PDF had no text (Might be an image scan).")
            return InvoiceCreate(
                filename=filename,
                vendor_name="SCAN_DETECTED_FAILED",
                total_gross=0,
                currency="EUR"
            )

        # 2. The Prompt (Instructions for the AI)
        system_message = """You are an expert data extractor. 
Extract these fields from invoice text into a valid JSON object:
- vendor_name (String)
- invoice_number (String)
- invoice_date (YYYY-MM-DD)
- total_gross (Number)
- currency (String, e.g. EUR)
- iban (String)

Rules:
1. Return ONLY JSON. No explanation.
2. If a field is missing, use null.
3. Convert date to YYYY-MM-DD format."""

        user_message = f"Extract data from this invoice:\n\n{text}"

        print("Sending request to AI...")
        
        try:
            # 3. Calling the API using chat_completion (HuggingFace updated API)
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.1  # Low temperature = strict facts
            )
            
            # 4. Parsing the result
            raw_response = response.choices[0].message.content
            json_str = self._clean_json_string(raw_response)
            data = json.loads(json_str)

            # 5. Returning validated object
            return InvoiceCreate(
                filename=filename,
                vendor_name=data.get("vendor_name"),
                invoice_number=data.get("invoice_number"),
                invoice_date=data.get("invoice_date"),
                total_gross=data.get("total_gross"),
                currency=data.get("currency", "EUR"),
                iban=data.get("iban")
            )

        except Exception as e:
            print(f"AI Extraction Failed: {e}")
            # Failing gracefully so the server doesn't crash
            return InvoiceCreate(
                filename=filename,
                vendor_name="AI_ERROR", 
                total_gross=0, 
                currency="EUR"
            )

extractor = InvoiceExtractor()