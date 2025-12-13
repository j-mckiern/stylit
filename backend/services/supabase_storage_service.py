from fastapi import HTTPException, UploadFile
from dependencies.supabase_client import supabase


class SupabaseStorageService:
    def __init__(self):
        pass

    def _build_path(self, filename: str, folder: str | None = None) -> str:
        if folder:
            return f"{folder}/{filename}"
        return filename

    async def save_file(
        self, file: UploadFile, bucket: str, filename: str, folder: str | None = None
    ):
        file_path = self._build_path(filename, folder)
        file_content = await file.read()

        try:
            supabase.storage.from_(bucket).upload(
                file_path,
                file_content,
                file_options={"content-type": file.content_type, "upsert": "true"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to upload file: {str(e)}"
            )
        return

    async def create_signed_url(
        self, expires_in: int, filename: str, folder: str | None = None
    ):
        file_path = self._build_path(filename, folder)

        signed_url = supabase.storage.from_("private_uploads").create_signed_url(
            file_path, expires_in
        )
        return signed_url["signedUrl"]

    async def get_public_url(self, filename: str, folder: str | None = None):
        file_path = self._build_path(filename, folder)

        try:
            public_url = supabase.storage.from_("public_uploads").get_public_url(
                file_path
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get pfp: {str(e)}")

        return public_url

    async def delete_file(self, filename: str, bucket: str, folder: str | None = None):
        file_path = self._build_path(filename, folder)
        try:
            supabase.storage.from_(bucket).remove(file_path)
        except Exception as e:
            # Log the error but don't fail the deletion
            print(f"Warning: Failed to delete file {filename}: {str(e)}")
