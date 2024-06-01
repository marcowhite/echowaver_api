from fastapi import APIRouter, WebSocket, Depends
from database.models import UserTable
from routers.song import get_song_by_id
from routers.user import fastapi_users
from pydub import AudioSegment
from pydub.utils import make_chunks

current_user = fastapi_users.current_user()

CHUNK = 1024

router = APIRouter(
    prefix='/ws',
    tags=['Websockets']
)

@router.websocket("/song/{id}")
async def audio_stream(websocket: WebSocket,
                       id: int,
                       user: UserTable = Depends(current_user)):
    await websocket.accept()
    song = await get_song_by_id(id, user)

    path = 'data/music/' + song.audio_file

    try:
        audio = AudioSegment.from_mp3(path)

        chunks = make_chunks(audio, CHUNK)

        for chunk in chunks:
            await websocket.send_bytes(chunk.raw_data)

    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        await websocket.close()