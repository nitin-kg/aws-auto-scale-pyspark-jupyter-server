from resource import Resource
import logging
import requests
import sys
from service_registry import ServiceRegistry

class AutoScalingGroup(Resource):
    
    def __init__(self):    
        self.SERVICE_NAME = 'autoscaling'
        self.OPERATION_NAME = ''

    def create(self, subnet_ids, target_group_arn):
        self.OPERATION_NAME = 'createAutoScalingGroup'
        logging.debug(f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME}')

        try:
            # params
            additional_params = {
                'VPCZoneIdentifier': ','.join(subnet_ids), # comma separated subnet-ids
                'TargetGroupARNs.member.1': target_group_arn,
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

        auto_scale_group_arn = response_dict['CreateTargetGroupResponse'][
            'CreateTargetGroupResult']['TargetGroups']['member']['TargetGroupArn']
        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} New Target Group ARN:: {auto_scale_group_arn}')

        return auto_scale_group_arn
    
    def validate(self, asg_id):
        self.OPERATION_NAME = 'describeAutoScalingGroups'
        pass

    def createScalingPolicy(self):
        self.OPERATION_NAME = 'PutScalingPolicy'