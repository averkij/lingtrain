from datetime import datetime

from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: int
    guid: str
    lang: str
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}
