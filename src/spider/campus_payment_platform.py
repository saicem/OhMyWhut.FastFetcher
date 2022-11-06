from requests import Session

from services.ias import Ias

FACTORY_CODE = "E035"
AREA_ID_东院 = "0001"
AREA_ID_西院 = "0002"
AREA_ID_南湖 = "0003"
AREA_ID_鉴湖 = "0004"
AREA_ID_余区 = "0005"


class CampusPaymentPlatform:
    """
    校园缴费平台
    """

    def __init__(self):
        self.session: Session = None
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "proxy-connection": "keep-alive",
            "x-requested-with": "XMLHttpRequest",
        }

    def login(self, username: str, password: str):
        ias = Ias(username, password)
        if not ias.login():
            print("账密错误")
            exit()
        self.session = ias.session
        res = self.session.get("http://cwsf.whut.edu.cn/casLogin")
        if not res.url.startswith("http://cwsf.whut.edu.cn/showPublic"):
            print("登录失败")
            exit()

    def query_area_info(self, factory_code: str) -> list[tuple[str, str]]:
        """
        获取地区信息
        :param factory_code: 固定 E035
        :return: (area_id, area_name)
        """
        url = "http://cwsf.whut.edu.cn/getAreaInfo"
        data = f"factorycode={factory_code}"
        res = self.session.post(url=url, headers=self.headers, data=data)
        area_list = res.json()["areaList"]
        return [item.split("@") for item in area_list]

    def query_build_list(
            self, area_id: str, factory_code: str
    ) -> list[tuple[str, str]]:
        """
        获取建筑信息
        :param area_id: 从 get_area_info 获取
        :param factory_code: 固定 E035
        :return: 建筑信息 000004@东1舍（原东院一公寓1）
        """
        url = "http://cwsf.whut.edu.cn/queryBuildList"
        data = f"areaid={area_id}&factorycode={factory_code}"
        res = self.session.post(url=url, headers=self.headers, data=data)
        build_list = res.json()["buildList"]
        return [item.split("@") for item in build_list]

    def query_floor_list(
            self, area_id: str, build_id: str, factory_code: str
    ) -> list[int]:
        """
        获取楼层信息
        :param factory_code: 固定 E035
        :param build_id: 从 query_build_list 获取
        :param area_id: 从 get_area_info 获取
        :return: 楼层信息
        """
        url = "http://cwsf.whut.edu.cn/queryFloorList"
        data = f"areaid={area_id}&buildid={build_id}&factorycode={factory_code}"
        res = self.session.post(url=url, headers=self.headers, data=data)
        floor_list = res.json()["floorList"]
        return floor_list

    def query_room_info(
            self, build_id: str, floor: int, factory_code: str
    ) -> list[tuple[str, str]]:
        """
        获取楼层有多少宿舍的信息
        :param build_id: 从 query_build_list 获取
        :param floor: 从 query_floor_list 获取
        :param factory_code: 固定 E035
        :return: 宿舍信息 例如：[("00000260", "东12舍-101"), ...]
        """
        url = "http://cwsf.whut.edu.cn/getRoomInfo"
        data = f"buildid={build_id}&floorid={floor}&factorycode={factory_code}"
        res = self.session.post(url=url, headers=self.headers, data=data)
        room_list = res.json()["roomList"]
        return [item.split("@") for item in room_list]

    def query_meter_id(self, room_id: str, factory_code: str) -> str:
        """
        获取这个宿舍的电表信息
        :param room_id: 从 get_room_info 获取
        :param factory_code: 固定 E035
        :return: meterId
        """
        url = "http://cwsf.whut.edu.cn/queryRoomElec"
        data = f"roomid={room_id}&factorycode={factory_code}"
        res = self.session.post(url=url, headers=self.headers, data=data)
        meter_id = res.json()["meterId"]
        return meter_id
