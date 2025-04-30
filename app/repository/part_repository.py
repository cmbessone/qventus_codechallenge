from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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
    # Check for existing SKU
    existing_part = get_part_sku(db, part.sku)
    if existing_part:
        logger.warning(f"Part with SKU {part.sku} already exists")
        return None

    part_data = part.model_dump()
    is_active = part_data.pop("is_active", True)
    db_part = Part(**part_data)
    db_part.is_active = is_active  # This will use the setter
    db.add(db_part)
    try:
        db.commit()
        db.refresh(db_part)
        return db_part
    except IntegrityError:
        db.rollback()
        logger.error(f"Failed to create part with SKU {part.sku}")
        return None


def update_part(db: Session, part_id: int, part_data: PartUpdate):
    logger.info(f"Updating part with ID: {part_id}")
    part = db.query(Part).filter(Part.id == part_id).first()
    if part:
        data = part_data.model_dump()
        is_active = data.pop("is_active", part.is_active)
        for key, value in data.items():
            setattr(part, key, value)
        part.is_active = is_active  # This will use the setter
        try:
            db.commit()
            db.refresh(part)
            logger.info(f"Part updated with ID: {part_id}")
            return part
        except IntegrityError:
            db.rollback()
            logger.error(f"Failed to update part with ID {part_id}")
            return None
    else:
        logger.warning(f"Part with ID: {part_id} not found for update.")
        return None


def update_part_sku(db: Session, sku: str, part_data: PartUpdate):
    logger.info(f"Updating part with SKU: {sku}")
    part = db.query(Part).filter(Part.sku == sku).first()
    if part:
        data = part_data.model_dump()
        is_active = data.pop("is_active", part.is_active)
        for key, value in data.items():
            setattr(part, key, value)
        part.is_active = is_active  # This will use the setter
        try:
            db.commit()
            db.refresh(part)
            logger.info(f"Part updated with SKU: {sku}")
            return part
        except IntegrityError:
            db.rollback()
            logger.error(f"Failed to update part with SKU {sku}")
            return None
    else:
        logger.warning(f"Part with SKU: {sku} not found for update.")
        return None


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
