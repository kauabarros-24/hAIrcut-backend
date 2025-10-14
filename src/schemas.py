from pydantic import BaseModel, field_validator
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import PhoneNumberFormat, parse, is_valid_number, format_number


class UserCreateSchema(BaseModel):
    email: str
    phone: str
    name: str
    password: str

    @field_validator("email")
    def validate_email_field(cls, v):
        
        try:
            valid = validate_email(v)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError(f"Email is not valid: {str(e)}")

    @field_validator("phone")
    def validate_phone_field(cls, v):
        try:
            parsed = parse(v, None)
            if not is_valid_number(parsed):
                raise ValueError("Phone number is not valid")
            return format_number(parsed, PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"Error parsing phone number: {str(e)}")
    
    @field_validator("password")
    def validate_password(cls, v):
        print(len(v))
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v
    