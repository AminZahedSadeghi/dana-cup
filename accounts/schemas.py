from ninja import Schema, Field
from pydantic import field_validator


class RegisterInSchema(Schema):
    username: str
    password: str


class AuthOutSchema(Schema):
    username: str
