import shutil

from fastapi import APIRouter, BackgroundTasks, UploadFile

from services.images import ImagesService
from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_images(file, background_tasks)
