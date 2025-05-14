from ninja import Schema, Field
from pydantic import field_validator


class RegisterInSchema(Schema):
    username: str
    password: str

    # @field_validator('username', mode='before')
    # def validate_username(cls, v: str):
    #     return v.strip()
    #
    # @field_validator('password', mode='before')
    # def validate_username(cls, v: str):
    #     return v.strip()
