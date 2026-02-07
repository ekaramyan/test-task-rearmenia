from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from controllers.unifided_request import unifided_request
from database import get_async_db
from models.documents__logic import DocumentService
from views.json.unifided import UnifidedResponse
from views.json.documents import DocumentCreate, DocumentResponse, Question

router = APIRouter(prefix="/documents", tags=["Документы"])

settings = get_settings()


async def get_document_service(db: AsyncSession = Depends(get_async_db)) -> DocumentService:
    return DocumentService(db)


@router.post("/", response_model=UnifidedResponse, status_code=200)
@unifided_request
async def create_document(
    _response: Response,
    request: Request,
    doc: DocumentCreate,
    service: DocumentService = Depends(get_document_service),
):
    created_doc = await service.create_document(doc.title, doc.content)

    return DocumentResponse.model_validate(created_doc)


@router.get("/", response_model=UnifidedResponse[list[DocumentResponse]], status_code=200)
@unifided_request
async def get_documents(
    _response: Response,
    request: Request,
    service: DocumentService = Depends(get_document_service),
):
    docs = await service.get_all_documents()
    return [DocumentResponse.model_validate(doc) for doc in docs]


@router.get("/{id}", response_model=UnifidedResponse[DocumentResponse], status_code=200)
@unifided_request
async def get_document(
    _response: Response,
    request: Request,
    id: int,
    service: DocumentService = Depends(get_document_service),
):
    doc = await service.get_document_by_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse.model_validate(doc)


@router.post("/{id}/summarize", response_model=UnifidedResponse, status_code=200)
@unifided_request
async def summarize(
    _response: Response,
    request: Request,
    id: int,
    service: DocumentService = Depends(get_document_service),
):
    try:
        summary = await service.summarize_document(id)
        return {"summary": summary}
    except ValueError:
        raise HTTPException(status_code=404, detail="Document not found")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{id}/ask", response_model=UnifidedResponse, status_code=200)
@unifided_request
async def ask(
    _response: Response,
    request: Request,
    id: int,
    question: Question,
    service: DocumentService = Depends(get_document_service),
):
    try:
        answer = await service.ask_question(id, question.question)
        return {"answer": answer}
    except ValueError:
        raise HTTPException(status_code=404, detail="Document not found")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))