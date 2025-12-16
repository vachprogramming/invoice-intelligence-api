from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import date
from typing import Optional

# Base schema (shared properties)
class InvoiceBase(BaseModel):
    filename: str
    vendor_name: Optional[str] = Field(None, description="Company issuing the invoice")
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    total_gross: Optional[Decimal] = Field(None, description="Total amount to pay")
    currency: str = Field("EUR", max_length=3)
    iban: Optional[str] = None

    # Validator: Clean up the currency
    @field_validator('currency')
    @classmethod
    def normalize_currency(cls, v: str):
        if v.strip() in ["€", "Euro", "euro"]:
            return "EUR"
        return v.upper()

# Schema for CREATING an invoice (Input)
class InvoiceCreate(InvoiceBase):
    pass

# Schema for READING an invoice (Output)
# This adds the ID and CreatedAt, which the DB generates, not the user
class InvoiceResponse(InvoiceBase):
    id: int
    
    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models