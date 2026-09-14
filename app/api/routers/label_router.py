from fastapi import APIRouter, status

from app.api.deps import DBSession, CurrentUser
from app.models.label import LabelRead, LabelCreate
from app.services.label_service import LabelService

router = APIRouter(prefix="/labels", tags=["Label"])


@router.get("/", response_model=list[LabelRead], status_code=status.HTTP_200_OK)
def list_labels(db: DBSession, user: CurrentUser):
    return LabelService(db).list(user.id)


@router.post("/", response_model=LabelRead, status_code=status.HTTP_201_CREATED)
def create_label(db: DBSession, label_data: LabelCreate, user: CurrentUser):
    return LabelService(db).create(owner_id=user.id, label_data=label_data)


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(db: DBSession, label_id: int, user: CurrentUser):
    LabelService(db).delete(owner_id=user.id, label_id=label_id)
