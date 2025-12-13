from fastapi import HTTPException, UploadFile
from dependencies.supabase_client import supabase
from services.supabase_storage_service import SupabaseStorageService
from schemas.item_schema import ItemCreateRequest


class ItemService:
    def __init__(self):
        self.supabase_storage = SupabaseStorageService()

    async def create_item(self, item: ItemCreateRequest, img: UploadFile):
        """Create a new item in the 'items' table."""
        data = item.model_dump()

        filename = f"{data['user_id']}-{data['name']}"

        await self.supabase_storage.save_file(img, "private_uploads", filename, "items")

        img_url = await self.supabase_storage.create_signed_url(
            3600,
            filename,
            "items",
        )
        data["img_url"] = img_url

        response = supabase.table("items").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create item")
        return None

    async def read_item():
        pass

    async def update_item():
        pass

    async def delete_item():
        pass
