from fastapi import APIRouter, status

from router import item, resources, authors, tags

api_router = APIRouter()


api_router.include_router(item.router)
api_router.include_router(resources.router)
api_router.include_router(authors.router)
api_router.include_router(tags.router)


@api_router.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"status": "Server is running"}
