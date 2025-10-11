import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from src.config import GEMINI_API_KEY
from src.utils import ReportLab

report_lab = ReportLab()
chunks_result = report_lab.getInitialDocs()
chunks = chunks_result.get("chunks", [])

if not chunks:
    raise ValueError("Nenhum chunk encontrado. Verifique se o PDF existe e tem conteúdo.")

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
vector_store = FAISS.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

rag_prompt_template = """
Você é um analisador de templates que deverá recomendar os dois ou três melhores cortes de cabelo masculino.
Seja realista sobre a aparência do usuário.

<context>
{context}
</context>

Pergunta: {input}
"""

rag_prompt = ChatPromptTemplate.from_template(rag_prompt_template)
document_chain = create_stuff_documents_chain(llm, rag_prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

perguntas = [
    "Tenho rosto redondo e cabelo cacheado, qual corte devo escolher?",
    "Meu cabelo é liso e fino, qual o melhor estilo para parecer mais cheio?",
    "Quero algo moderno mas discreto, o que me recomenda?",
    "Tenho testa grande e cabelo ondulado, o que fazer?",
    "Meu cabelo está caindo, que corte ajuda a disfarçar?",
]

for i, pergunta in enumerate(perguntas, 1):
    resposta = retrieval_chain.invoke({"input": pergunta})
    print(f"Pergunta {i}: {pergunta}")
    print(f"Resposta {i}:\n{resposta}\n{'-'*50}\n")
