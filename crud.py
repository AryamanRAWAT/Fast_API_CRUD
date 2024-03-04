# from local
from typing import List
from fastapi import HTTPException
from models import Users
from schemas import UserSchema
# from python lib
import traceback
# from 3rd party
from sqlalchemy.orm import Session


def get_users(db: Session, skip: int, limit: int, name: str, sort: str):
	try:
		query = db.query(Users)
		if name:
			query = query.filter((Users.first_name.ilike(f"%{name}%")) | (Users.last_name.ilike(f"%{name}%")))

		if sort[0]=="-":       
			query = query.order_by(getattr(Users, sort[1:]).desc())
		else:
			query = query.order_by(sort)

		return query
	except:
		print(traceback.format_exc())
		raise HTTPException(status_code=500, detail="Internal Server Error")

def get_user_by_id(db: Session, pk: int):
	# try:
		user = db.query(Users).filter(Users.id == pk).first()
		if user:
			return user
		else:
			raise HTTPException(status_code=404, detail="User not found")
	# except:
	# 	print(traceback.format_exc())
	# 	raise HTTPException(status_code=500, detail="Internal Server Error")
	
def create_user(db: Session, request: List[UserSchema]):
	try:
		users = []
		print(request)
		for entry in request:
			data = entry.model_dump()
			user = Users(
						**data
						)
			db.add(user)
			db.commit()
			db.refresh(user)
			users.append(user)
		return users
	except:
		print(traceback.format_exc())
		raise HTTPException(status_code=500, detail="Internal Server Error")

def remove_user(db: Session, pk: int):
	try:	
		user = get_user_by_id(db=db, pk=pk)
		if user:
			db.delete(user)
			db.commit()
		else:
			return None
	except:
		print(traceback.format_exc())
		raise HTTPException(status_code=500, detail="Internal Server Error")

def update_user(db: Session, pk: int, user_data: dict):
	try:
		user = db.query(Users).filter(Users.id == pk).first()
		if not user:
			raise HTTPException(status_code=404, detail="User not found")

		for key, value in user_data.items():
			setattr(user, key, value)

		db.commit()
		db.refresh(user)
		return user
	except:
		print(traceback.format_exc())
		raise HTTPException(status_code=500, detail="Internal Server Error")