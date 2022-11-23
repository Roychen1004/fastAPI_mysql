from typing import List
from fastapi import FastAPI, Depends, HTTPException
import crud
import schemas
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    """
    每一個請求處理完畢後會關閉當前連線，不同的請求使用不同的連線
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")  # 指定 api 路徑 (get方法)
def read_root():
    return {"Hello": "World"}


# 新建使用者
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.db_create_user(db=db, user=user)


# 通過id查詢使用者
@app.get("/users/{user_id}", response_model=schemas.UserCreate)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    return {"email": db_user.email, "password": db_user.hashed_password}


# 登入 /get 422 Unprocessable Entity
"""
@app.get("/users/login/{user_email}", response_model=schemas.UserLogin)
def comfirm_user(user_email: str, user_password: str, db: Session = Depends(get_db)):
    #print("Error start")
    db_user = crud.login_user(
        db=db, lg_email=user_email)
    print("password:", db_user.hashed_password)
    #print("lg_email:", user_email)
    #print("down_Error start")
    return {"email": db_user.email, "password": db_user.hashed_password}

"""
# 登入2.0


@app.post("/users/login")  # , response_model=schemas.User)
def comfirm_user(user_email: str, user_password: str, db: Session = Depends(get_db)):
    db_user = crud.login_user(
        db=db, lg_email=user_email)
    print("db_user = ", db_user)

    if not db_user:
        return {"email is wrong!"}
    elif db_user.hashed_password != user_password:
        return {"password is wrong!"}
    else:
        return {"wellcome user:": db_user.id}


# 讀取使用者擁有的item

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    items = crud.get_item(db=db, skip=skip, limit=limit)
    return items


# 建立使用者的item
@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
