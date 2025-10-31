from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    description: str
    Published: bool = True
    rating: Optional[int] = "None"

my_posts = [
    {'title': 'Title of post 1', 'description': 'Description of post 1', 'id': 1},
    {'title': 'Title of post 2', 'description': 'Description of post 2', 'id': 2},
    {'title': 'Title of post 3', 'description': 'Description of post 3', 'id': 3},
    {'title': 'Title of post 4', 'description': 'Description of post 4', 'id': 4},
    {'title': 'Title of post 5', 'description': 'Description of post 5', 'id': 5},
    {'title': 'Title of post 6', 'description': 'Description of post 6', 'id': 6},
    {'title': 'Title of post 7', 'description': 'Description of post 7', 'id': 7},
    {'title': 'Title of post 8', 'description': 'Description of post 8', 'id': 8},
    {'title': 'Title of post 9', 'description': 'Description of post 9', 'id': 9},
    {'title': 'Title of post 10', 'description': 'Description of post 10', 'id': 10},
]

def get_single_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def get_index_post(id):
    for i , p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message" : "Welcom To the Fast Api"}

@app.get("/posts")
async def get_posts():
    return {'data' : my_posts}

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"Data" : post_dict}

# @app.get("/posts/{id}")
# async def get_posts_by_id(id: int , response: Response):
#     post = get_single_posts(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"detail" : f'Post not found for id: {id}'}
#     return {"Data" : post}

#  ---------------- BETTER APPROACH ----------------

@app.get("/posts/{id}")
async def get_posts_by_id(id):
    post = get_single_posts(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f'post with id: {id} Not found')
    return {"Data" : post}


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int):
    deleted_post = get_index_post(id)
    if deleted_post == None:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND ,  detail={'message' : 'post with id {id} Not found'})
    my_posts.pop(deleted_post)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
      index = get_index_post(id)
      if index == None:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND ,  detail={'message' : 'post with id {id} Not found'})
      post_dict = post.model_dump()
      post_dict["id"] = id
      my_posts[index] = post_dict

      return {"Data" : post_dict}
      
