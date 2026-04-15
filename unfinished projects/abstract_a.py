from abc import ABC, abstractmethod
class Animal (ABC):
    @abstractmethod
    def __init__(self, sound: str)- None:
        self.__sound = sound 
