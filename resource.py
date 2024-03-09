from abc import ABC, abstractmethod
import logging
import jxmlease

class Resource(ABC):
    @classmethod
    def parseResponse(self, response):
        response_dict = jxmlease.parse(response.text)

        logging.debug(
            f'Parsed Response: {response_dict}')

        return response_dict

    @abstractmethod
    def create():
        pass

    @abstractmethod
    def validate(id):
        pass
