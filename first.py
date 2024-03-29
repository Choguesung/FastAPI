from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import riotapi

app = FastAPI()

# MongoDB 연결
client = MongoClient('mongodb+srv://admin:qwer1234@cluster0.yqujlrz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',tlsInsecure=True)
db = client["test"]
collection = db["test"]

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 프로덕션 환경에서는 특정 origin으로 제한하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    title: str
    content: str

class Nickname(BaseModel):
    nickname: str
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/title")
def get_first_title():
    # MongoDB에서 첫 번째 문서 읽기
    document = collection.find_one({})
    
    if document:
        title = document.get("title", "Title not found")
        return {"title": title}
    else:
        return {"error": "Document not found"}

# 리액트에서 글제목, 내용받아서 몽고 디비에 올리는 코드임
@app.post("/post")
def create_post(post: Post):
    # FastAPI의 모델 검증을 통과한 데이터를 MongoDB에 삽입
    result = collection.insert_one(post)
    if result.inserted_id:
        return {"message": "Post created successfully", "post_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create post")
    
# 서버로 닉네임 + 태그라인
@app.get("/riotpost/{nickname}/{tagline}")
async def riot_post(nickname: str, tagline: str):

    result = riotapi.search(str(nickname),str(tagline))

    return {"result": result}

@app.get("/isplayed/{nickname}/{tagline}")
async def riot_post(nickname: str, tagline: str):

    result = riotapi.is_played(str(nickname),str(tagline))

    try:
        result["status"]
        return {"result" : "게임중이 아닙니다"}
    
    except:
        return {"result" : result}