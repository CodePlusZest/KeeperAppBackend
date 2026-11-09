from datetime import datetime, timezone
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator


class NoteStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    TRASH = "trash"


class NoteDraft(BaseModel):
    title: str = Field(default="", max_length=120)
    content: str = Field(default="", max_length=100_000)

    @model_validator(mode="after")
    def require_title_or_content(self) -> "NoteDraft":
        if not self.title.strip() and not self.content.strip():
            raise ValueError("A note must have a title or content")
        return self


class NoteCreate(NoteDraft):
    pass


class NoteReplace(BaseModel):
    title: str = Field(max_length=120)
    content: str = Field(max_length=100_000)

    @model_validator(mode="after")
    def require_title_or_content(self) -> "NoteReplace":
        if not self.title.strip() and not self.content.strip():
            raise ValueError("A note must have a title or content")
        return self


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=120)
    content: str | None = Field(default=None, max_length=100_000)
    status: NoteStatus | None = None
    pinned: bool | None = None

    model_config = ConfigDict(extra="forbid")


class NoteRead(BaseModel):
    id: UUID
    title: str
    content: str
    status: NoteStatus
    pinned: bool
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def serialize_timestamp(self, value: datetime) -> int:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return round(value.timestamp() * 1000)