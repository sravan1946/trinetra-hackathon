from mangadex import Auth, Manga, Chapter
from pprint import pprint
from icecream import ic
from typing import Optional, Literal
import subprocess
import asyncio
from app import download_manga

asyncio.run(download_manga("5985d431-a60c-460c-8256-ddd0133d852f", "raw"))

auth = Auth()
manga = Manga(auth=auth)
search = manga.get_manga_list(title="solo leveling")
titles = [(manga.title, manga.manga_id) for manga in search]
chapter = Chapter(auth=auth)
pprint(titles)
# pprint(search[1])
chapter_list = chapter.get_chapter_list(manga=titles[1][1],limit=100,translatedLanguage=["en"],
                                        volume=[1], chapter=[1])
pprint(chapter_list)
print([chap.chapter for chap in chapter_list])
print(search[1].lastChapter)
print(search[1].lastVolume)

# setup subprocess and run the command mangadex-dl to download the file
subprocess.run(["mangadex-dl", search[0].manga_id, "--path", "mangadex-dl_downloads", "-pbl", "stacked"])


def get_manga_id_from_title(title: str) -> Optional[str]:
    manga = Manga(auth=auth)
    search = manga.get_manga_list(title=title)
    manga_id = [manga.manga_id for manga in search if manga.lastChapter is not None and manga.lastVolume is not None]
    return manga_id[0] if manga_id else None

def get_manga_from_id(manga_id: str) -> Optional[Manga]:
    manga = Manga(auth=auth)
    search = manga.get_manga_list(ids=[manga_id])
    return search[0] if search else None


VALID_FORMATS = Literal["raw","raw-volume","tachiyomi","pdf","pdf-volume"]
