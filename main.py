
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db import SessionLocal, engine, Base
from model import User


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI()


# Pydantic schema
class UserCreate(BaseModel):
    name: str
    phone: str


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str

    class Config:
        from_attributes = True


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Create User
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        phone=user.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# 2. Get All Users
@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users


# 3. Get User By ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# 4. Update User
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = user_data.name
    user.phone = user_data.phone

    db.commit()
    db.refresh(user)

    return user


# 5. Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
