from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

current_dir = os.path.dirname(__file__)
pdf_path = os.path.join(current_dir, "..", "..", "data", "hairrag.pdf")
hairrag_pdf = os.path.abspath(pdf_path)


class ReportLab:
    def getInitialDocs():
        try:
            loader = PyPDFLoader(hairrag_pdf)
            if not loader:
                return {"message": "pdf not found"}
        except Exception as error:
            raise ValueError(f"There's a exception in reporlab class: {error}")
        docs = loader.load()
        text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_spliter.split_documents(docs)
        return {"chunks": chunks}
