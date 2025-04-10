from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    currency = Column(String, default="SUI")
    location = Column(String, index=True)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area = Column(Float)  # in square meters
    property_type = Column(String, index=True)  # house, apartment, land, etc.
    
    # Blockchain related
    token_id = Column(String, unique=True, index=True)  # NFT token ID
    owner_address = Column(String, index=True)
    is_listed = Column(Boolean, default=False)
    
    # Media
    images = Column(JSON)  # List of IPFS hashes
    documents = Column(JSON)  # List of IPFS hashes for property documents
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="properties") 