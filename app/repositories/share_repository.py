from typing import TypeVar, Type

from sqlmodel import Session, select, delete, SQLModel

from app.models.share import NoteShare, LabelShare

ShareT = TypeVar("ShareT", bound=SQLModel)


class ShareRepository:
    def __init__(self, db: Session):
        self.db = db

    def _upsert_share(self, model: Type[ShareT], role: str, **filters) -> ShareT:
        share = self.db.exec(
            select(model).filter_by(**filters)
        ).first()

        if share:
            share.role = role
        else:
            share = model(role=role, **filters)

        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        return share

    def _remove_share(self, model: Type[ShareT], **filters) -> None:
        self.db.exec(
            delete(model).filter_by(**filters)
        )
        self.db.commit()

    def _has_share(
            self,
            model: Type[ShareT],
            fk_field: str,
            fk_value: int | list[int],
            user_id: int,
            role: str | None = None,
    ) -> bool:
        if isinstance(fk_value, list) and not fk_value:
            return False

        column = getattr(model, fk_field)
        condition = column.in_(fk_value) if isinstance(fk_value, list) else column == fk_value

        query = select(model).where(condition, model.user_id == user_id)
        if role is not None:
            query = query.where(model.role == role)

        return self.db.exec(query).first() is not None

    def _list_shared_ids(self, model: Type[ShareT], fk_field: str, user_id: int) -> list[int]:
        column = getattr(model, fk_field)
        return self.db.exec(
            select(column).where(model.user_id == user_id)
        ).all()

    def create_note_share(self, note_id: int, user_id: int, role: str) -> NoteShare:
        return self._upsert_share(NoteShare, role, note_id=note_id, user_id=user_id)

    def remove_note_share(self, note_id: int, user_id: int) -> None:
        self._remove_share(NoteShare, note_id=note_id, user_id=user_id)

    def create_label_share(self, label_id: int, user_id: int, role: str) -> LabelShare:
        return self._upsert_share(LabelShare, role, label_id=label_id, user_id=user_id)

    def remove_label_share(self, label_id: int, user_id: int) -> None:
        self._remove_share(LabelShare, label_id=label_id, user_id=user_id)

    def has_note_share(self, note_id: int, user_id: int, role: str | None = None) -> bool:
        return self._has_share(NoteShare, "note_id", note_id, user_id, role)

    def has_label_share(self, labels_id: list[int], user_id: int, role: str | None = None) -> bool:
        return self._has_share(LabelShare, "label_id", labels_id, user_id, role)

    def list_note_ids_shared(self, user_id: int) -> list[int]:
        return self._list_shared_ids(NoteShare, "note_id", user_id)

    def list_labels_shared(self, user_id: int) -> list[int]:
        return self._list_shared_ids(LabelShare, "label_id", user_id)
