import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.schemas import UserCreateSchema
from passlib.context import CryptContext


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
        
async def create_user(user_data: UserCreateSchema):
    
    from src.models import User
    
    existing_user = await User.get_or_none(email=user_data.email)
    if existing_user:
        return {
            "message": "User already exists with this email",
            "status": 409,
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

    return {
       "message": "New user created successfully",
       "status": 201,
       "user": {
           "uuid": str(user.uuid), 
           "email": user.email,
           "phone": user.phone,
           "name": user.name
       }
    }
