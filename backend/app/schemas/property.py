from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    currency: str = "SUI"
    location: str
    bedrooms: int
    bathrooms: int
    area: float
    property_type: str
    images: List[str] = []
    documents: List[str] = []

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    location: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[float] = None
    property_type: Optional[str] = None
    images: Optional[List[str]] = None
    documents: Optional[List[str]] = None

class PropertyInDB(PropertyBase):
    id: int
    token_id: Optional[str]
    owner_address: str
    is_listed: bool
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int

    class Config:
        from_attributes = True

class Property(PropertyInDB):
    pass

class PropertySearch(BaseModel):
    query: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    location: Optional[str] = None
    is_listed: Optional[bool] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100) 