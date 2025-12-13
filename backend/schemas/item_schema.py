from pydantic import BaseModel


class ItemCreateRequest(BaseModel):
    user_id: str
    name: str
    category: str
    style: str
    season: str
    color: str
    visibility: str
