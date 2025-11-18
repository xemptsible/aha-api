from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

router = APIRouter(
    prefix="/items", tags=["items"], responses={404: {"description": "Not found"}}
)

fake_items_db = [{"item": "HK416"}, {"item": "PA-15"}]


@router.get("/")
async def read_items():
    print("called")
    return fake_items_db


@router.get("/current/")
async def read_current_item():
    return {"item": "current-item"}


@router.get("/current/{item_name}")
async def read_item(item_name: str):
    return {"item": item_name}


@router.post("/create/")
async def add_item(item_name: Annotated[str, Body()]):
    new_fake_items_db = [*fake_items_db, {"item": item_name}]
    return new_fake_items_db


@router.put("/edit/")
async def edit_item(
    edited_item: Annotated[str, Body()], new_item: Annotated[str, Body()]
):
    new_fake_items_db = [*fake_items_db]
    for i, n in enumerate(new_fake_items_db):
        if n["item"] == edited_item:
            new_fake_items_db[i] = {"item": new_item}
            return new_fake_items_db

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
