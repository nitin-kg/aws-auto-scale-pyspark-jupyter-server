from service_registry import ServiceRegistry
from resource import Resource
import requests
import logging
import sys


class SecurityGroup(Resource):

    def __init__(self):
        self.SERVICE_NAME = 'securityGroup'
        self.OPERATION_NAME = ''

    def create(self):
        self.OPERATION_NAME = 'createSecurityGroup'

        logging.debug(f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME}')

        try:

            api_uri, auth_params = ServiceRegistry.generate_service_url(
                self.SERVICE_NAME, self.OPERATION_NAME, additional_params={})

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

        security_group_id = response_dict['CreateSecurityGroupResponse']['groupId']

        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} New Group ID:: {security_group_id}')

        return security_group_id

    """ 
    Since there is no "state" associated with the creation of a security group
    we would need to just verify whether the security exist on the cloud or not.
    
    We query the security group with the returned group id and validate that there 
    is no error and if error happens it is not - InvalidSecurityGroupID.NotFound.
    """

    def validate(self, security_group_id):
        self.OPERATION_NAME = 'describeSecurityGroups'
        logging.debug(
            f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME} SECURITY_GROUP_ID: {security_group_id}')
        try:

            additional_params = {'GroupId.1': security_group_id}

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

        group_id = response_dict['DescribeSecurityGroupsResponse']['securityGroupInfo']['item']['groupId']

        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} Status:: {security_group_id == group_id}')

        return group_id == security_group_id
