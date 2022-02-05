from abc import ABC, abstractmethod

class Loader(ABC):

    @abstractmethod
    def load_platform_history(self):
        pass

    @abstractmethod
    def load_instrument_list(self):
        pass

    @abstractmethod
    def update_platform_history(self):
        pass