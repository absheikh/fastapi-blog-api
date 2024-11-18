from typing import Annotated
from fastapi import Response,status,HTTPException,Query, APIRouter
from .. import models,schemas
from sqlmodel import select
from ..database import SessionDep


router = APIRouter(tags=["Posts"], prefix="/api/v1/posts")




    

@router.get("/", response_model=schemas.ResponseModel)
def get_posts(
        session:SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,)->list[models.Post]:
            posts = session.exec(select(models.Post).offset(offset).limit(limit)).all()
            return {"success": True, "message": "Posts retrieved successfully", "data": posts}
         

@router.post("/")
def create(post_data:schemas.PostCreate,session:SessionDep):
    post = models.Post.model_validate(post_data)
    session.add(post)
    session.commit()
    session.refresh(post)
    if post:
        return post
    
    
@router.get("/{id}", response_model=schemas.ResponseModel)
def get_post(session:SessionDep,id:int, response: Response):
        post = session.get(models.Post, id) 
        if post is None:
            return {"success": False, "message": "Post not found"}
        return {"success": True, "message": "Post retrieved successfully", "data": post.model_dump()}
   
@router.put("/{id}")
def update_post(session: SessionDep, id: int, post_data: schemas.PostUpdate):
    db_post = session.get(models.Post, id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post = post_data.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    
    return db_post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(session: SessionDep, id: int):
    post = session.exec(select(models.Post).where(models.Post.id == id)).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
  