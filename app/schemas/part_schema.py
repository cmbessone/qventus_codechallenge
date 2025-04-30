from pydantic import BaseModel, ConfigDict


class PartBase(BaseModel):
    name: str
    sku: str
    description: str
    weight_ounces: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class PartCreate(PartBase):
    pass


class PartUpdate(PartBase):
    pass


class PartOut(PartBase):
    id: int
