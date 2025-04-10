from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.db.session import get_db
from app.models.property import Property
from app.models.user import User
from app.schemas.property import (
    Property as PropertySchema,
    PropertyCreate,
    PropertyUpdate,
    PropertySearch
)
from app.api.v1.endpoints.auth import get_current_user
from app.utils.ipfs import upload_to_ipfs
from app.utils.sui import get_object

router = APIRouter()

@router.post("/", response_model=PropertySchema)
async def create_property(
    *,
    db: Session = Depends(get_db),
    property_in: PropertyCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new property listing"""
    db_property = Property(
        **property_in.dict(),
        owner_id=current_user.id,
        owner_address=current_user.sui_address
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.get("/", response_model=List[PropertySchema])
async def search_properties(
    search: PropertySearch = Depends(),
    db: Session = Depends(get_db)
):
    """Search for properties with filters"""
    query = db.query(Property)
    
    # Apply filters
    if search.query:
        query = query.filter(
            or_(
                Property.title.ilike(f"%{search.query}%"),
                Property.description.ilike(f"%{search.query}%"),
                Property.location.ilike(f"%{search.query}%")
            )
        )
    
    if search.min_price is not None:
        query = query.filter(Property.price >= search.min_price)
    if search.max_price is not None:
        query = query.filter(Property.price <= search.max_price)
    if search.property_type:
        query = query.filter(Property.property_type == search.property_type)
    if search.bedrooms:
        query = query.filter(Property.bedrooms == search.bedrooms)
    if search.bathrooms:
        query = query.filter(Property.bathrooms == search.bathrooms)
    if search.min_area is not None:
        query = query.filter(Property.area >= search.min_area)
    if search.max_area is not None:
        query = query.filter(Property.area <= search.max_area)
    if search.location:
        query = query.filter(Property.location.ilike(f"%{search.location}%"))
    if search.is_listed is not None:
        query = query.filter(Property.is_listed == search.is_listed)
    
    # Apply sorting
    if search.sort_by:
        sort_column = getattr(Property, search.sort_by)
        if search.sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    # Apply pagination
    skip = (search.page - 1) * search.limit
    query = query.offset(skip).limit(search.limit)
    
    return query.all()

@router.get("/{property_id}", response_model=PropertySchema)
async def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    """Get a property by ID"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@router.put("/{property_id}", response_model=PropertySchema)
async def update_property(
    *,
    db: Session = Depends(get_db),
    property_id: int,
    property_in: PropertyUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a property"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if db_property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = property_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_property, field, value)
    
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.post("/{property_id}/images")
async def upload_property_images(
    property_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload property images to IPFS"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if db_property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    image_hashes = []
    for file in files:
        content = await file.read()
        ipfs_hash = await upload_to_ipfs(content)
        image_hashes.append(ipfs_hash)
    
    db_property.images.extend(image_hashes)
    db.add(db_property)
    db.commit()
    
    return {"image_hashes": image_hashes}

@router.post("/{property_id}/documents")
async def upload_property_documents(
    property_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload property documents to IPFS"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if db_property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    doc_hashes = []
    for file in files:
        content = await file.read()
        ipfs_hash = await upload_to_ipfs(content)
        doc_hashes.append(ipfs_hash)
    
    db_property.documents.extend(doc_hashes)
    db.add(db_property)
    db.commit()
    
    return {"document_hashes": doc_hashes}

@router.post("/{property_id}/mint")
async def mint_property_nft(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mint a property as an NFT on Sui blockchain"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if db_property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if db_property.token_id:
        raise HTTPException(status_code=400, detail="Property is already minted")
    
    # TODO: Implement NFT minting logic using Sui SDK
    # This is a placeholder for the actual minting logic
    token_id = "placeholder_token_id"
    
    db_property.token_id = token_id
    db.add(db_property)
    db.commit()
    
    return {"token_id": token_id}

@router.post("/{property_id}/list")
async def list_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List a property for sale"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if db_property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not db_property.token_id:
        raise HTTPException(status_code=400, detail="Property must be minted first")
    
    # TODO: Implement listing logic using Sui SDK
    # This is a placeholder for the actual listing logic
    
    db_property.is_listed = True
    db.add(db_property)
    db.commit()
    
    return {"status": "listed"} 