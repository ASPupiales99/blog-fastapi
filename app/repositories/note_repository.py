from sqlmodel import Session, select, delete

from app.models.label import NoteLabelLink
from app.models.note import Note


class NoteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_owned_notes(self, owner_id: int) -> list[Note]:
        query = select(Note).where(Note.owner_id == owner_id).order_by(Note.id.desc())
        return self.db.exec(query).all()

    def get_note_by_id(self, note_id: int) -> Note | None:
        return self.db.get(Note, note_id)

    def create_note(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note

    def update_note(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note

    def delete_note(self, note: Note) -> None:
        query = delete(NoteLabelLink).where(NoteLabelLink.note_id == note.id)
        self.db.exec(query)
        self.db.delete(note)
        self.db.commit()

    def replace_labels(self, owner_id: int, note_id: int, labels_id: list[int]) -> None:
        query = delete(NoteLabelLink).where(NoteLabelLink.note_id == note_id)
        self.db.exec(query)

        for label in set(labels_id) or []:
            self.db.add(NoteLabelLink(note_id=note_id, label_id=label))

        self.db.commit()

    def list_by_ids(self, ids: list[int]) -> list[Note]:
        if not ids:
            return []

        return self.db.exec(
            select(Note).where(Note.id.in_(ids))
        ).all()
