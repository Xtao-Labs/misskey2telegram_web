import urllib.parse

from httpx import AsyncClient

client = AsyncClient()


async def get_auth(host: str, session: str):
    url = f"https://{host}/api/miauth/{session}/check"
    response = await client.post(url)
    return response.json()


def callback_url(username: str, host: str, back_host: str):
    return f"https://{back_host}/{username}/{host}"


def gen_url(username: str, host: str, back_host: str, session: str):
    return f"https://{host}/miauth/{session}?name=Misskey2Telegram&callback=" \
           f"{urllib.parse.quote(callback_url(username, host, back_host))}" \
           f"&permission=read:account,write:account,read:blocks,write:blocks,read:drive," \
           f"write:drive,read:favorites,write:favorites,read:following,write:following," \
           f"read:messaging,write:messaging,read:mutes,write:mutes,write:notes,read:notifications," \
           f"write:notifications,read:reactions,write:reactions,write:votes,read:pages," \
           f"write:pages,write:page-likes,read:page-likes,read:user-groups,write:user-groups," \
           f"read:channels,write:channels,read:gallery,write:gallery,read:gallery-likes," \
           f"write:gallery-likes"
