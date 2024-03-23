from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from typing import List, Optional
from .. import schemas, models, oauth2
from ..db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# get all posts
# @router.get("/", response_model=List[schemas.PostOut])
@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user), limit: int = 30, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


# inserting a post into the database
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(user_id=get_current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# getting a post with an id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

# deleting a post from the database
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.first().user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return {"Deleted post": post}
    
# updating a post in the database
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    updated_post.updated_at = datetime.now()
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    return post_query.first()


    
