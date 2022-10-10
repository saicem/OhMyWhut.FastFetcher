"""
@文件        :get_meter_csv1.py
@Description :爬取马房山校区的所有电表数据
@Date        :2021/11/08 00:02:56
@Author      :saicem
@version     :1.0
"""
from requests.sessions import Session
import requests
import json
import time
from lib.cwsf_ele import Cwsf
from lib import ias

# TODO 在这里设置用户名和密码
username = ""
password = ""


def login2cwsf(cur_session: Session, username: str, password: str) -> Cwsf:
    if len(username) == 0 or len(password) == 0:
        print("请先填写学号密码")
        exit()
    cur_session = requests.session()
    jsessionid, lt = zhlgd.cwsfCasLogin(cur_session)
    text = zhlgd.loginCwsf(username, password, jsessionid, lt, cur_session)
    if text == None:
        print("登录失败")
        exit()
    cwsf = Cwsf(cur_session=cur_session)
    return cwsf


def getAreaList(cwsf: Cwsf) -> list[str]:
    res_json = json.loads(cwsf.getAreaInfo())["areaList"]
    return res_json


def getBuildList(cwsf: Cwsf, area: str) -> list[str]:
    if area == None:
        return None
    area_id = area.split("@")[0]
    res_json = json.loads(cwsf.queryBuildList(area_id))
    if not res_json.__contains__("buildList"):
        print(res_json)
        return None
    return res_json["buildList"]


def getFloorList(cwsf: Cwsf, area: str, build: str) -> list[str]:
    if area == None or build == None:
        return None
    area_id = area.split("@")[0]
    build_id = build.split("@")[0]
    res_json = json.loads(cwsf.queryFloorListMa(area_id, build_id))
    if not res_json.__contains__("floorList"):
        print(res_json)
        return None
    return res_json["floorList"]


def getRoomList(cwsf: Cwsf, build: str, floor_id: str):
    if build == None or floor_id == None:
        return None
    build_id = build.split("@")[0]
    res_json = json.loads(cwsf.getRoomInfo(build_id, floor_id))
    if not res_json.__contains__("roomList"):
        print(res_json)
        return None
    return res_json["roomList"]


# 获取寝室列表 使用 json 会转为 unicode 编码
def makeRoomCsv(cwsf):
    index = 0
    area_list = getAreaList(cwsf)
    for area in area_list:
        build_list = getBuildList(cwsf, area)
        for build in build_list:
            floor_list = getFloorList(cwsf, area, build)
            for floor_id in floor_list:
                room_list = getRoomList(cwsf, build, floor_id)
                for room in room_list:
                    index += 1
                    str_form = "{},{},{},{}\n".format(index, area, build, room)
                    print(str_form, end="")
                    open("room.csv", "a", encoding="utf8").write(str_form)
                time.sleep(0.2)


# 将数据写入 meter.csv
def writeMeter(room_name: str, meter_id: str):
    if meter_id != None:
        open("meter.csv", "a", encoding="utf8").write(
            "{},{}\n".format(room_name, meter_id)
        )
    else:
        open("meter.csv", "a", encoding="utf8").write(
            "{},{}\n".format(room_name, "None")
        )


# 生成 room.csv 以便下一步处理
def makeRoomCsvCore():
    cwsf = login2cwsf()
    # 获取所有寝室
    makeRoomCsv(cwsf)


# 读取 room.csv 生成 meter.csv
def makeMeterCsvCore():
    cwsf = login2cwsf()
    rooms = open("room.csv", "r", encoding="utf8")
    for line in rooms:
        room = line.strip("\n").split(",")[3]
        room_id, room_name = room.split("@")
        res_json = json.loads(cwsf.queryRoomElec(room_id))
        time.sleep(0.2)
        if res_json.__contains__("meterId"):
            meter_id = res_json["meterId"]
        else:
            meter_id = None
        writeMeter(room_name, meter_id)


# 需要注意 运行耗时巨长
if __name__ == "__main__":
    makeRoomCsvCore()
    makeMeterCsvCore()
