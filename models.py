from pydantic import validator
# from local
from database import Base
# from 3rd party lib
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class Users(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True, index=True)
	first_name = Column(String)
	last_name = Column(String)
	company_name = Column(String)
	age = Column(Integer)
	city = Column(String)
	state = Column(String)
	zip = Column(Integer)
	email = Column(String, unique=True, index=True)
	web = Column(String)
