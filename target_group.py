import logging
from resource import Resource
import sys

import requests
from service_registry import ServiceRegistry


class TargetGroup(Resource):

    def __init__(self):
        self.serviceName = 'targetGroup'
        self.operationName = ''

    # do we need VPC_ID?
    def create(self, vpc_id):
        self.OPERATION_NAME = 'createTargetGroup'

        logging.debug(f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME}')

        try:
            # params
            additional_params = {
                'VpcId': vpc_id
            }

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
            awsErrorCode = response_dict['ErrorResponse']['Error']['Code']
            logging.debug(
                f'AWS Error Code:: {self.SERVICE_NAME} {self.OPERATION_NAME}:: {awsErrorCode}')
            sys.exit(1)

        target_group_arn = response_dict['CreateTargetGroupResponse'][
            'CreateTargetGroupResult']['TargetGroups']['member']['TargetGroupArn']
        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} New Target Group ARN:: {target_group_arn}')

        return target_group_arn

    def validate(asg_id):
        pass
