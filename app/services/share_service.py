from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class ShareService:
    def __init__(self, db: Session):
        self.db = db
        self.share_repository = ShareRepository(db)
        self.note_repository = NoteRepository(db)
        self.label_repository = LabelRepository(db)

    def share_note(self, owner_id: int, note_id: int, target_user_id: int, role: ShareRole):
        note = self.note_repository.get_note_by_id(note_id)

        if not note or note.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Note not found or user does not have permission")

        share = self.share_repository.create_note_share(note_id=note_id, user_id=target_user_id,
                                                        role=role.value if hasattr(role, 'value') else role)

        return share

    def unshare_note(self, owner_id: int, note_id: int, target_user_id: int) -> None:
        note = self.note_repository.get_note_by_id(note_id)

        if not note or note.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Note not found or user does not have permission")

        self.share_repository.remove_note_share(note_id=note_id, user_id=target_user_id)

    def share_label(self, owner_id: int, label_id: int, target_user_id: int, role: ShareRole):
        label = self.label_repository.get_label_by_id(label_id)

        if not label or label.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Label not found or user does not have permission")

        share = self.share_repository.create_label_share(label_id=label_id, user_id=target_user_id,
                                                         role=role.value if hasattr(role, 'value') else role)

        return share

    def unshare_label(self, owner_id: int, label_id: int, target_user_id: int) -> None:
        label = self.label_repository.get_label_by_id(label_id)

        if not label or label.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Label not found or user does not have permission")

        self.share_repository.remove_label_share(label_id=label_id, user_id=target_user_id)
