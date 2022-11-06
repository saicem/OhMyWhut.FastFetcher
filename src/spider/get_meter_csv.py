"""
@文件        :get_meter_csv.py
@Description :爬取所有电表的信息
@Date        :2022/10/10
@Author      :saicem
@version     :1.0
"""
from spider.campus_payment_platform import *

username = ""
password = ""


def write_meter_csv(cpp: CampusPaymentPlatform):
    """
    需要先运行 get_room_csv
    获取宿舍的电表信息
    """
    reader = open("room.csv", "r", encoding="utf-8")
    writer = open("meter.csv", "w", encoding="utf-8")
    writer.write("room_name,meter_id")

    reader.readline()
    for line in reader:
        (
            area_id,
            build_id,
            build_name,
            floor,
            room_id,
            room_name,
        ) = line.rstrip().split(",")
        meter_id = cpp.query_meter_id(room_id, FACTORY_CODE)
        print(f"{room_name}: {meter_id}")
        writer.write(f"\n{room_name},{meter_id}")


def write_room_csv(cpp: CampusPaymentPlatform):
    writer = open("room.csv", "w", encoding="utf-8")
    writer.write("area_id,build_id,build_name,floor,room_id,room_name")

    area_ids = [AREA_ID_东院, AREA_ID_西院, AREA_ID_南湖, AREA_ID_鉴湖, AREA_ID_余区]
    for area_id in area_ids:
        build_list = cpp.query_build_list(area_id, FACTORY_CODE)
        for build_id, build_name in build_list:
            floors = cpp.query_floor_list(area_id, build_id, FACTORY_CODE)
            for floor in floors:
                room_list = cpp.query_room_info(build_id, floor, FACTORY_CODE)
                for room_id, room_name in room_list:
                    print(f"{room_name}")
                    writer.write(
                        f"\n{area_id},{build_id},{build_name},{floor},{room_id},{room_name}"
                    )
    writer.close()


# 注意 未作并行处理 运行耗时巨长
if __name__ == "__main__":
    cpp = CampusPaymentPlatform()
    cpp.login(username, password)
    write_room_csv(cpp)
    write_meter_csv(cpp)
