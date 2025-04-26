from pydantic import BaseModel


class PartBase(BaseModel):
    name: str
    sku: str
    description: str
    weight_ounces: int
    is_active: bool = True


class PartCreate(PartBase):
    pass


class PartUpdate(PartBase):
    pass


class PartOut(PartBase):
    id: int

    class Config:
        from_attributes = True
