"""
@文件        :get_meter_csv2.py
@Description :爬取余区的所有电表数据
@Date        :2021/11/08 00:03:43
@Author      :saicem
@version     :1.0
"""
import requests
import json
from lib.cwsf_ele import Cwsf
from lib import zhlgd

# TODO 在这里设置用户名和密码
username = ""
password = ""


def login2cwsf() -> Cwsf:
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


# 获取余区的楼栋信息
def get_floor_list(cwsf: Cwsf, area_id: str, area: str):
    res_json = json.loads(cwsf.queryFloorListYu(area_id, area))
    if not res_json.__contains__("buildinglist"):
        raise Exception("得到了错误的JSON:{}".format(res_json))
    return res_json["buildinglist"]


# 生成余区宿舍信息的csv
def make_csv_room_yu_core():
    # 只选取学生宿舍 所以该参数是固定的
    area_id: str = "1"
    # 登录
    cwsf = login2cwsf()
    # 获取楼栋列表信息 生成 csv
    build_list = get_floor_list(cwsf, area_id)
    for build in build_list:
        architecture_name = build["ArchitectureName"]
        architecture_id = build["ArchitectureID"]
        architecture_begin = build["ArchitectureBegin"]
        architecture_storys = build["ArchitectureStorys"]
        for floor in range(int(architecture_begin), int(architecture_storys) + 1):
            room_list = json.loads(cwsf.queryRoomListYu(floor, architecture_id))[
                "roomlist"
            ]
            for room in room_list:
                open("room_yu.csv", "a", encoding="utf8").write(
                    "{},{},{}\n".format(
                        architecture_name,
                        room["RoomName"],
                        room["AmMeter_ID"],
                    )
                )


# 需要注意 运行耗时巨长
if __name__ == "__main__":
    make_csv_room_yu_core()
