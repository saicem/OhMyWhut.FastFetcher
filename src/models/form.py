from pydantic import BaseModel


class LoginForm(BaseModel):
    username: str
    password: str


class ElectricForm(LoginForm):
    meterId: str
    factoryCode: str


class CoursePngForm(LoginForm):
    week: int = 0
