from mangadex import Auth, Manga, Cover
from pprint import pprint
from icecream import ic
from typing import Optional, Literal
import asyncio
from app import download_manga

# asyncio.run(download_manga("5985d431-a60c-460c-8256-ddd0133d852f", "pdf"))



def get_manga_id_from_title(title: str) -> Optional[str]:
    manga = Manga(auth=Auth())
    search = manga.get_manga_list(title=title)
    manga_id = [manga.manga_id for manga in search if manga.lastChapter is not None and manga.lastVolume is not None]
    return manga_id[0] if manga_id else None

def get_manga_from_id(manga_id: str) -> Optional[Manga]:
    manga = Manga(auth=Auth())
    search = manga.get_manga_list(ids=[manga_id])
    return search[0] if search else None

def get_cover_url_from_id(manga_id: str) -> Optional[str]:
    cover = Cover(auth=Auth())
    manga = get_manga_from_id(manga_id)
    search = cover.get_cover_url(manga.cover_id)
    print(search)
    return search if search else None


VALID_FORMATS = Literal["raw","raw-volume","pdf","pdf-volume"]
