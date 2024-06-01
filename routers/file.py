import os

from fastapi import File, UploadFile, APIRouter, HTTPException, Depends
import shutil
from config import IMAGE_PATH, MUSIC_PATH

import hashlib
from random import random

from PIL import Image
import ffmpeg

from database.models import UserTable
from routers.user import fastapi_users

from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse


async def _encrypt_string(string):
    string = string + str(random())
    hashed_string = hashlib.shake_256(string.encode('utf-8')).hexdigest(32)
    return hashed_string


async def _create_file_path(file_name, directory):
    hashed_file_name = await _encrypt_string(file_name)
    return directory + '/' + hashed_file_name + "." + file_name.split(".")[1]


current_user = fastapi_users.current_user()

router = APIRouter(
    prefix='/file',
    tags=['File']
)

image_types = ['jpg', 'jpeg', 'png']


@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...), user: UserTable = Depends(current_user)):
    if file.filename.split(".")[1] not in image_types:
        raise HTTPException(status_code=415, detail="This image is Unsupported Media Type")
    try:

        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        new_name = file.filename.split('.')[0] + ".jpg"
        file_path = await _create_file_path(new_name, IMAGE_PATH)
        Image.open(file.filename).convert("RGB").save(file_path)

    except Exception as e:
        print(e)
        return {"responce": "error",
                "message": "There was an error uploading the file"}
    finally:
        file.file.close()
        os.remove(file.filename)

    return {"responce": "ok",
            "message": f"{file_path.split("/")[-1]}"}


audio_types = ['wav', 'mp3', 'aac', 'aiff']


@router.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...), user: UserTable = Depends(current_user)):
    if file.filename.split('.')[1] not in audio_types:
        raise HTTPException(status_code=415, detail="This audio is Unsupported Media Type")
    try:
        hashed_file_name = await _encrypt_string(file.filename)
        with open(hashed_file_name, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        new_name = hashed_file_name + ".mp3"
        file_path = await _create_file_path(new_name, MUSIC_PATH)
        ffmpeg.input(hashed_file_name).output(new_name).run()
        shutil.copyfile(new_name, file_path)

    except Exception as e:
        print(e)
        return {"responce": "error",
                "message": "There was an error uploading the file"}
    finally:
        file.file.close()
        os.remove(hashed_file_name)
        os.remove(new_name)

    return {"responce": "ok",
            "message": f"{file_path.split("/")[-1]}"}


@router.get("/image/{image_file}", response_class=FileResponse)
async def get_image_file(image_file: str):
    path = IMAGE_PATH + image_file
    return FileResponse(path=path)

@router.get("/audio/{audio_file}", response_class=StreamingResponse)
async def get_audio_file_stream(audio_file: str):
    def iterfile():
        with open(MUSIC_PATH + audio_file , mode="rb") as file_like:  #
            yield from file_like  #

    return StreamingResponse(iterfile(), media_type="audio/mp3")
