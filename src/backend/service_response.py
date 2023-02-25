class ServiceResponse:
    def __init__(self, status, data=None) -> None:
        self._status = status
        self._data = data
    @property
    def status(self):
        return self._status
    @property
    def data(self):
        return self._data

