#  from pydantic
from pydantic import BaseModel, Field, validator
import pydantic
from typing import List, Optional, TypeVar, Generic, Union
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

	@validator('id')
	def valid_id(cls, value):
		if value <= 0:
			raise ValueError(f"id must be positive: {value}")
		return value	
	class Config:
		from_attributes = True


class Response(pydantic.BaseModel):
    code: str
    status: str
    message: str
    result: Union[List[UserSchema], UserSchema, str, None] 

    class Config:
        from_attributes = True
