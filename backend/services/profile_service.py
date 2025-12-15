import math
from fastapi import HTTPException, UploadFile
from dependencies.supabase_client import supabase
from services.supabase_storage_service import SupabaseStorageService
from schemas.profile_schema import ProfileCreateRequest, ProfileUpdateRequest
from settings import settings


class ProfileService:
    def __init__(self):
        self.supabase_storage = SupabaseStorageService()

    async def create_profile(
        self, profile: ProfileCreateRequest, pfp: UploadFile | None
    ):
        """Create a new user profile in the 'profiles' table."""
        # Check if profile with same id exists
        existing = supabase.table("profiles").select("*").eq("id", profile.id).execute()
        if existing.data:
            raise HTTPException(
                status_code=409, detail=f"Profile with id {profile.id} already exists"
            )

        # Check if profile with same username exists
        existing = (
            supabase.table("profiles")
            .select("*")
            .eq("username", profile.username)
            .execute()
        )
        if existing.data:
            raise HTTPException(
                status_code=409,
                detail=f"Profile with username {profile.username} already exists",
            )

        data = profile.model_dump()

        if pfp:
            pfp_filename = f"{profile.id}-pfp"
            pfp_url = await self.save_pfp(pfp, pfp_filename)
            data["pfp_url"] = pfp_url
        else:
            data["pfp_url"] = settings.default_pfp_url
        response = supabase.table("profiles").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create profile")
        return None

    async def read_profiles(
        self,
        username: str | None = None,
        page: int = 1,
        limit: int = 20,
    ):
        """
        Read profiles from the 'profiles' table.
        Supports optional username filtering and pagination.
        """
        query = supabase.table("profiles").select("*", count="exact")

        # Optional username filter (prefix match)
        if username:
            query = query.ilike("username", f"{username}%")

        # Pagination safety
        page = max(page, 1)
        offset = (page - 1) * limit

        query = query.range(offset, offset + limit - 1)

        response = query.execute()

        total = response.count or 0

        if total == 0:
            raise HTTPException(status_code=404, detail="No profiles found")

        total_pages = math.ceil(total / limit)

        return {
            "data": response.data,
            "meta": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
            },
        }

    async def read_profile_by_id(self, profile_id: str):
        response = (
            supabase.table("profiles")
            .select("*")
            .eq("id", profile_id)
            .single()
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="No profiles found")
        return response.data

    async def update_profile(
        self, profile_id: str, profile: ProfileUpdateRequest, pfp: UploadFile | None
    ):
        """Update an existing user profile in the 'profiles' table."""
        # Check profile exists
        existing = supabase.table("profiles").select("*").eq("id", profile_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Profile not found")

        data = {k: v for k, v in profile.model_dump().items() if v is not None}
        # If username is being updataed check its not taken
        if "username" in data:
            username_check = (
                supabase.table("profiles")
                .select("*")
                .eq("username", data["username"])
                .execute()
            )
            # Make sure it's not the current user's profile
            if username_check.data and username_check.data[0]["id"] != profile_id:
                raise HTTPException(
                    status_code=409,
                    detail=f"Profile with username {data['username']} already exists",
                )

        if pfp:
            pfp_filename = f"{profile_id}-pfp"
            pfp_url = await self.save_pfp(pfp, pfp_filename)
            data["pfp_url"] = pfp_url
        if not data:
            return None
        # Update profile
        response = (
            supabase.table("profiles").update(data).eq("id", profile_id).execute()
        )
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to update profile")
        return None

    async def delete_profile(self, profile_id: str):
        """Delete a user profile from the 'profiles' table."""
        existing = supabase.table("profiles").select("*").eq("id", profile_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Profile not found")

        profile_data = existing.data[0]
        pfp_url = profile_data.get("pfp_url")

        # Delete the profile from the database
        response = supabase.table("profiles").delete().eq("id", profile_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Delete the pfp from storage if it's not the default pfp
        if pfp_url and pfp_url != settings.default_pfp_url:
            await self.supabase_storage.delete_file(
                f"{profile_id}-pfp", "public_uploads", "pfps"
            )

        return None

    async def save_pfp(self, pfp: UploadFile, filename: str):
        await self.supabase_storage.save_file(
            file=pfp,
            bucket="public_uploads",
            filename=filename,
            folder="pfps",
        )

        return await self.supabase_storage.get_public_url(
            filename=filename,
            folder="pfps",
        )
