from fastapi import APIRouter, HTTPException, status
from src.schemas import UserCreateSchema
from src.utils import create_user

router = APIRouter()

@router.post("/user", status_code=status.HTTP_201_CREATED)
async def createUser(user: UserCreateSchema):
    new_user = await create_user(user_data=user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar o usuário"
        )

    if "error" in new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=new_user["error"]
        )

    return {
        "message": "Usuário criado com sucesso",
        "data": new_user
    }
