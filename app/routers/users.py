from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, FastAPI, Depends, APIRouter
from  sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# inserting a user into the user table
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.password
    user.password = utils.hash(user.password)
    get_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if get_user:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="E-mail déjà pris")
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user 

# getting a user with a specific id
@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with the id: {id} doesn't exist")
    return user