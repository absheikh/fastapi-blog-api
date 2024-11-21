
from typing import Annotated, List
from fastapi import Depends, Response,status,HTTPException,Query, APIRouter
from sqlalchemy import select
from .. import models,schemas
from ..database import SessionDep
from ..utils import CurrentUser

router = APIRouter(tags=["Vote"], prefix="/api/v1/vote")

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, session: SessionDep, current_user: dict = CurrentUser):
    # Check if the post exists
    post_query = session.exec(select(models.Post).where(models.Post.id == vote.post_id))
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The post you are trying to vote on does not exist"
        )

    # Check if a vote already exists for this post by the current user
    vote_query = session.exec(
        select(models.Vote).where(
            (models.Vote.post_id == vote.post_id) & 
            (models.Vote.user_id == current_user.id)
        )
    )
    found_vote = vote_query.first()

    if vote.dir == 1:  # Upvote
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already upvoted this post"
            )
        vote_data = vote.dict()
        vote_data.update({"user_id": current_user.id})
        new_vote = models.Vote(**vote_data)
        session.add(new_vote)
        session.commit()
        return {"success": True, "message": "Upvoted successfully", "data": new_vote}
    else:  # Remove upvote
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You have not upvoted this post"
            )
        session.delete(found_vote)
        session.commit()
        return {"success": True, "message": "Upvote removed successfully"}
        
   