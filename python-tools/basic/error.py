class LxzBaseExpection(Exception):
    """
    所有程序的默认报错
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        