from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session, SQLModel, create_engine, select, text

from .models import Author, Image, Resource, Tag


class Settings(BaseSettings):
    db_url: str
    
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()  # type: ignore


engine = create_engine(url=get_settings().db_url, echo=False)


def create_db_and_tables():
    print("Creating database and tables...")
    SQLModel.metadata.create_all(engine)
    print("Successfully created database and table.")


def get_db_session():
    with Session(engine) as session:
        yield session


def init_db():
    try:
        with Session(engine) as session:
            session.exec(select(text("1")))

            print("Database is awake.")

            create_db_and_tables()

            create_test_data()
    except Exception as e:
        raise e


def create_test_data():
    images = [
        Image(
            name="An image",
            url="https://static.wikitide.net/bluearchivewiki/3/38/Lobby_Banner_20251112_01.png",
            alt_text="subie",
        ),
        Image(
            name="An image",
            url="https://static.wikitide.net/bluearchivewiki/c/ce/Lobby_Banner_20240904_01.png",
            alt_text="ui",
        ),
        Image(
            name="An image",
            url="https://static.wikitide.net/bluearchivewiki/a/a7/Lobby_Banner_20220907_01.png",
            alt_text="hina",
        ),
        Image(
            name="An image",
            url="https://i.imgur.com/8Iv7PhJ.jpg",
            alt_text="yesod",
        ),
    ]

    tags = [
        Tag(name="EN"),
        Tag(name="CN"),
        Tag(name="JP"),
        Tag(name="KR"),
        Tag(name="Beginner-focused"),
        Tag(name="Advanced"),
    ]

    resources = [
        Resource(
            title="Hina Loves Midokuni",
            description="Guide",
            url="https://hina.loves.midokuni.com/",
            tags=[tags[0], tags[1]],
            image=images[0],
        ),
        Resource(
            title="Joexyz",
            description="Guide",
            url="https://hina.loves.midokuni.com/",
            tags=[tags[0], tags[1], tags[4]],
            image=images[1],
        ),
        Resource(
            title="Shared guide",
            description="Guide",
            url="https://hina.loves.midokuni.com/",
            tags=[tags[0], tags[1], tags[3]],
            image=images[2],
        ),
        Resource(
            title="\u308f\u305f\u3057\u548c\u5c0f\u5e02",
            description="Guide",
            url="https://hina.loves.midokuni.com/",
            tags=[tags[0], tags[2], tags[4]],
            image=images[3],
        ),
    ]

    authors = [
        Author(
            name="Midokuni",
            personal_site="https://hina.loves.midokuni.com/",
            credited_resources=[resources[0], resources[2]],
        ),
        Author(
            name="Joexyz",
            personal_site="https://hina.loves.midokuni.com/",
            credited_resources=[resources[1], resources[2]],
        ),
        Author(
            name="こいち",
            personal_site="https://hina.loves.midokuni.com/",
            credited_resources=[resources[3]],
        ),
    ]

    with Session(engine) as session:
        test_author = session.exec(
            select(Author).where(Author.name == "Midokuni")
        ).first()
        if not test_author:
            print("New data incoming.")
            for tag in tags:
                session.add(tag)

            for author in authors:
                session.add(author)

            for image in images:
                session.add(image)

            for resource in resources:
                session.add(resource)

            session.commit()
        else:
            print("Data already created.")


SessionDep = Annotated[Session, Depends(get_db_session)]
