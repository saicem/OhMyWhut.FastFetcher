from requests.sessions import Session
import requests
import json
import time
from lib.cwsf_ele import Cwsf
from lib import zhlgd

# TODO 在这里设置用户名和密码
username = ""
password = ""


def login2cwsf(cur_session: Session, username: str, password: str) -> bool:
    jsessionid, lt = zhlgd.cas_login(cur_session)
    text = zhlgd.post_cas_login(username, password, jsessionid, lt, cur_session)
    return text != None


def get_area_list(cwsf: Cwsf) -> list[str]:
    res_json = json.loads(cwsf.getAreaInfo())["areaList"]
    return res_json


def get_build_list(cwsf: Cwsf, area: str) -> list[str]:
    if area == None:
        return None
    area_id = area.split("@")[0]
    res_json = json.loads(cwsf.queryBuildList(area_id))
    if not res_json.__contains__("buildList"):
        print(res_json)
        return None
    return res_json["buildList"]


def get_floor_list(cwsf: Cwsf, area: str, build: str) -> list[str]:
    if area == None or build == None:
        return None
    area_id = area.split("@")[0]
    build_id = build.split("@")[0]
    res_json = json.loads(cwsf.queryFloorList(area_id, build_id))
    if not res_json.__contains__("floorList"):
        print(res_json)
        return None
    return res_json["floorList"]


def get_room_list(cwsf: Cwsf, build: str, floor_id: str):
    if build == None or floor_id == None:
        return None
    build_id = build.split("@")[0]
    res_json = json.loads(cwsf.getRoomInfo(build_id, floor_id))
    if not res_json.__contains__("roomList"):
        print(res_json)
        return None
    return res_json["roomList"]


# 获取寝室列表 使用 json 会转为 unicode 编码
def make_room_csv(cwsf):
    index = 0
    base_list = []
    area_list = get_area_list(cwsf)
    for area in area_list:
        build_list = get_build_list(cwsf, area)
        for build in build_list:
            floor_list = get_floor_list(cwsf, area, build)
            for floor_id in floor_list:
                room_list = get_room_list(cwsf, build, floor_id)
                for room in room_list:
                    base_list.append([index, area, build, floor_id, room])
                    index += 1
                    str_form = "{},{},{},{}".format(index, area, build, room)
                    print(str_form)
                    open("room.csv", "a", encoding="utf8").write(str_form + "\n")
                time.sleep(0.2)
    return base_list

# 将数据写入 meter_room.csv
def write_meter_room(room_name: str, meter_id: str):
    if meter_id != None:
        open("meter_room.csv", "a", encoding="utf8").write(
            "{},{}\n".format(room_name, meter_id)
        )
    else:
        open("meter_room.csv", "a", encoding="utf8").write(
            "{},{}\n".format(room_name, "None")
        )

# 生成 room.csv 以便下一步处理
def make_room_csv_core():
    # 获取 cookie
    cur_session = requests.session()
    if not login2cwsf(cur_session, username, password):
        print("查询失败")
        exit()
    cwsf = Cwsf(cur_session=cur_session)
    # 获取所有寝室
    make_room_csv(cwsf)

# 读取 room.csv 生成 meter_room.csv
def make_meter_csv_core():
    cur_session = requests.session()
    if not login2cwsf(cur_session, username, password):
        print("查询失败")
        exit()
    cwsf = Cwsf(cur_session=cur_session)

    rooms = open("room.csv", "r", encoding="utf8")
    for line in rooms:
        room = line.strip("\n").split(",")[3]
        room_id, room_name = room.split("@")
        res_json = json.loads(cwsf.queryRoomElec(room_id))
        if res_json.__contains__("meterId"):
            meter_id = res_json["meterId"]
        else:
            meter_id = None
        write_meter_room(room_name, meter_id)

# 需要注意 运行耗时巨长
# if __name__ == "__main__":
#     make_room_csv_core()
#     make_meter_csv_core()

