from sqlalchemy.orm import Session
from sqlalchemy import select
from model import User
from schemas import UserBase,UserCreate,UserRead,UserUpdate
def create_user(db:Session,user:UserCreate):
    new_user=User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db:Session):
    all_users=select(User)
    return db.scalars(all_users).all()

def update_user(db:Session,user_id:int,user:UserUpdate):
    db_user=db.scalars(select(User).where(User.id==user_id)).first()
    if not db_user:
        return None
    for key, value in user.model_dump(exclude_none=True).items():
           setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def delete_user(db:Session,user_id:id):
    db_user=db.scalars(select(User).where(User.id==user_id)).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return True
        