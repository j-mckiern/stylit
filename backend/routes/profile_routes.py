from fastapi import APIRouter, File, Form, UploadFile
from services.profile_service import ProfileService
from schemas.profile_schema import (
    ProfileCreateRequest,
    ProfileUpdateRequest,
    ProfileResponse,
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

service = ProfileService()


@router.post("/", summary="Create user profile", status_code=201)
async def create_profile(
    id: str = Form(...),
    username: str = Form(...),
    display_name: str = Form(...),
    visibility: str = Form(...),
    pfp: UploadFile | None = File(None),
):
    """
    Create profile in the 'profiles' table.
    """
    profile = ProfileCreateRequest(
        id=id,
        username=username,
        display_name=display_name,
        visibility=visibility,
    )
    response = await service.create_profile(profile, pfp)
    return response


@router.get("/", summary="Get user profiles", response_model=list[ProfileResponse])
async def get_profiles(username: str | None = None, profile_id: str | None = None):
    """
    Fetch profiles from the 'profiles' table.
    """
    response = await service.read_profiles(username, profile_id)
    return response


@router.put("/", summary="Update user profile", status_code=204)
async def update_profile(
    profile_id: str,
    username: str | None = Form(None),
    display_name: str | None = Form(None),
    visibility: str | None = Form(None),
    pfp: UploadFile | None = File(None),
):
    """
    Update profile in the 'profiles' table.
    """
    profile = ProfileUpdateRequest(
        username=username,
        display_name=display_name,
        visibility=visibility,
    )
    response = await service.update_profile(profile_id, profile, pfp)
    return response


@router.delete("/", summary="Delete user profile", status_code=204)
async def delete_profile(profile_id: str):
    """
    Delete profile from the 'profiles' table.
    """
    response = await service.delete_profile(profile_id)
    return response
