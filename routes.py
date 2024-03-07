from typing import List, Optional
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



@router.post("/create", response_model=Response)
def createuser_service(request: List[UserSchema], db: Session = Depends(get_db)):
    result = crud.create_user(db, request)

    if result == None:
        return Response(status="Error", code="500", message="Failed to create user", result=None)
    else:
        return Response(status="Ok", code="200", message="User created successfully", result=result)


@router.get("/{id:int}", response_model=Response)
def get(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, id, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch user by ID", result=user)


@router.get("/", response_model=Response)
def get(skip: int = 0, limit: int = 100, name: str=None, sort: str='id', db: Session = Depends(get_db)):
        users = crud.get_users(db, skip, limit, name , sort)
        if users:
            user_dicts = [user for user in users]
            print(user_dicts)
            return Response(status="Ok", code="200", message="Success fetch all data", result=user_dicts)
        else:
            return Response(status="Error", code="404", message="User not found", result=None)

# no partial update at the moment
@router.patch("/update/{id:int}")
def updateuser(id: int, request: UserSchema, db: Session = Depends(get_db)):
    user = crud.update_user(db, pk=id, user_data=request.model_dump())
    if user == None:
        return Response(status="Error", code="404", message="User Not Found", result=None)
    else:
        return Response(status="Ok", code="200", message="Success update data", result=user)


@router.delete("/delete/{id:int}")
def deleteuser(id:int, db: Session = Depends(get_db)):
    user=crud.remove_user(db, pk=id)
    if user == None:
        return Response(status="Error", code="404", message="User Not Found", result=None)
    else:
        return Response(status="Ok", code="200", message="Success deleted data", result=None)
