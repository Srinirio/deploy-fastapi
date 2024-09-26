from pydantic import BaseModel


class MaterialRequestResponse(BaseModel):
    id: int
    material_name: str
    
    class Config:
        orm_mode = True
        
class MaterialResponse(BaseModel):
    material_name: str
    material_count: int

    class Config:
        orm_mode = True
        
class MaterialAdminResponse(MaterialRequestResponse):
    amount: float
        
class MaterialIn(BaseModel):
    material_name: str
    amount: float
    
    class Config:
        orm_mode = True
        
class MaterialUpdateIn(BaseModel):
    material_name: str | None = None
    amount: float | None = None
    
    class Config:
        orm_mode = True
