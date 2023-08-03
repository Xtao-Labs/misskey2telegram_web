import io
import traceback
import uuid
import PIL.Image
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.responses import RedirectResponse, StreamingResponse

from utils import gen_url, get_auth

app = FastAPI()
with open("default.jpg", "rb") as f:
    default_jpg = io.BytesIO(f.read())


@app.get('/gen')
async def gen(
    *,
    username: str,
    host: str,
    back_host: str,
):
    session = str(uuid.uuid4())
    return RedirectResponse(gen_url(username, host, back_host, session))


@app.get('/1.jpg')
async def jpg(
    *,
    url: str,
) -> StreamingResponse:
    if "/proxy/avatar" not in url:
        return StreamingResponse(default_jpg, media_type="image/jpg")
    url = url.replace("/proxy/avatar.webp", "/proxy/avatar.png")
    # jpg png webp gif to jpg
    try:
        async with AsyncClient() as client:
            print(f"get jpg {url}")
            r = await client.get(url)
            remote = PIL.Image.open(io.BytesIO(r.content))
            remote = remote.convert("RGB")
            file_like = io.BytesIO()
            remote.save(file_like, "jpeg")
            file_like.seek(0)
            return StreamingResponse(file_like, media_type="image/jpg")
    except Exception:
        traceback.print_exc()
        return StreamingResponse(default_jpg, media_type="image/jpg")


@app.get("/{username}/{host}")
async def back_to_telegram(
    *,
    username: str,
    host: str,
    session: str,
):
    data = await get_auth(host, session)
    if data.get("ok", False):
        return RedirectResponse(f"https://t.me/{username}?start={data['token']}")
    else:
        return data
