from sqlalchemy.orm import Session
from app.models.part_model import Part
from app.schemas.part_schema import PartCreate, PartUpdate
from app.logger import logger


def get_all_parts(db: Session):
    logger.info("Fetching all parts from the database.")
    return db.query(Part).all()


def get_part(db: Session, part_id: int):
    logger.info(f"Fetching part with ID: {part_id}")
    return db.query(Part).filter(Part.id == part_id).first()


def get_part_sku(db: Session, sku: str):
    logger.info(f"Fetching part with SKU: {sku}")  
    return db.query(Part).filter(Part.sku == sku).first()


def create_part(db: Session, part: PartCreate):
    logger.info(f"Creating new part with SKU: {part.sku}")
    part_data = part.model_dump()
    db_part = Part(**part_data)
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part


def update_part(db: Session, part_id: int, part_data: PartUpdate):
    logger.info(f"Updating part with ID: {part_id}")
    part = db.query(Part).filter(Part.id == part_id).first()
    if part:
        data = part_data.model_dump()
        for key, value in data.items():
            setattr(part, key, value)
        db.commit()
        db.refresh(part)
        logger.info(f"Part updated with ID: {part_id}")
    else:
        logger.warning(f"Part with ID: {part_id} not found for update.")
    return part


def update_part_sku(db: Session, sku: str, part_data: PartUpdate):
    logger.info(f"Updating part with SKU: {sku}")
    part = db.query(Part).filter(Part.sku == sku).first()
    if part:
        data = part_data.model_dump()
        for key, value in data.items():
            setattr(part, key, value)
        db.commit()
        db.refresh(part)
        logger.info(f"Part updated with SKU: {sku}")
    else:
        logger.warning(f"Part with SKU: {sku} not found for update.")
    return part


def delete_part(db: Session, part_id: int):
    part = db.query(Part).filter(Part.id == part_id).first()
    if part:
        db.delete(part)
        db.commit()
        logger.info(f"Part deleted with ID: {part_id}")
        return True
    else:
        logger.warning(f"Part with ID: {part_id} not found for deletion.")
    return False

