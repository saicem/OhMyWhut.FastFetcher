import os

import execjs

from src import config


def des3(username: str, password: str, lt: str) -> str:
    encode_js = open(f"{config.APP_FOLDER_PATH}/data/static/encode.js", "r", encoding="utf-8").read()
    # 加载 js 脚本
    ctx = execjs.compile(encode_js)
    # 执行 js 脚本的 strEnc 函数并传入参数
    res = ctx.call("strEnc", username + password + lt, "1", "2", "3")
    return res
