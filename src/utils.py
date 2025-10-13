import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
from tortoise import fields, models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
hairrag_pdf = os.path.join(BASE_DIR, "data", "hairrag.pdf")

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
        
class UUIDModel(models.Model):
    uuid = fields.UUIDField(pk=True, default=uuid.uuid4)
    
    class Meta:
        abstract = True  
