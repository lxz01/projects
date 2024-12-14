from typing import Any
from basic.persistence.base import PersistenceBase


class Yaml(PersistenceBase):
    def __init__(self, data: str | dict = None) -> None:
        if data is None:
            return
        from data.config import dp
        import yaml, os
        if isinstance(data, str):
            with open(data, "r", encoding=dp.encoding.json) as file:
                self.data = yaml.safe_dump(file, data)
            self.path = data
        else:
            self.data = data
            self.path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "configs", "noname.yaml")
    
    def __call__(self, data: str | dict) -> Any:
        from data.config import dp
        import yaml, os
        if isinstance(data, str):
            with open(data, "r", encoding=dp.encoding.json) as file:
                self.data = yaml.safe_dump(file, data)
            self.path = data
        else:
            self.data = data
            self.path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "configs", "noname.yaml")
        return self

    def save(self, path: str = None):
        from data.config import dp
        import yaml, os
        if path is not None:
            self.path = path
        with open(self.path, "w", encoding=dp.encoding.json) as file:
            yaml.dump(self.data, file, indent=dp.indent)
    
    def update(self, data: dict):
        self.data.update(data)
        return self


if __name__ == "__main__":
    y = Yaml({
        "a": "b",
        "c": "d"
    }).save()
