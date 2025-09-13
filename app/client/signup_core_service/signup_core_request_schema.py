from pydantic import BaseModel


class SignupCoreRequestSchema(BaseModel):
    firstName: str
    lastName: str
    gender: str
    email: str
    username: str
    password: str
