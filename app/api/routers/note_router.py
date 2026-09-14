from fastapi import APIRouter, status

from app.api.deps import DBSession, CurrentUser
from app.models.note import NoteRead, NoteCreate, NoteUpdate
from app.services.note_service import NoteService

router = APIRouter(prefix="/note", tags=["Notes"])


@router.get("/", response_model=list[NoteRead], status_code=status.HTTP_200_OK)
def list_notes(db: DBSession, user: CurrentUser):
    return NoteService(db).list_notes_by_user(user.id)


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(db: DBSession, note_data: NoteCreate, user: CurrentUser):
    return NoteService(db).create_note(owner_id=user.id, note_data=note_data)


@router.patch("/{note_id}", response_model=NoteRead, status_code=status.HTTP_200_OK)
def update_note(db: DBSession, note_id: int, note_data: NoteUpdate, user: CurrentUser):
    return NoteService(db).update_note(note_id=note_id, note_data=note_data, user_id=user.id)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(db: DBSession, note_id: int, user: CurrentUser):
    NoteService(db).delete_note(note_id=note_id, user_id=user.id)
