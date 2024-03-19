from resource import Resource
import os
import logging
from service_registry import ServiceRegistry
import requests
import sys


class LoadBalancer(Resource):

    def __init__(self):
        self.SERVICE_NAME = 'alb'
        self.OPERATION_NAME = ''

    def create(self, subnet_ids, security_group_id, ):
        self.OPERATION_NAME = 'createLoadBalancer'

        logging.debug(f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME}')

        try:

            # params
            additional_params = {
                'Subnets.member.1': subnet_ids[0],
                'Subnets.member.2': subnet_ids[1],
                'Subnets.member.3': subnet_ids[2],
                'SecurityGroups.member.1': security_group_id
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

        new_load_balancer_arn = response_dict['CreateLoadBalancerResponse'][
            'CreateLoadBalancerResult']['LoadBalancers']['member']['LoadBalancerArn']
        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} New Load Balancer ARN:: {new_load_balancer_arn}')

        return new_load_balancer_arn

    """ 
    The Load Balancer creation takes some time and the state changes from 'provisioning' to 'active'
    """

    def validate(self, load_balancer_arn):
        self.OPERATION_NAME = 'describeLoadBalancer'
        logging.debug(
            f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME} LOAD_BALANCER_ID: {load_balancer_arn}')

        try:

            # params
            additional_params = {
                'LoadBalancerArns.member.1': load_balancer_arn}

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

        load_balancer_state = response_dict['DescribeLoadBalancersResponse'][
            'DescribeLoadBalancersResult']['LoadBalancers']['member']['State']['Code']

        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} Status:: {load_balancer_state}')

        return load_balancer_state

    def create_listener(self, load_balancer_arn, target_group_arn):
        self.OPERATION_NAME = 'createListener'

        logging.debug(f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME}')

        try:

            # params
            additional_params = {
                'LoadBalancerArn': load_balancer_arn,
                'DefaultActions.member.1.TargetGroupArn': target_group_arn
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

        listener_arn = response_dict['CreateListenerResponse'][
            'CreateListenerResult']['Listeners']['member']['ListenerArn']
        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} New Load Balancer ARN:: {listener_arn}')

        return listener_arn
