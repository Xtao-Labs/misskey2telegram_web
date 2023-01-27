import uuid
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from utils import gen_url, get_auth

app = FastAPI()


@app.get('/gen')
async def gen(
    *,
    username: str,
    host: str,
    back_host: str,
):
    session = str(uuid.uuid4())
    return RedirectResponse(gen_url(username, host, back_host, session))


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
