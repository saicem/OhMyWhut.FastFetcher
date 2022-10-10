class ApiRes:
    ok: bool
    msg: str
    data: object


class GoodRes(ApiRes):
    def __init__(self, msg: str, data: object) -> None:
        self.ok = True
        self.msg = msg
        self.data = data


class BadRes(ApiRes):
    def __init__(self, msg: str) -> None:
        self.ok = False
        self.msg = msg
        self.data = None
