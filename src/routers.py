from fastapi import APIRouter, HTTPException
from src.schemas import UserCreateSchema
from src.utils import create_user

router = APIRouter()

@router.get("/")
def hello():
    return {"message": "System running"}

@router.post("/user")
async def createUser(user: UserCreateSchema):    
    new_user = await create_user(user_data=user)
    if new_user.get("status") != 201:
        raise HTTPException(status_code=new_user.get('status'), detail=new_user.get("message"))
    
    return new_user
    

    
    



