from pydantic import BaseModel, ConfigDict

from viewer.public.utils import to_camel


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


class UserSchema(BaseSchema):
    """Schema for user information."""

    username: str
    role: str
