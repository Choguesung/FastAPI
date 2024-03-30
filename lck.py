from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from bson.json_util import dumps

app = FastAPI()

client = MongoClient('mongodb+srv://admin:qwer1234@cluster0.yqujlrz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',tlsInsecure=True)

db = client["lck"]
team_collection = db["team"]
player_collection = db["player"]

class Item(BaseModel):
    name: str
    description: str

# 팀 이름으로 조회
@app.get("/team/{name}")
async def read_team(name: str):
    item = team_collection.find_one({"name": name}, {"_id": 0})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/team/names")
async def get_team_names():
    # team_collection에서 "name" 필드의 모든 고유한 값을 가져옵니다.
    team_names = team_collection.distinct("name")
    return team_names
    
@app.get("/player/{name}")
async def read_player(name: str):
    item = player_collection.find_one({"name": name}, {"_id": 0})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")
