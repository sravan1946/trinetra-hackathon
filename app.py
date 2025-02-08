from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
import asyncio
from mangadex import Manga, Auth
import shutil
import os



async def download_manga(manga_id: str, format: str = "raw"):
    manga = Manga(auth=Auth())
    folder_name = manga.get_manga_list(ids=[manga_id],limit=1)[0].title
    process = await asyncio.create_subprocess_exec(
        "mangadex-dl", manga_id, "--path", "mangadex-dl_downloads", "-pbl", "stacked", "-f", format
    )
    await process.communicate()
    socketio.emit("download_complete", {"manga_id": manga_id})
    # convert the downloaded files to a zip file
    print(folder_name)
    shutil.make_archive(folder_name["en"], "zip", "mangadex-dl_downloads")

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=True)
