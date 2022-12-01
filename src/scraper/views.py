import asyncio
from typing import List
from pathlib import Path, PosixPath

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from fastapi.responses import Response
from fastapi.routing import APIRouter

from src.config import BASE_DIR, NAVER_HEADERS


BASE_URL = "https://bjpublic.tistory.com/category/%EC%A0%84%EC%B2%B4%20%EC%B6%9C%EA%B0%84%20%EB%8F%84%EC%84%9C"


scraper_router = APIRouter()


@scraper_router.get(path="/naver")
async def get_from_naver(
    q: str | None = None, display: int = 10, start: int = 1, sort: str = "sim"
):
    import os

    print(f"main stream pid: {os.getpid()}")
    headers = NAVER_HEADERS
    if q is None:
        return Response(content="No search keyword", status_code=400)
    url = f"https://openapi.naver.com/v1/search/image?query={q}&display={display}&start={start}&sort={sort}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                res = await response.json()
                links = [item["link"] for item in res["items"]]
                if links:
                    import time

                    s = time.time()
                    await asyncio.gather(
                        *[img_downloader(session, link=link, route=q) for link in links]
                    )
                    print(f"img download total excute time: {time.time()-s}")
                return res
            message = await response.text()
            return Response(message, status_code=response.status)


async def img_downloader(session: aiohttp.ClientSession, link: str, route: str) -> None:
    import os
    import time

    print(f"fetcher pid: {os.getpid()}")
    s = time.time()
    print(f"start at@ {s}")
    if not route:
        raise ValueError("route in needed for downloading images")
    img_base_dir: PosixPath = BASE_DIR / "media"
    img_dir = mk_img_dir(img_base_dir, route)
    img_name: str = refine_image_name_from_link(link)

    async with session.get(link) as res:
        # Early return
        if res.status != 200:
            return None

        async with aiofiles.open(img_dir / img_name, mode="wb") as file:
            data: bytes = await res.read()
            await file.write(data)
    e = time.time()
    print(f"ends at@ {e}")
    print(f"excution time: {e-s}")


def mk_img_dir(img_base_dir: PosixPath, route: str) -> PosixPath:
    img_dir = Path(img_base_dir / route)

    if not img_dir.exists():
        img_dir.mkdir()

    return img_dir


def refine_image_name_from_link(link: str) -> str:
    img_name = link.rsplit("/", maxsplit=1)[-1]

    if "?" in img_name:
        img_name: str = img_name.split("?")[0]
    if "jpg" not in img_name:
        img_name: str = img_name + ".jpg"

    return img_name


@scraper_router.get(path="/html")
async def get_title():
    return await html_scraper()


async def html_scraper():
    urls = [f"{BASE_URL}?page={i}" for i in range(1, 10)]

    async with aiohttp.ClientSession() as session:
        res = await asyncio.gather(*[html_fetcher(session, url) for url in urls])

    return res


async def html_fetcher(session: aiohttp.ClientSession, url: str) -> None:
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        cont_thumb = soup.find_all("div", "cont_thumb")

        titles: List[str] = [
            cont.find("p", "txt_thumb")
            .text.replace("</p>", "")
            .replace('<p class="txt_thumb">', "")
            for cont in cont_thumb
            if cont.find("p", "txt_thumb") is not None
        ]

        return titles
