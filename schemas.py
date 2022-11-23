from typing import Optional, List
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserLogin(UserBase):
    email: str
    password: str


class UserCreate(UserBase):
    """
    請求模型驗證：
    email:
    password:
    """
    email: str
    password: str


class User(UserBase):
    """
    響應模型：
    id:
    email:
    is_active
    並且設定orm_mode與之相容
    """
    id: int
    is_active: bool
    items: List[Item] = []


class Config:
    orm_mode = True
