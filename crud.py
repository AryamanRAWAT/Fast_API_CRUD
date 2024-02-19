# from local
from fastapi import HTTPException
from models import Users
from schemas import UserSchema
# from python lib
import traceback
# from 3rd party
from sqlalchemy.orm import Session


def get_users(db: Session, skip: int = 0, limit: int = 100):
	try:
		users = db.query(Users).offset(skip).limit(limit).all()
		print(users, type(users))
		return users
	except:
		print(traceback.format_exc())
		return 'error'
def get_user_by_id(db: Session, pk: int):
	try:
		user = db.query(Users).filter(Users.id == pk).first()
		if user:
			return user
		else:
			raise HTTPException(status_code=404, detail="User not found")
	except:
		print(traceback.format_exc())
		return 'error'
def create_user( request: UserSchema,db: Session):
	try:
		print(request.id)
		user = Users(
					id = request.id, 
					first_name = request.first_name,
					last_name = request.last_name,
					age = request.age,
					city = request.city,
					state = request.state,
					zip = request.zip,
					email = request.email,
					web = request.web
					)
		db.add(user)
		db.commit()
		db.refresh(user)
		return user
	except:
		print(traceback.format_exc())
		return 'error'

def remove_user(db: Session, pk: int):
	try:	
		user = get_user_by_id(db=db, id=pk)
		db.delete(user)
		db.commit()
	except:
		print(traceback.format_exc())
		return 'error'


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
		return 'error'