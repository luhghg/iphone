from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserBase(BaseModel):
    username: str
    email: EmailStr
    


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)



class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)



class UserResponse(BaseModel):
    id: int 
    is_active: bool 
    role: str 

    model_config = ConfigDict(from_attributes = True) 



class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)



class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")



