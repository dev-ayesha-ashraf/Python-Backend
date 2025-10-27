from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    description: str
    Published: bool = True
    rating: Optional[int] = "None"

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Welcom To the Fast Api"}

@app.get("/posts")
async def get_posts():
    return {"Message: " : "This is the post"}

@app.post("/create-posts")
async def create_posts(post: Post):
    print(post)
    print(post.model_dump())
    return {"Data" : post.model_dump()}