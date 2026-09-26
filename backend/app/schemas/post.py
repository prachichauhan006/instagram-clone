from pydantic import BaseModel


class PostCreate(BaseModel):
    caption: str | None = None
    image_url: str | None = None