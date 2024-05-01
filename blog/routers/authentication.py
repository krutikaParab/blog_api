from fastapi import APIRouter, Depends, Response, status, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags=['Auth'],
    prefix="/auth"
)


@router.post('/login')
def login(request: schemas.LoginUser, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    # verify user with an email
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    # verify user password
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect Password")
    return user