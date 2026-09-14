from fastapi import APIRouter, status

from app.api.deps import DBSession, CurrentUser
from app.models.share import ShareRequest
from app.services import share_service

router = APIRouter(prefix="/shares", tags=["Share"])


@router.post("/notes/{note_id}", status_code=status.HTTP_200_OK)
def share_note(note_id: int, payload: ShareRequest, user: CurrentUser, db: DBSession):
    share = share_service.ShareService(db).share_note(
        owner_id=user.id,
        note_id=note_id,
        target_user_id=payload.target_user_id,
        role=payload.role
    )

    return {
        "id": share.id,
        "note_id": note_id,
        "target_user_id": payload.target_user_id,
        "role": share.role,
    }


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_note(note_id: int, target_user_id: int, user: CurrentUser, db: DBSession):
    share_service.ShareService(db).unshare_note(
        owner_id=user.id,
        note_id=note_id,
        target_user_id=target_user_id
    )


@router.post("/labels/{label_id}", status_code=status.HTTP_201_CREATED)
def share_label(label_id: int, payload: ShareRequest, user: CurrentUser, db: DBSession):
    share = share_service.ShareService(db).share_label(
        owner_id=user.id,
        label_id=label_id,
        target_user_id=payload.target_user_id,
        role=payload.role
    )

    return {
        "id": share.id,
        "label_id": label_id,
        "target_user_id": payload.target_user_id,
        "role": share.role,
    }


@router.delete("/label/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_label(label_id: int, target_user_id: int, user: CurrentUser, db: DBSession):
    share_service.ShareService(db).unshare_label(
        owner_id=user.id,
        label_id=label_id,
        target_user_id=target_user_id
    )
