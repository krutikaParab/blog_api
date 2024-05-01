from fastapi import FastAPI, Depends, Response, status
from .schemas import Blog
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=201, tags=['Blogs'])
def create(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", tags=['Blogs'])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}/", status_code=200, response_model=schemas.Blog, tags=['Blogs'])
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with id {id} not found"}
    return blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(id: int, request: schemas.Blog,
           db: Session = Depends(get_db)):
    db.query(models.Blog).get(id).update(request)
    db.commit()
    return "Updated"


@app.delete("/blog/{id}/delete", status_code=status.HTTP_404_NOT_FOUND, tags=['Blogs'])
def delete_blog(id: int, db: Session = Depends(get_db)):
    del_blog = db.query(models.Blog).get(id)
    db.delete(del_blog)
    db.commit()
    return {"detail": f"Blog id with {id} deleted successfully"}


@app.post("/user", response_model=schemas.ShowUser, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


