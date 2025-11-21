from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class ResourceTagLink(SQLModel, table=True):
    __tablename__ = "resource_tag_link"  # type: ignore
    resource_id: int = Field(default=None, foreign_key="resource.id", primary_key=True)
    tag_id: int = Field(default=None, foreign_key="tag.id", primary_key=True)


class ResourceAuthorLink(SQLModel, table=True):
    __tablename__ = "resource_author_link"  # type: ignore
    resource_id: int = Field(default=None, foreign_key="resource.id", primary_key=True)
    author_id: int = Field(default=None, foreign_key="author.id", primary_key=True)


class ImageBase(SQLModel):
    name: str
    url: str
    alt_text: str


class ImagePublic(ImageBase):
    id: int


class ImagesPublic(BaseModel):
    data: list["ImagePublic"]
    count: int


class ImageCreate(BaseModel):
    name: str | None = None
    url: str | None = None
    alt_text: str | None = None


class ImageUpdate(BaseModel):
    name: str | None = None
    url: str | None = None


class Image(ImageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    resource_thumbnail: Optional["Resource"] = Relationship(
        back_populates="image", sa_relationship_kwargs={"uselist": False}
    )


class ResourceBase(SQLModel):
    title: str
    description: str
    url: str


class ResourceCreate(ResourceBase):
    image_id: int | None = None


class ResourceUpdate(BaseModel):
    title: str | None = None
    author: set[str] | None = None
    tags: set[str] | None = None
    description: str | None = None


class ResourcePublic(ResourceBase):
    id: int


class ResourcesPublic(BaseModel):
    data: list[ResourcePublic]
    count: int


class Resource(ResourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_id: Optional[int] = Field(default=None, foreign_key="image.id")

    authors: list["Author"] = Relationship(
        back_populates="credited_resources", link_model=ResourceAuthorLink
    )
    tags: Optional[list["Tag"]] = Relationship(
        back_populates="related_resources", link_model=ResourceTagLink
    )
    image: Optional["Image"] = Relationship(
        back_populates="resource_thumbnail", sa_relationship_kwargs={"uselist": False}
    )


class ResourceWithAuthorsAndTags(ResourceBase):
    id: int
    authors: list["AuthorPublic"] = []
    tags: list["TagPublic"] = []
    image: ImagePublic | None = None


class ResourcesWithAuthorsAndTags(BaseModel):
    data: list["ResourceWithAuthorsAndTags"]
    count: int


class TagBase(SQLModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None


class TagPublic(TagBase):
    id: int


class TagsPublic(BaseModel):
    data: list["TagPublic"]
    count: int


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    related_resources: list["Resource"] = Relationship(
        back_populates="tags", link_model=ResourceTagLink
    )


class AuthorBase(SQLModel):
    name: str
    personal_site: str


class AuthorPublic(AuthorBase):
    id: int


class AuthorsPublic(BaseModel):
    data: list["AuthorPublic"]
    count: int


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = None
    personal_site: str | None = None


class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    credited_resources: list["Resource"] = Relationship(
        back_populates="authors", link_model=ResourceAuthorLink
    )
