from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    email: EmailStr
    full_name: str
    subject: str
    message: str

class EmailResponse(BaseModel):
    success: bool
    message: str