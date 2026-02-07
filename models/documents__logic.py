from typing import List, Optional, Dict, Any
from sqlalchemy import select
import asyncio 
from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI
from views.database.documents import Document
from config import get_settings

settings = get_settings()
openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

class DocumentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(self, title: str, content: str) -> Document:
        doc = Document(title=title, content=content)
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def get_all_documents(self) -> List[Document]:
        stmt = select(Document)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_document_by_id(self, doc_id: int) -> Optional[Document]:
        stmt = select(Document).where(Document.id == doc_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def summarize_document(self, doc_id: int) -> str:
        doc = await self.get_document_by_id(doc_id)
        if not doc:
            raise ValueError("Document not found")

        prompt = f"Summarize the following document in 3-5 bullet points:\n\n{doc.content}"
        try:
            response = await openai_client.chat.completions.create(  # ← вот так теперь
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # можно добавить, если хочешь разнообразия
                max_tokens=300,   # лимит, чтоб не улетел в бесконечность
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"LLM error: {str(e)}")

    async def ask_question(self, doc_id: int, question: str) -> str:
        doc = await self.get_document_by_id(doc_id)
        if not doc:
            raise ValueError("Document not found")

        prompt = (
            f"Answer the question based only on the following document content. "
            f"If the answer is not in the document, say 'Not found in the document':\n\n"
            f"Document: {doc.content}\n\nQuestion: {question}"
        )
        try:
            response = await openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"LLM error: {str(e)}")