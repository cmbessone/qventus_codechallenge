from sqlalchemy.orm import Session
from app.schemas.part_schema import PartCreate, PartUpdate
from app.repository import part_repository


def list_parts(db: Session):
    return part_repository.get_all_parts(db)


def retrieve_part(db: Session, part_id: int):
    return part_repository.get_part(db, part_id)


def add_part(db: Session, part: PartCreate):
    return part_repository.create_part(db, part)


def modify_part(db: Session, part_id: int, part: PartUpdate):
    return part_repository.update_part(db, part_id, part)


def remove_part(db: Session, part_id: int) -> bool:
    return part_repository.delete_part(db, part_id)


def top_words(db: Session, top_n: int = 5):
    parts = part_repository.get_all_parts(db)
    from collections import Counter

    words = " ".join([p.description or "" for p in parts]).lower().split()
    counter = Counter(words)
    return [
        {"word": word, "count": count} for word, count in counter.most_common(top_n)
    ]
