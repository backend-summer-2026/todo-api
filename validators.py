from pydantic import BaseModel, EmailStr, field_validator, model_validator


class User(BaseModel):
   username: str
   email: EmailStr
   password: str
   confirm: str

   @field_validator("username")
   @staticmethod
   def validate_username(value: str) -> str:
       if len(value) < 3:
           raise ValueError("username kamida 3 ta belgidan iborat bolishi kerak")
       return value

   @field_validator("password")
   @staticmethod
   def validate_password(value: str) -> str:
       if len(value) < 8:
           raise ValueError("password kamida 8 ta belgidan iborat bolishi kerak")
       return value

   @field_validator("confirm")
   @staticmethod
   def validate_confirm(value: str) -> str:
       if len(value) < 8:
           raise ValueError("confirm kamida 8 ta belgidan iborat bolishi kerak")
       return value

   @model_validator(mode='after')
   @staticmethod
   def validate_password_match(obj):
       if obj.password != obj.confirm:
           raise ValueError("passowrd va confirm teng bolishi kerak")
       return obj


data = {
    "username": "alijon",
    "email": "ali@gmail.com",
    "password": "12345678",
    "confirm": "12345678"
}

# validate
"""
1. field level
2. object level
"""

try:
    User.model_validate(data)
except Exception as exc:
    print(exc)
