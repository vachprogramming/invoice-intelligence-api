from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Core Data
    filename = Column(String, nullable=False)
    extraction_date = Column(DateTime(timezone=True), server_default=func.now())

    # Extracted Fields (Matches the Pydantic Schema)
    invoice_number = Column(String, nullable=True)
    vendor_name = Column(String, nullable=True)
    invoice_date = Column(Date, nullable=True)
    
    # Financials (Use Numeric for money, never Float)
    total_gross = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="EUR")
    
    # German Specifics
    iban = Column(String, nullable=True)