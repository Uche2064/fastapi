from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class PostBase(BaseModel):
    id: Optional[int] = None
    title: str
    content: str 
    published: bool = True  
    
class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str
    content: str 
    published: bool
    updated_at: Optional[datetime] = None

    
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class Post(PostBase):
    created_at: datetime
    updated_at: datetime
    user_id: int
    user: User

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

        
class LoginUser(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1) # type: ignore