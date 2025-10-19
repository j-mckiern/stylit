from fastapi import HTTPException
from dependencies.supabase_client import supabase
from schemas.profile_schema import ProfileCreateRequest, ProfileUpdateRequest


class ProfileService:
    def __init__(self):
        pass

    async def create_profile(self, profile: ProfileCreateRequest):
        """Create a new user profile in the 'profiles' table."""
        # Check if profile with same id exists
        existing = supabase.table("profiles").select("*").eq("id", profile.id).execute()
        if existing.data:
            raise HTTPException(
                status_code=409, detail=f"Profile with id {profile.id} already exists"
            )
        
        # Check if profile with same username exists
        existing = supabase.table("profiles").select("*").eq("username", profile.username).execute()
        if existing.data:
            raise HTTPException(
                status_code=409, detail=f"Profile with username {profile.username} already exists"
            )

        data = profile.model_dump()
        response = supabase.table("profiles").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create profile")
        return None

    async def read_profiles(self, username: str | None = None, profile_id: str | None = None):
        """Read user profiles from the 'profiles' table."""
        query = supabase.table("profiles").select("*")
        if profile_id:
            query = query.eq("id", profile_id)
        elif username:
            query = query.eq("username", username)
        response = query.execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="No profiles found")
        return response.data

    async def update_profile(self, profile_id: str, profile: ProfileUpdateRequest):
        """Update an existing user profile in the 'profiles' table."""
        # Check profile exists
        existing = supabase.table("profiles").select("*").eq("id", profile_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Profile not found")

        data = profile.model_dump(exclude_unset=True)
        # If username is being updataed check its not taken
        if(data["username"]):
            existing = supabase.table("profiles").select("*").eq("username", profile.username).execute()
            if existing.data:
                raise HTTPException(
                    status_code=409, detail=f"Profile with username {profile.username} already exists"
                )

        # Update profile
        response = (
            supabase.table("profiles").update(data).eq("id", profile_id).execute()
        )
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to update profile")
        return None

    async def delete_profile(self, profile_id: str):
        """Delete a user profile from the 'profiles' table."""
        response = supabase.table("profiles").delete().eq("id", profile_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return None
