from typing import Protocol
from abc import abstractmethod

# A route interface for the router to work with
class Route(Protocol):
    @abstractmethod
    def show(self): None

    @abstractmethod
    def hide(self): None
