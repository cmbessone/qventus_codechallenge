from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.part_schema import PartCreate, PartUpdate, PartOut
from app.services import part_service

router = APIRouter(prefix="/parts", tags=["Parts"])


@router.get("/", response_model=list[PartOut])
def get_parts(db: Session = Depends(get_db)):
    return part_service.list_parts(db)


@router.get("/top-words", tags=["Analysis"])
def get_top_words(db: Session = Depends(get_db)):
    return part_service.top_words(db)


@router.get("/{part_id}", response_model=PartOut)
def get_part(part_id: int, db: Session = Depends(get_db)):
    part = part_service.retrieve_part(db, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part


@router.post("/", response_model=PartOut)
def create_part(part: PartCreate, db: Session = Depends(get_db)):
    created_part = part_service.add_part(db, part)
    if created_part is None:
        raise HTTPException(status_code=400, detail="Part with this SKU already exists")
    return created_part


@router.put("/{part_id}", response_model=PartOut)
def update_part(part_id: int, part: PartUpdate, db: Session = Depends(get_db)):
    updated = part_service.modify_part(db, part_id, part)
    if updated is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return updated


@router.delete("/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    success = part_service.remove_part(db, part_id)
    if not success:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"message": "Part deleted successfully"}
