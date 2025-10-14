from fastapi import APIRouter, HTTPException, status, Depends
from src.schemas import UserCreateSchema, TokenSchema, LoginSchema
from fastapi.security import OAuth2PasswordBearer
from src.utils import UserMethod

router = APIRouter()
user_method = UserMethod()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")



@router.post("/user", status_code=status.HTTP_201_CREATED)
async def createUser(user: UserCreateSchema):
    new_user = await user_method.create_user(user_data=user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request, invalid datas offering"
        )

    if "error" in new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=new_user["error"]
        )

    return {
        "message": "User created with successfully",
        "data": new_user
    }
    
@router.post("/user/login", response_model=TokenSchema)
async def login(user: LoginSchema):
    try:
        exists_user = await user_method.get_user(user_data=user)
        
        if exists_user.get("status") != 200:
            raise HTTPException(
                status_code=exists_user.get("status"),
                detail=exists_user.get("message")
            )

        return {
            "access_token": exists_user.get("access_token"),
            "token_type": "bearer"
        }

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        )
        
@router.get("/user/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    user_uuid = UserMethod.verify_token(token)
    if not user_uuid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    from src.models import User
    user = await User.get_or_none(uuid=user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return {
        "uuid": str(user.uuid),
        "email": user.email,
        "name": user.name,
        "phone": user.phone
    }