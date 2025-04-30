import pathlib
import os

APP_FOLDER = pathlib.Path(__file__).parent.resolve().name
print("App folder is", APP_FOLDER)
UPLOAD_FOLDER = os.path.abspath(os.path.join(APP_FOLDER, "uploads"))

print("UPLOAD FOLDER", UPLOAD_FOLDER)

from tools_app.routes import *
