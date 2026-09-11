from sqlmodel import Session, select, delete

from app.models.label import Label, NoteLabelLink
from app.models.share import LabelShare


class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_labels_by_owner(self, owner_id: int) -> list[Label] | None:
        query = select(Label).where(Label.owner_id == owner_id).order_by(Label.name.asc())
        return self.db.exec(query).all()

    def get_label_by_id(self, label_id: int) -> Label | None:
        return self.db.get(Label, label_id)

    def get_label_by_name(self, owner_id: int, label_name: str) -> Label | None:
        query = select(Label).where(
            Label.owner_id == owner_id,
            Label.name == label_name
        ).order_by(Label.name)
        return self.db.exec(query).first()

    def create_label(self, owner_id: int, name: str) -> Label:
        label = Label(owner_id=owner_id, name=name)

        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)

        return label

    def delete_label(self, label: Label) -> None:
        self.db.exec(
            delete(NoteLabelLink).where(NoteLabelLink.label_id == label.id)
        )

        self.db.exec(
            delete(LabelShare).where(LabelShare.label_id == label.id)
        )

        self.db.delete(label)
        self.db.commit()

    def get_ids_by_owner_subset(self, owner_id: int, ids: list[int]) -> list[int]:
        if not ids:
            return []

        return self.db.exec(
            select(Label.id).where(
                Label.owner_id == owner_id,
                Label.id.in_(set(ids))
            )
        ).all()

    def get_labels_id_by_note(self, note_id: int) -> list[int]:
        return self.db.exec(
            select(NoteLabelLink.label_id).where(NoteLabelLink.note_id == note_id)
        ).all()

    def get_notes_by_label_ids(self, label_ids: list[int]) -> list[int]:
        if not label_ids:
            return []

        return self.db.exec(
            select(NoteLabelLink.note_id).where(NoteLabelLink.label_id.in_(label_ids))
        ).all()
