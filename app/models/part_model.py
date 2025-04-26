from sqlalchemy import Column, Integer, String
from app.database import Base


class Part(Base):
    __tablename__ = "part"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(30), unique=True, nullable=False)
    description = Column(String(1024))
    weight_ounces = Column(Integer)
    is_active = Column(Integer, default=1)  # 1 = True, 0 = False
