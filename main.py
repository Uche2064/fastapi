from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# to create a schema you need to import the pydantic library. A schema is defined to tell the user what data we need from him

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True    


my_posts = [
    {
        "title": "title of post 1", 
        "content": "content of post 1",
        "id": 1
    },
    
    {
        "title": "title of post 2", 
        "content": "content of post 2",
        "id": 2
    },
    
    ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        

@app.get("/posts")
def get_post():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post.model_dump())
    
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    
    post = find_post(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, default=f"Post with id {id} not found")
    my_posts.pop(index)
    return {"message": "Post removed"}
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, default=f"Post with id {id} not found")
    
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}