import mimetypes
from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import or_, select

from ..core.db import SessionDep
from ..core.models import (
    Author,
    Resource,
    ResourceAuthorLink,
    ResourceCreate,
    ResourceTagLink,
    ResourcesWithAuthorsAndTags,
    Tag,
)

router = APIRouter(
    prefix="/resources",
    tags=["resources"],
    responses={404: {"description": "Resource not found"}},
)


@router.get("/", response_model=ResourcesWithAuthorsAndTags)
async def read_resources(
    session: SessionDep,
    author: Annotated[list[str], Query()] = [],
    tag: Annotated[list[str], Query()] = [],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    author_where_clause = []
    tag_where_clause = []
    data = []

    join_statement = (
        select(Resource)
        .distinct()
        .join(ResourceAuthorLink)
        .join(Author)
        .join(ResourceTagLink)
        .join(Tag)
        .offset(offset)
        .limit(limit)
    )

    if len(author) > 0:
        for author_query in author:
            author_where_clause.append(Author.name == author_query)

    if len(tag) > 0:
        for tag_query in tag:
            tag_where_clause.append(Tag.name == tag_query)

    if len(author) > 0:
        data = session.exec(join_statement.where(or_(*author_where_clause))).all()
    if len(tag) > 0:
        data = session.exec(join_statement.where(or_(*tag_where_clause))).all()
    if len(author) > 0 and len(tag) > 0:
        data = session.exec(
            join_statement.where(or_(*author_where_clause, *tag_where_clause))
        ).all()
    if len(author) == 0 and len(tag) == 0:
        data = session.exec(select(Resource).offset(offset).limit(limit)).all()

    for resource in data:
        if resource.image and resource.image.url:
            mime_type = mimetypes.guess_type(resource.image.url)[0] or ""
            image_format = mime_type[6::]

            # Skip converting Imgur link. See https://github.com/weserv/images/issues/319
            # Use 'm' for medium-size Imgur images. See https://thomas.vanhoutte.be/miniblog/imgur-thumbnail-trick/
            if resource.image.url.find(
                "imgur"
            ) != -1 and not resource.image.url.endswith(".jpeg"):
                resource.image.url = resource.image.url.replace(".jpg", "t.jpeg")
            elif resource.image.url.find(
                "imgur"
            ) != -1 and not resource.image.url.endswith(".png"):
                resource.image.url = resource.image.url.replace(".png", "t.png")
            else:
                if image_format in ("png"):
                    print("well that happened")
                    # Max compression and adaptive filter
                    resource.image.url = (
                        f"http://wsrv.nl/?url={resource.image.url}&output=webp&q=1"
                    )
                elif image_format in ("jpeg", "jpg", "webp"):
                    print("well that happened 2")
                    resource.image.url = (
                        f"http://wsrv.nl/?url={resource.image.url}&q=1"
                    )

    return {"data": data, "count": len(data)}


@router.post("/", response_model=ResourcesWithAuthorsAndTags)
async def create_resources(session: SessionDep, resource: ResourceCreate):
    pass
