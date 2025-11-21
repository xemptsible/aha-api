from fastapi import APIRouter
from sqlmodel import select

from ..core.db import SessionDep
from ..core.models import Author, AuthorsPublic

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    responses={404: {"description": "Resource not found"}},
)


@router.get("/", response_model=AuthorsPublic)
async def read_authors(session: SessionDep):
    data = session.exec(select(Author)).all()
    return {"data": data, "count": len(data)}
