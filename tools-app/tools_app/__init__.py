import pathlib
import os

APP_FOLDER = pathlib.Path(__file__).parent.resolve().name
UPLOAD_FOLDER = os.path.abspath(os.path.join(APP_FOLDER, "uploads"))
MEDIA_BACKUP_PATH = os.environ.get("MEDIA_BACKUP_PATH", "/tmp/iphone_backup")

from tools_app.routes import *
