from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.label import Label, LabelCreate
from app.repositories.label_repository import LabelRepository


class LabelService():
    def __init__(self, db: Session):
        self.db = db
        self.repo = LabelRepository(db)

    def list(self, owner_id: int) -> list[Label]:
        return self.repo.get_labels_by_owner(owner_id=owner_id)

    def create(self, owner_id: int, label_data: LabelCreate) -> Label:
        if self.repo.get_label_by_name(owner_id=owner_id, label_name=label_data.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Label already exists")

        return self.repo.create_label(owner_id=owner_id, name=label_data.name)

    def delete(self, owner_id: int, label_id: int) -> None:
        label = self.repo.get_label_by_id(label_id=label_id)

        if not label or label.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Label not found or owner does not have permission")

        self.repo.delete_label(label)
