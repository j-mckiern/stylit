from fastapi import APIRouter, File, Form, UploadFile
from schemas.item_schema import ItemCreateRequest
from services.item_service import ItemService


router = APIRouter(prefix="/items", tags=["Items"])

service = ItemService()


@router.post("/", summary="Create user item", status_code=201)
async def create_profile(
    user_id: str = Form(...),
    name: str = Form(...),
    category: str = Form(...),
    style: str = Form(...),
    season: str = Form(...),
    color: str = Form(...),
    visibility: str = Form(...),
    img: UploadFile = File(...),
):
    """
    Create item in the 'items' table.
    """
    item = ItemCreateRequest(
        user_id=user_id,
        name=name,
        category=category,
        style=style,
        season=season,
        color=color,
        visibility=visibility,
    )
    response = await service.create_item(item, img)
    return response
