from pydantic import BaseModel, ValidationError as PydanticError
from typing import Optional

class HabitSchema(BaseModel):
    """
    Schema for creating a new habit/diary entry.
    title is required when creating a new item.
    """
    title: str
    frequency: Optional[str] = "daily"
    done: Optional[bool] = False
    notes: Optional[str] = None
    date: Optional[str] = None

    @classmethod
    def validate(cls, data):
        try:
            return cls(**data).dict()
        except PydanticError as e:
            raise ValidationError(str(e))


class UpdateHabitSchema(BaseModel):
    """
    Schema for partial updates. All fields are optional so you can PATCH/PUT
    only the fields you want to change (e.g. {'done': True}).
    """
    title: Optional[str] = None
    frequency: Optional[str] = None
    done: Optional[bool] = None
    notes: Optional[str] = None
    date: Optional[str] = None

    @classmethod
    def validate(cls, data):
        # Accept empty dict (no changes) — will be handled by route/model logic.
        try:
            return cls(**(data or {})).dict(exclude_none=True)
        except PydanticError as e:
            raise ValidationError(str(e))


class ValidationError(Exception):
    pass
