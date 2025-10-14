import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.schemas import UserCreateSchema, LoginSchema
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from src.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
hairrag_pdf = os.path.join(BASE_DIR, "data", "hairrag.pdf")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print("Diretório de dados:", hairrag_pdf)
class ReportLab:
    def getInitialDocs(self):
        try:
            if not os.path.exists(hairrag_pdf):
                return {"message": f"PDF not found at {hairrag_pdf}"}

            loader = PyPDFLoader(hairrag_pdf)
            docs = loader.load()

            if not docs:
                return {"message": "PDF loaded but no content found"}

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = text_splitter.split_documents(docs)
            return {"chunks": chunks}

        except Exception as error:
            raise ValueError(f"There was an exception in ReportLab class: {error}")
        
class UserMethod:
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        from src.utils import pwd_context
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")
        except JWTError:
            return None
    
    @staticmethod
    async def create_user(user_data: UserCreateSchema):
        from src.models import User
        from src.utils import pwd_context
        
        existing_user = await User.get_or_none(email=user_data.email)
        if existing_user:
            return {
                "message": "User already exists with this email",
                "status": 409
            }

        hashed_password = pwd_context.hash(user_data.password)

        try:
            user = await User.create(
                name=user_data.name,
                email=user_data.email,
                phone=user_data.phone,
                password=hashed_password
            )
        except Exception as error:
            return {
                "status": 500,
                "message": f"Error creating user: {error}"
            }

        token = UserMethod.create_access_token({"sub": str(user.uuid)})

        return {
            "message": "New user created successfully",
            "status": 201,
            "user": {
                "uuid": str(user.uuid),
                "email": user.email,
                "phone": user.phone,
                "name": user.name
            },
            "access_token": token,
            "token_type": "bearer"
        }
        
    @staticmethod
    async def get_user(user_data: LoginSchema):
        from src.models import User
        from src.utils import pwd_context
        
        if not user_data:
            return {
                "message": "You need offer email and password to get user",
                "status": 400
            }

        try:
            user = await User.get_or_none(email=user_data.email)
            if not user:
                return {
                    "message": "User not found",
                    "status": 404
                }
        except Exception as error:
            return {
                "message": "There's an error in get user",
                "status": 500,
                "error": f"{error}"
            }

        if not pwd_context.verify(user_data.password, user.password):
            return {
                "message": "Invalid password",
                "status": 401
            }

        token = UserMethod.create_access_token({"sub": str(user.uuid)})

        return {
            "message": "User authenticated successfully",
            "status": 200,
            "user": {
                "uuid": str(user.uuid),
                "email": user.email,
                "name": user.name,
                "phone": user.phone
            },
            "access_token": token,
            "token_type": "bearer"
}

    