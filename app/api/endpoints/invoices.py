from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.extractor import extractor
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceResponse

router = APIRouter()

@router.post("/upload", response_model=InvoiceResponse)
async def upload_invoice(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db)
):
    """
    1. Read the uploaded file.
    2. Send it to the Extractor Service.
    3. Save the result to PostgreSQL.
    """
    # 1. Reading file content
    content = await file.read()
    
    # 2. Extracting Data (The AI part)
    data = extractor.extract(content, file.filename)
    
    # 3. Save to DB (The Engineering part)
    # We convert the Pydantic model (data) into a SQLAlchemy model (db_invoice)
    db_invoice = Invoice(
        filename=data.filename,
        invoice_number=data.invoice_number,
        vendor_name=data.vendor_name,
        invoice_date=data.invoice_date,
        total_gross=data.total_gross,
        currency=data.currency,
        iban=data.iban
    )
    
    db.add(db_invoice)
    await db.commit()
    await db.refresh(db_invoice) # Get the ID back from the DB
    
    return db_invoice