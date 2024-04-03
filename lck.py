from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from bson.json_util import dumps
import os
import riotapi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용. 필요에 따라 변경 가능
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

mongodb_uri = os.environ.get('MONGODB_URL')
client = MongoClient(mongodb_uri,tlsInsecure=True)

db = client["lck"]
team_collection = db["team"]
player_collection = db["player"]

class Item(BaseModel):
    name: str
    description: str

# 팀 이름으로 조회함
@app.get("/team/{name}")
async def read_team(name: str):
    item = team_collection.find_one({"name": name}, {"_id": 0})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# 모든 팀의 팀명만 리턴함
@app.get("/team/names")
async def get_team_names():
    teams = team_collection.find()
    if teams:
        team_names = [{"name": team["name"] for team in teams}]
        return team_names
    else:
        raise HTTPException(status_code=404, detail="Item not found")

    
@app.get("/player/{name}")
async def read_player(name: str):
    item = player_collection.find_one({"name": name}, {"_id": 0})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# 팀명으로 선수이름 리스트 받아오기
@app.get("/getplayerbyteam/{team_name}")
async def get_player_by_team(team_name: str):
    players = player_collection.find({"team" : team_name}, {"_id" : 0})

    players = list(players)

    if players:
        # processed_players = [{"name": player["name"]} for player in players]
        return players
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    

# 특정 유저가 게임중이면, 게임중인 데이터, 게임중이 아니면 게임중이 아니라고 알림
@app.get("/isplayed/{nickname}/{tagline}")
async def riot_post(nickname: str, tagline: str):

    result = riotapi.is_played(str(nickname),str(tagline))

    try:
        result["status"]
        return {"result" : "게임중이 아닙니다"}
    
    except:
        return {"result" : result}