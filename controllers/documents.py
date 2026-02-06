from datetime import datetime
import io
import json
import os
from typing import Optional, Annotated
import zipfile
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select

from config import  get_settings
from controllers.unifided_request import role_secure, unifided_request
from database import get_async_db
from jwt_auth import get_current_user
from models.documents__logic import DocumentService
from views.json.unifided import UnifidedResponse
from views.json.v3.applications import AddAppRequestScheme
from pydantic import BaseModel
import openai
from views.database.documents import Document


router = APIRouter(prefix='/documents', tags=["Документы"])  # noqa 401
settings = get_settings()
CURRENT_HOST = settings.current_host  # noqa 501

openai.api_key = settings.openai_api_key

class DocumentCreate(BaseModel):
    title: str
    content: str

class Question(BaseModel):
    question: str


@router.post("/documents", response_model=UnifidedResponse, status_code=200)
@unifided_request
def create_document(
            _response: Response,
            request: Request,
            doc: DocumentCreate,
            db: AsyncSession = Depends(get_async_db)):
    db_doc = Document(title=doc.title, content=doc.content)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.get("/documents", response_model=UnifidedResponse, status_code=200)
@unifided_request
def get_documents(
        _response: Response,
        request: Request,
        db: AsyncSession = Depends(get_async_db),
):
    return db.query(Document).all()

@router.get("/documents/{id}", response_model=UnifidedResponse, status_code=200)
@unifided_request
def get_document(
        _response: Response,
        request: Request,
        id: int, 
        db: AsyncSession = Depends(get_async_db)):

    doc = db.query(Document).filter(Document.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/documents/{id}/summarize", response_model=UnifidedResponse, status_code=200)
@unifided_request
def summarize(
            _response: Response,
            request: Request,
            id: int,
            db: AsyncSession = Depends(get_async_db)):
    doc = db.query(Document).filter(Document.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    prompt = f"Summarize the following document in 3-5 bullet points:\n\n{doc.content}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/{id}/ask", response_model=UnifidedResponse, status_code=200)
@unifided_request
def ask(
        _response: Response,
        request: Request,
        id: int, question: Question,
        db: AsyncSession = Depends(get_async_db)):
    doc = db.query(Document).filter(Document.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    prompt = f"Answer the question based only on the following document content. If the answer is not in the document, say 'Not found in the document':\n\nDocument: {doc.content}\n\nQuestion: {question.question}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))