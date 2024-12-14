from basic.persistence.base import PersistenceBase


class Json(PersistenceBase):

    def __init__(self, data: str | dict = None) -> None:
        if data is None:
            return
        from data.config import dp
        import json, os
        if isinstance(data, str):
            with open(data, "r", encoding=dp.encoding.json) as file:
                self.data = json.load(file, data)
            self.path = data
        else:
            self.data = data
            self.path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "configs", "noname.json")
    
    def __call__(self, data: str | dict) -> None:
        from data.config import dp
        import json, os
        if isinstance(data, str):
            with open(data, "r", encoding=dp.encoding.json) as file:
                self.data = json.load(file, data)
            self.path = data
        else:
            self.data = data
            self.path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "configs", "noname.json")
        return self

    def save(self, path: str = None):
        from data.config import dp
        import json, os
        if path is not None:
            self.path = path
        with open(self.path, "w", encoding=dp.encoding.json) as file:
            json.dump(self.data, file, indent=dp.indent)
    
    def update(self, data: dict):
        self.data.update(data)
        return self


class JsonPlus:

    def __init__(self) -> None:
        pass


if __name__ == "__main__":
    from data.config import dp
    j = Json({
        "a": 1,
        "b": 2
    })
    print(j.path)
    j.save()
    print(dp.encoding.json)
