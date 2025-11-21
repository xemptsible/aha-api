from fastapi import APIRouter
from sqlmodel import select

from ..core.db import SessionDep
from ..core.models import Image, ImagesPublic

router = APIRouter(
    prefix="/images", tags=["images"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=ImagesPublic)
async def read_images(session: SessionDep):
    data = session.exec(select(Image)).all()

    return {"data": data, "count": len(data)}
