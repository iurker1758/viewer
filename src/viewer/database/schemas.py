from viewer.public.schemas import BaseSchema


class DatabaseSchema(BaseSchema):
    """Schema for fetching database documents."""

    db: str


class DatabaseUpdateSchema(BaseSchema):
    """Schema for updating database documents."""

    db: str
    page: str
