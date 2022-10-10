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

# 需要注意 运行耗时巨长
if __name__ == "__main__":
    cpp = CampusPaymentPlatform()
    cpp.login(username, password)

    # 需要先运行 get_room_csv
    reader = open("room.csv", "r", encoding='utf-8')
    writer = open("meter.csv", "w", encoding='utf-8')
    writer.write("room_name,meter_id")

    reader.readline()
    for line in reader:
        (area_id, build_id, build_name, floor, room_id, room_name) = line.rstrip().split(',')
        meter_id = cpp.query_meter_id(room_id, FACTORY_CODE)
        print(f"{room_name}: {meter_id}")
        writer.write(f"\n{room_name},{meter_id}")
