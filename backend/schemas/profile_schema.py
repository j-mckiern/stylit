from pydantic import BaseModel

class ProfileCreateRequest(BaseModel):
    id: str
    username: str
    display_name: str | None = None
    pfp_url: str
    visibility: str


class ProfileUpdateRequest(BaseModel):
    username: str | None = None
    display_name: str | None = None
    visibility: str | None = None


class ProfileResponse(BaseModel):
    id: str
    username: str
    display_name: str | None = None
    pfp_url: str
    visibility: str
