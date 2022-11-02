class LruDict:
    def __init__(self, maxsize: int):
        self.jar = dict()
        self.maxsize = maxsize

    def add(self, key: str, value):
        if key in self.jar:
            del self.jar
        self.jar[key] = value
        if self.maxsize < len(self.jar):
            del self.jar[next(iter(self.jar))]

    def get(self, key: str):
        return self.jar.get(key, None)
