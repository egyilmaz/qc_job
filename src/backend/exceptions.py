class EmptyJob(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidDelimeter(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidAxis(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidToken(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)