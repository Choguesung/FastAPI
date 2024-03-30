from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from bson.json_util import dumps

app = FastAPI()

client = MongoClient('mongodb+srv://admin:qwer1234@cluster0.yqujlrz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',tlsInsecure=True)

db = client["lck"]
collection = db["player"]

class Item(BaseModel):
    name: str
    description: str

# Create (데이터 삽입)
@app.post("/items/create/")
async def create_item(item: Item):
    result = collection.insert_one(item.dict())
    return {"id": str(result.inserted_id), "data": item}


# Read (데이터 조회) 
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = collection.find_one({"name": item_id}, {"_id": 0})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# # Update (데이터 업데이트)
# @app.put("/items/{item_id}")
# async def update_item(item_id: str, item: Item):
#     updated_item = collection.update_one({"_id": item_id}, {"$set": item.dict()})
#     if updated_item.modified_count:
#         return {"id": item_id, "updated_data": item}
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")

# # Delete (데이터 삭제)
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: str):
#     deleted_item = collection.delete_one({"_id": item_id})
#     if deleted_item.deleted_count:
#         return {"id": item_id, "status": "deleted"}
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")

# Read all items (모든 데이터 조회)
@app.get("/items/")
async def read_all_items():
    items = []
    for item in collection.find():
        items.append(item)
    return dumps(items)
