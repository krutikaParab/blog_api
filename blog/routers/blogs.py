from fastapi import APIRouter, Depends, Response, status
from ..schemas import Blog
from .. import schemas, models, database
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Blogs'],
    prefix="/blog"
)


@router.get("/")
def get_all_blog(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/", status_code=201)
def create(blog: Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{id}/", status_code=200, response_model=schemas.Blog)
def get_blog_by_id(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with id {id} not found"}
    return blog


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog,
           db: Session = Depends(database.get_db)):
    db.query(models.Blog).get(id).update(request)
    db.commit()
    return "Updated"


@router.delete("/{id}/delete", status_code=status.HTTP_404_NOT_FOUND)
def delete_blog(id: int, db: Session = Depends(database.get_db)):
    del_blog = db.query(models.Blog).get(id)
    db.delete(del_blog)
    db.commit()
    return {"detail": f"Blog id with {id} deleted successfully"}


