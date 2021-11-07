from requests import Session
from requests.sessions import session


class Cwsf:
    __factorycode: str = "E035"
    __session: Session

    def __init__(self, cur_session: Session = session()) -> None:
        self.__session = cur_session

    def getAreaInfo(self):
        url = "http://cwsf.whut.edu.cn/getAreaInfo"
        data = {"factorycode": self.__factorycode}
        res = self.__session.post(url, data)
        return res.text

    def queryBuildList(
        self,
        areaid: str,
    ):
        url = "http://cwsf.whut.edu.cn/queryBuildList"
        data = {"areaid": areaid, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text

    def queryFloorList(
        self,
        areaid: str,
        buildid: str,
    ):
        url = "http://cwsf.whut.edu.cn/queryFloorList"
        data = {"areaid": areaid, "buildid": buildid, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text

    def getRoomInfo(
        self,
        buildid: str,
        floorid: str,
    ):
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
    ):
        url = "http://cwsf.whut.edu.cn/queryRoomElec"
        data = {"roomid": roomid, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text

    def queryReserve(
        self,
        meterId: str,
    ):
        url = "http://cwsf.whut.edu.cn/queryReserve"
        data = {"meterId": meterId, "factorycode": self.__factorycode}
        res = self.__session.post(url, data=data)
        return res.text
