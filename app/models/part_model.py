from sqlalchemy import Column, Integer, String
from app.database import Base


class Part(Base):
    __tablename__ = "part"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(30), unique=True, nullable=False)
    description = Column(String(1024))
    weight_ounces = Column(Integer)
    _is_active = Column("is_active", Integer, default=1)  # 1 = True, 0 = False

    @property
    def is_active(self) -> bool:
        return self._is_active == 1

    @is_active.setter
    def is_active(self, value: bool):
        self._is_active = 1 if value else 0
