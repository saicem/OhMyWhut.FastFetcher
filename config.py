import os
from datetime import datetime

from PIL import ImageFont

TERM_START_DAY = datetime.date(datetime.strptime(os.environ.get("TERM_START_DATE", "2022-08-29"), "%Y-%m-%d"))
IMAGE_TTF = ImageFont.truetype(os.environ.get("COURSE_TTF", "LXGWWenKaiMono-Regular.ttf"), 24)
USER_AGENT = os.environ.get("USER_AGENT", None)
