from abc import ABC, abstractmethod


class BaseSplitter(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def read(self, path_file):
        pass

    @abstractmethod
    def split(self, content) -> list:
        pass
