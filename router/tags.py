from fastapi import APIRouter
from sqlmodel import select

from ..core.db import SessionDep
from ..core.models import Tag, TagsPublic

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Resource not found"}},
)


@router.get("/", response_model=TagsPublic)
async def read_tags(session: SessionDep):
    data = session.exec(select(Tag)).all()

    return {"data": data, "count": len(data)}
