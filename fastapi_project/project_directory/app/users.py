from fastapi import APIRouter, File, UploadFile
from cloudinary.uploader import upload

router = APIRouter()

@router.post("/upload-avatar/")
async def upload_avatar(file: UploadFile = File(...)):
    # Завантаження аватара на Cloudinary
    result = upload(file.file)
    avatar_url = result["secure_url"]
    return {"avatar_url": avatar_url}
