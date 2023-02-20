import os
from datetime import datetime

from PIL import ImageFont

TERM_START_DATE = datetime.date(
    datetime.strptime(os.environ.get("TERM_START_DATE", "2023-02-20"), "%Y-%m-%d")
)
IMAGE_TTF = ImageFont.truetype(
    os.environ.get("COURSE_TTF", "../data/fonts/LXGWWenKaiMono-Regular.ttf"), 24
)
USER_AGENT = os.environ.get("USER_AGENT", None)
APP_FOLDER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_VERSION = os.environ.get("APP_VERSION", "unknown")
