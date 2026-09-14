from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.note_repository = NoteRepository(db)
        self.label_repository = LabelRepository(db)
        self.share_repository = ShareRepository(db)

    # Permissions
    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.share_repository.has_note_share(note_id=note.id, user_id=user_id):
            return True

        label_ids = self.label_repository.get_labels_id_by_note(note_id=note.id)

        return self.share_repository.has_label_share(labels_id=label_ids, user_id=user_id)

    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.share_repository.has_note_share(note_id=note.id, user_id=user_id, role=ShareRole.EDIT):
            return True

        label_ids = self.label_repository.get_labels_id_by_note(note_id=note.id)
        return self.share_repository.has_label_share(labels_id=label_ids, user_id=user_id, role=ShareRole.EDIT)

    def list_notes_by_user(self, user_id: int) -> list[Note]:
        owned = self.note_repository.get_owned_notes(user_id)

        direct_ids = self.share_repository.list_note_ids_shared(user_id=user_id)

        shared_label_ids = self.share_repository.list_labels_shared(user_id=user_id)

        ids_by_label = self.label_repository.get_notes_by_label_ids(label_ids=shared_label_ids)

        combined_ids = list({*direct_ids, *ids_by_label})

        shared = self.note_repository.list_by_ids(ids=combined_ids)
        combined = {note.id: note for note in owned}

        for note in shared:
            combined.setdefault(note.id, note)

        return sorted(combined.values(), key=lambda note: note.id, reverse=True)

    def create_note(self, owner_id: int, note_data: NoteCreate) -> Note:
        note = self.note_repository.create_note(
            Note(
                owner_id=owner_id,
                **note_data.model_dump(exclude={"label_ids"})
            )
        )

        if note_data.label_ids:
            self._set_labels(owner_id=owner_id, note_id=note.id, label_ids=note_data.label_ids)

        return note

    def update_note(self, user_id: int, note_id: int, note_data: NoteUpdate) -> Note:
        note = self.note_repository.get_note_by_id(note_id)

        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

        if not self.user_can_edit(user_id, note):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have permission")

        update_data = note_data.model_dump(exclude_unset=True)
        label_ids = update_data.pop("label_ids", None)

        for key, value in update_data.items():
            setattr(note, key, value)

        updated_note = self.note_repository.update_note(note)

        if label_ids is not None:
            if updated_note.owner_id != user_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't have permission")

            self._set_labels(user_id, updated_note.id, label_ids)

        return updated_note

    def delete_note(self, user_id: int, note_id: int) -> None:
        note = self.note_repository.get_note_by_id(note_id)

        if not note or note.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Note not found or user doesn't have permission")

        self.note_repository.delete_note(note)

    def _set_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        valid_ids = self.label_repository.get_ids_by_owner_subset(owner_id=owner_id, ids=label_ids or [])
        self.note_repository.replace_labels(owner_id=owner_id, note_id=note_id, labels_id=valid_ids)
