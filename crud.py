from sqlalchemy.orm import Session
import models
import schemas


# 通過id查詢使用者
def get_user(db: Session, user_id: int):
    seach_user = db.query(models.User).filter(
        models.User.id == user_id).first()
    # print(type(seach_user))
    # print(seach_user.email)
    return seach_user


# 新建使用者-
def db_create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password  # + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()  # 提交儲存到資料庫中
    db.refresh(db_user)  # 重新整理
    return db_user

# 登入


def login_user(db: Session, lg_email: str):
    e = db.query(models.User).filter(
        models.User.email == lg_email).first()
    # print(type(seach_user))
    # print(seach_user.email)
    return e


# 獲取使用者擁有的item


def get_item(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# 新建使用者的item
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
