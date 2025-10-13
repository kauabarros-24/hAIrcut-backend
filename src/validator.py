from email_validator import validate_email, EmailNotValidError

def emailValidator(email: str):
    if not email:
        return {"message": "Email is requested"}
    
    try:
        valid_email = validate_email(email)
        return valid_email.email
    except EmailNotValidError as error:
        return {"message": f"Email is not valid: {str(error)}"}
    except Exception as error:
        raise ValueError(f"There's a exception in email validator: {str(error)}")
    
def formatPhone(phone, region):
    pass

