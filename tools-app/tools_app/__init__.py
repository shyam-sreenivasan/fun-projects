import pathlib
import os

APP_FOLDER = pathlib.Path(__file__).parent.resolve().name
UPLOAD_FOLDER = os.environ.get('MYTOOLS_UPLOADS_FOLDER', "/tmp/uploads")
MEDIA_BACKUP_PATH = os.environ.get("MYTOOLS_MEDIA_BACKUP_PATH", "/tmp/mytools_backup")

from tools_app.routes import *
