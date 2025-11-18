from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import or_, select

from core.db import SessionDep
from core.models import (
    Author,
    Resource,
    ResourceAuthorLink,
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

    return {"data": data, "count": len(data)}
