from abc import ABC, abstractmethod
import jxmlease

class Resource(ABC):
    @classmethod
    def parseResponse(self, response):
        return jxmlease.parse(response.text)

    @abstractmethod
    def create():
        pass

    @abstractmethod
    def validate(id):
        pass
