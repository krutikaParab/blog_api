from fastapi import APIRouter, Depends, Response, status
from ..schemas import Blog
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags=['User'],
    prefix="/User"
)


@router.post("/", response_model=schemas.ShowUser, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

