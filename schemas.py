#  from pydantic
from pydantic import BaseModel, Field, EmailStr, validator
import pydantic
from typing import List, Optional, TypeVar, Generic
T = TypeVar('T')

class UserSchema(BaseModel):
	id : int
	first_name : str
	last_name : str
	company_name : Optional[str] = None
	age : int
	city : str
	state : str
	zip : int
	email : EmailStr
	web : Optional[str] = None

	@validator('id')
	def valid_id(cls, value):
		if value <= 0:
			raise ValueError(f"id must be positive: {value}")
		return value	
	class Config:
		orm_mode = True


class Response(pydantic.BaseModel,Generic[T]):
	code: str
	status: str
	message: str
	result: UserSchema