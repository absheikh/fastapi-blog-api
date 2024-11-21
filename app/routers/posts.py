from typing import Annotated, List
from fastapi import Depends, Response,status,HTTPException,Query, APIRouter
from .. import models,schemas
from sqlmodel import select
from ..database import SessionDep
from ..utils import CurrentUser
from sqlalchemy import func

router = APIRouter(tags=["Posts"], prefix="/api/v1/posts")




    

@router.get("/", response_model=List[schemas.PostBase])
def get_posts(
        session:SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
        current_user:dict = CurrentUser,
        )->list[models.Post]:
            #with user_id
            posts = session.exec(select(models.Post).where(models.Post.user_id == current_user.id).offset(offset).limit(limit)).all()
            results = session.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
            print(results)
            #add votes to post
            posts = [post.dict() for post in posts]
            
            for post in posts:
                for result in results:
                    if post["id"] == result[0].id:
                        post["votes"] = result[1]
                        
                        
            return posts
         

@router.post("/")
def create(post_obj:schemas.PostCreate,session:SessionDep,current_user:dict = CurrentUser):
    post_data = post_obj.dict()
    #add user_id to post_data
    post_data.update({"user_id":current_user.id})
    post = models.Post.model_validate(post_data)
    # print(post)
    session.add(post)
    session.commit()
    session.refresh(post)
    if post:
        return post
    
    
@router.get("/{id}", response_model=schemas.ResponseModel)
def get_post(session:SessionDep,id:int,  current_user:dict = CurrentUser):
        post = session.exec(select(models.Post).where(models.Post.id == id and models.Post.user_id == current_user.id)).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"success": True, "message": "Post retrieved successfully", "data": post.model_dump()}
   
@router.put("/{id}")
def update_post(session: SessionDep, id: int, post_data: schemas.PostUpdate, current_user:dict = CurrentUser):
    db_post = session.exec(select(models.Post).where(models.Post.id == id and models.Post.user_id == current_user.id)).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post = post_data.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    
    return db_post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(session: SessionDep, id: int, current_user:dict = CurrentUser):
    post = session.exec(select(models.Post).where(models.Post.id == id and models.Post.user_id == current_user.id)).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
  