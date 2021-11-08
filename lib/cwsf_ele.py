from requests import Session
from requests.sessions import session


class Cwsf:
    __factorycode: str = "E035"
    __factorycode_yu: str = "E023"
    # 这个好像是余区的意思
    __area_yu: str = "9004"
    __session: Session

    def __init__(self, cur_session: Session = session()) -> None:
        self.__session = cur_session

    def getAreaInfo(self) -> str:
        url = "http://cwsf.whut.edu.cn/getAreaInfo"
        data = {"factorycode": self.__factorycode}
        res = self.__session.post(url, data)
        return res.text

    def queryBuildList(
        self,
        areaid: str,
    ) -> str:
        url = "http://cwsf.whut.edu.cn/queryBuildList"
        data = {"areaid": areaid, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text

    # 马区
    def queryFloorListMa(
        self,
        areaid: str,
        buildid: str,
    ) -> str:
        url = "http://cwsf.whut.edu.cn/queryFloorList"
        data = {"areaid": areaid, "buildid": buildid, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text

    def getRoomInfo(
        self,
        buildid: str,
        floorid: str,
    ) -> str:
        url = "http://cwsf.whut.edu.cn/getRoomInfo"
        data = {
            "buildid": buildid,
            "floorid": floorid,
            "factorycode": self.__factorycode,
        }
        res = self.__session.post(url, data=data)
        return res.text

    def queryRoomElec(
        self,
        roomid: str,
    ) -> str:
        url = "http://cwsf.whut.edu.cn/queryRoomElec"
        data = {"roomid": roomid, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text

    def queryReserve(
        self,
        meterId: str,
    ) -> str:
        url = "http://cwsf.whut.edu.cn/queryReserve"
        data = {"meterId": meterId, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text

    # -------------------------------------------------------------------------------------

    # 余区
    # 这个的 factorycode 不一样
    def queryFloorListYu(self, area_id: str) -> str:
        url = "http://cwsf.whut.edu.cn/queryFloorsList"
        data = {
            "Area_ID": area_id,
            "factorycode": self.__factorycode_yu,
            "area": self.__area_yu,
        }
        res = self.__session.post(url, data=data)
        return res.text

    # 余区
    def queryRoomListYu(self, floor: str, architecture_id: str) -> str:
        url = "http://cwsf.whut.edu.cn/queryRoomList"
        data = {
            "floor": floor,
            "ArchitectureID": architecture_id,
            "factorycode": self.__factorycode_yu,
            "area": self.__area_yu,
        }
        res = self.__session.post(url, data=data)
        return res.text

    def querySydl(self, roomno: str) -> str:
        url = "http://cwsf.whut.edu.cn/querySydl"
        data = {
            "roomno": roomno,
            "factorycode": self.__factorycode_yu,
            "area": self.__area_yu,
        }
        res = self.__session.post(url, data=data)
        return res.text
