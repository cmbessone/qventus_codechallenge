# scripts/preload_data.py

from app.database import SessionLocal, Base, engine
from app.models.part_model import Part

# Create the database and tables
Base.metadata.create_all(bind=engine)

# Insert data provided in Database
parts = [
    Part(
        name="Heavy coil",
        sku="SDJDDH8223DHJ",
        description="Tightly wound nickel-gravy alloy spring",
        weight_ounces=22,
        is_active=True,
    ),
    Part(
        name="Reverse lever",
        sku="DCMM39823DSJD",
        description="Attached to provide inverse leverage",
        weight_ounces=9,
        is_active=False,
    ),
    Part(
        name="Macrochip",
        sku="OWDD823011DJSD",
        description="Used for heavy-load computing",
        weight_ounces=2,
        is_active=True,
    ),
]

db = SessionLocal()
db.add_all(parts)
db.commit()
db.close()

print("✅ DB preloaded.")
