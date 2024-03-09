from service_registry import ServiceRegistry
from resource import Resource
import requests
import logging
import os
import sys


class AMI(Resource):
    def __init__(self):
        self.SERVICE_NAME = 'ami'
        self.OPERATION_NAME = ''

    def create(self):
        self.OPERATION_NAME = 'createImage'
        instance_id = os.getenv('AMI_INSTANCE_ID')

        logging.debug(f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME}')

        try:

            # params
            additional_params = {'InstanceId': instance_id}

            api_uri, auth_params = ServiceRegistry.generate_service_url(
                self.SERVICE_NAME, self.OPERATION_NAME, additional_params=additional_params)

            response = requests.request(
                method='GET', url=api_uri, auth=auth_params)

            response_dict = Resource.parseResponse(response)
            logging.debug(
                f'Response:: {self.SERVICE_NAME} {self.OPERATION_NAME}:: {response_dict}')

            response.raise_for_status()

        except requests.exceptions.HTTPError:
            logging.debug(
                f'Http Error:: {self.SERVICE_NAME} {self.OPERATION_NAME}:: {requests.exceptions.HTTPError}')
            awsErrorCode = response_dict['Response']['Errors']['Error']['Code']
            logging.debug(
                f'AWS Error Code:: {self.SERVICE_NAME} {self.OPERATION_NAME}:: {awsErrorCode}')
            sys.exit(1)

        new_image_id = response_dict['CreateImageResponse']['imageId']
        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} New Group ID:: {new_image_id}')

        return new_image_id

    """ 
    The AMI creation takes some time and the state changes from 'pending' to 'available'
    """

    def validate(self, image_id):
        self.OPERATION_NAME = 'describeImages'
        logging.debug(
            f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME} SECURITY_GROUP_ID: {image_id}')

        try:

            # params
            additional_params = {'ImageId': image_id}

            api_uri, auth_params = ServiceRegistry.generate_service_url(
                self.SERVICE_NAME, self.OPERATION_NAME, additional_params=additional_params)

            response = requests.request(
                method='GET', url=api_uri, auth=auth_params)

            response_dict = Resource.parseResponse(response)
            logging.debug(
                f'Response:: {self.SERVICE_NAME} {self.OPERATION_NAME}:: {response_dict}')

            response.raise_for_status()

        except requests.exceptions.HTTPError:
            logging.debug(
                f'Http Error:: {self.SERVICE_NAME} {self.OPERATION_NAME}:: {requests.exceptions.HTTPError}')
            awsErrorCode = response_dict['Response']['Errors']['Error']['Code']
            logging.debug(
                f'AWS Error Code:: {self.SERVICE_NAME} {self.OPERATION_NAME}:: {awsErrorCode}')
            sys.exit(1)

        image_state = response_dict['DescribeImagesResponse']['imagesSet']['item']['imageState']

        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} Status:: {image_state}')

        return image_state
