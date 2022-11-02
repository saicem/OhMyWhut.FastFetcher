import os
import sys
from datetime import datetime

from PIL import ImageFont

TERM_START_DATE = datetime.date(datetime.strptime(os.environ.get("TERM_START_DATE", "2022-08-29"), "%Y-%m-%d"))
IMAGE_TTF = ImageFont.truetype(os.environ.get("COURSE_TTF", "../data/fonts/LXGWWenKaiMono-Regular.ttf"), 24)
USER_AGENT = os.environ.get("USER_AGENT", None)
APP_FOLDER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
