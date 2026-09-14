from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


class Label(SQLModel, table=True):
    __tablename__ = "label"
    __table_args__ = (UniqueConstraint("owner_id", "name", name="unq_label_owner_name"),)

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=50)
    owner_id: int = Field(index=True, foreign_key="user.id")


class NoteLabelLink(SQLModel, table=True):
    __tablename__ = "note_label_link"
    __table_args__ = (UniqueConstraint("note_id", "label_id", name="unq_label_note_id"),)

    id: int = Field(default=None, primary_key=True)
    note_id: int = Field(foreign_key="note.id", index=True)
    label_id: int = Field(foreign_key="label.id", index=True)


class LabelCreate(SQLModel):
    name: str


class LabelRead(SQLModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
