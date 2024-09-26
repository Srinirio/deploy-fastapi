
from pydantic import BaseModel,EmailStr,Field,validator

class EmployeeIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    destination_id: int
    phone_number: str = Field(...,max_length=10,min_length=10)
    report_to: str | None = None
    
    @validator('phone_number')
    def validate_phone_number(cls, value: str):
        if not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        return value
    
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone_number: str | None = None
    destination_name: str  
    report_to_name: str | None = None  
    
    class Config:
        orm_mode = True
        
class UpdateUserIn(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    destination_id: int | None = None
    phone_number: str | None = Field(...,max_length=10,min_length=10)
    report_to: str | None = None
    is_active: bool | None = None
    
    @validator('phone_number')
    def validate_phone_number(cls, value: str):
        if not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        return value
    
class EmployeeUnderHeadResponse(BaseModel):
    id: str
    name: str
    email: str
    phone_number: str | None = None
    
class EmployeeInUnderHead(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str = Field(...,max_length=10,min_length=10)
    
    @validator('phone_number')
    def validate_phone_number(cls, value: str):
        if not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        return value
    

 
    



