from fastapi import APIRouter, Depends, File, Form, UploadFile
from dependencies.user_auth import get_current_user
from services.profile_service import ProfileService
from schemas.profile_schema import (
    ProfileCreateRequest,
    ProfileUpdateRequest,
    ProfileResponse,
)
from gotrue.types import User

router = APIRouter(prefix="/profiles", tags=["Profiles"], dependencies=[Depends(get_current_user)])

service = ProfileService()


@router.post("/", summary="Create user profile", status_code=201)
async def create_profile(
    current_user: User = Depends(get_current_user),
    username: str = Form(...),
    display_name: str = Form(...),
    visibility: str = Form(...),
    pfp: UploadFile | None = File(None),
):
    """
    Create profile in the 'profiles' table.
    """
    profile = ProfileCreateRequest(
        id=current_user.id,
        username=username,
        display_name=display_name,
        visibility=visibility,
    )
    return await service.create_profile(profile, pfp)

@router.get("/verify")
async def verify_user(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.id}! You have access to protected data."}

@router.get("/me", summary="Get user profile by id", response_model=list[ProfileResponse])
async def get_profiles(
    current_user: User = Depends(get_current_user)
):
    """
    Fetch profiles by id from the 'profiles' table.
    """
    return await service.read_profiles(profile_id=current_user.id)

@router.get("/", summary="Get user profiles", response_model=list[ProfileResponse])
async def get_profiles():
    """
    Fetch profiles from the 'profiles' table.
    """
    return await service.read_profiles()


@router.get("/{username}", summary="Get user profiles by username", response_model=list[ProfileResponse])
async def get_profiles(
    username: str
):
    """
    Fetch profiles by username from the 'profiles' table.
    """
    return await service.read_profiles(username=username)


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
    return await service.update_profile(profile_id, profile, pfp)


@router.delete("/", summary="Delete user profile", status_code=204)
async def delete_profile(profile_id: str):
    """
    Delete profile from the 'profiles' table.
    """
    return await service.delete_profile(profile_id)