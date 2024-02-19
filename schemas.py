#  from pydantic
from pydantic import BaseModel, Field
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
	email : str
	web : Optional[str] = None

	class Config:
		orm_mode = True


class Response(pydantic.BaseModel,Generic[T]):
	code: str
	status: str
	message: str
	result: UserSchema