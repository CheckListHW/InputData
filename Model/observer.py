from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Callable


class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass


class Subject(ABC):
    __slots__ = ['_observers']

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)


class ObjectObserver(Observer):
    def __init__(self, handlers: [Callable]):
        super(ObjectObserver, self).__init__()
        self.__handlers: [Callable] = list()
        self.add_handlers(handlers)

    def add_handler(self, handler: Callable) -> None:
        self.__handlers.append(handler)

    def add_handlers(self, handlers: [Callable]) -> None:
        for handler in handlers:
            self.add_handler(handler)

    def update(self, subject: Subject) -> None:
        for handler in self.__handlers:
            handler()
