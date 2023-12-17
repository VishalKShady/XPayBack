from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Users
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"

class UserRequest(BaseModel):
    full_name:str = Field(min_length=3)
    email:str = Field(gt=0)
    password:str = Field(gt=0)
    phone:int = Field(gt=0, lt=11)
    profile_pic:bool



@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Users).all()



@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(db:db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_data(db: db_dependency, user_request: UserRequest):
    user_model = Users(**user_request.model_dump())

    db.add(user_model)
    db.commit()
