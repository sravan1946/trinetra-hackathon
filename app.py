import re
from flask import Flask
from flask import render_template, send_from_directory, request, redirect, url_for
from flask_socketio import SocketIO
import asyncio
from mangadex import Manga, Auth
import shutil
import os
import requests

COVER_FOLDER = "static/covers"  # Store images in 'static/covers'
IMAGE_FOLDER = "mangadex-dl_downloads"  # Path where images are stored
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def download_image(image_url, manga_id):
    """Download an image and save it locally."""
    if os.path.exists(os.path.join(COVER_FOLDER, f"{manga_id}.jpg")):
        return f"/cover/{manga_id}"
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(COVER_FOLDER, f"{manga_id}.jpg")
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return f"/cover/{manga_id}"
    return None


async def download_manga(manga_id: str, format: str = "raw"):
    manga = Manga(auth=Auth())
    folder_name = manga.get_manga_list(ids=[manga_id],limit=1)[0].title
    process = await asyncio.create_subprocess_exec(
        "mangadex-dl", manga_id, "--path", "mangadex-dl_downloads", "-pbl", "stacked", "-f", format
    )
    await process.communicate()
    socketio.emit("download_complete", {"manga_id": manga_id})
    print(folder_name)
    shutil.make_archive("mangadex-dl_downloads/" + folder_name["en"], "zip", "mangadex-dl_downloads/" + folder_name["en"])

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.post("/validate-manga/<string:manga_id>")
def validate_manga(manga_id):
    manga = Manga(auth=Auth())
    try:
        manga.get_manga_list(ids=[manga_id])
    except:
        return "Invalid manga ID"

    return "Valid"  # JS will use this to redirect

@app.post("/download/<string:manga_id>")
def download_manga_post(manga_id):
    # validate manga_id
    manga = Manga(auth=Auth())
    try:
        manga.get_manga_list(ids=[manga_id])
    except Exception:
        return "Invalid manga ID"
    return render_template("download.html", manga_id=manga_id, manga=manga)

@app.route("/download/<string:manga_id>")
def download(manga_id):
    from utils import get_manga_from_id, get_cover_url_from_id
    manga = get_manga_from_id(manga_id)
    download_image(get_cover_url_from_id(manga_id), manga_id)
    return render_template("download.html", manga_id=manga_id, manga=manga)

@app.route("/test/<string:manga_id>")
def test(manga_id):
    from utils import get_manga_from_id, get_cover_url_from_id
    manga = get_manga_from_id(manga_id)
    download_image(get_cover_url_from_id(manga_id), manga_id)
    return render_template("test.html", manga_id=manga_id, manga=manga)


@app.route("/cover/<manga_id>")
def serve_image(manga_id):
    """Serve the downloaded image."""
    return send_from_directory(COVER_FOLDER, f"{manga_id}.jpg")

if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=True, port=8000)

