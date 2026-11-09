from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteRead, NoteReplace, NoteStatus, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_note_or_404(note_id: UUID, db: Session) -> Note:
    note = db.get(Note, note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    return note


@router.get("", response_model=list[NoteRead])
def list_notes(
    db: DatabaseSession,
    note_status: Annotated[NoteStatus | None, Query(alias="status")] = None,
    q: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Note]:
    statement = select(Note)
    if note_status is not None:
        statement = statement.where(Note.status == note_status.value)
    if q:
        search = f"%{q.strip()}%"
        statement = statement.where(
            or_(Note.title.ilike(search), Note.content.ilike(search))
        )

    statement = (
        statement.order_by(Note.pinned.desc(), Note.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(statement))


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: DatabaseSession) -> Note:
    note = Note(**payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/{note_id}", response_model=NoteRead)
def read_note(note_id: UUID, db: DatabaseSession) -> Note:
    return get_note_or_404(note_id, db)


@router.put("/{note_id}", response_model=NoteRead)
def replace_note(note_id: UUID, payload: NoteReplace, db: DatabaseSession) -> Note:
    note = get_note_or_404(note_id, db)
    note.title = payload.title
    note.content = payload.content
    db.commit()
    db.refresh(note)
    return note


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(note_id: UUID, payload: NoteUpdate, db: DatabaseSession) -> Note:
    note = get_note_or_404(note_id, db)
    for field, value in payload.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(note, field, value.value if isinstance(value, NoteStatus) else value)

    if not note.title.strip() and not note.content.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A note must have a title or content",
        )

    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: UUID, db: DatabaseSession) -> Response:
    note = get_note_or_404(note_id, db)
    db.delete(note)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)