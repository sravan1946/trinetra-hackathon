from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
import asyncio



async def download_manga(manga_id: str, format: str = "raw"):
    process = await asyncio.create_subprocess_exec(
        "mangadex-dl", manga_id, "--path", "mangadex-dl_downloads", "-pbl", "stacked", "-f", format
    )
    await process.communicate()
    socketio.emit("download_complete", {"manga_id": manga_id})

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, debug=True)
