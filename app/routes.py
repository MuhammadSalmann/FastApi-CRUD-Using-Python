# app/routes.py
from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.models import Item, PyObjectId
from app.db import collection
from bson import ObjectId
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def read_root(request: Request):
    items = await collection.find().to_list(100)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@router.post("/items/")
async def create_item(name: str = Form(...), description: str = Form(...)):
    item = Item(name=name, description=description)
    result = await collection.insert_one(item.dict(by_alias=True))
    if result.inserted_id:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=400, detail="Item not created")

@router.get("/items/{item_id}")
async def read_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    item["_id"] = str(item["_id"])
    # for item in items:
    #     item["_id"] = str(item["_id"])
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/{item_id}/update")
async def read_update(request: Request, item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    # item["_id"] = str(item["_id"])
    return templates.TemplateResponse("update.html", {"request": request, "item": item})


@router.put("/items/{item_id}")
async def update_item(item_id: str, request: Request):
    data = await request.json()
    name = data.get("name")
    description = data.get("description")
    if name is None or description is None:
        raise HTTPException(status_code=422, detail="Name and description are required")
    result = await collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"name": name, "description": description}})
    if result.modified_count:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=404, detail="Item not found")
