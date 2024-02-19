from typing import List
from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import UserSchema, Response
import crud


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/create", response_model=UserSchema)
def createuser_service(request: UserSchema, db: Session = Depends(get_db)):
    crud.create_user(db, user=request)
    return Response(status="Ok",code="200",message="user created successfully")


@router.get("/", response_model=List[UserSchema])
def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = crud.get_users(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=user)


@router.patch("/update")
def updateuser(request: UserSchema, db: Session = Depends(get_db)):
    user = crud.update_user(db, pk=request.parameter.id,)
    return Response(status="Ok", code="200", message="Success update data", result=user)


@router.delete("/delete")
def deleteuser(request: UserSchema,  db: Session = Depends(get_db)):
    crud.remove_user(db, pk=request.parameter.id)
    return Response(status="Ok", code="200", message="Success! Deleted the data").dict(exclude_none=True)