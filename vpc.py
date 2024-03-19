from service_registry import ServiceRegistry
import requests
from resource import Resource
import logging
import sys
import jxmlease

class VPC(Resource):
    def __init__(self):
        self.SERVICE_NAME = ''
        self.OPERATION_NAME = ''

    def create():
        pass

    def validate():
        pass

    def describeSubnets(self):
        self.OPERATION_NAME = 'describeSubnets'
        self.SERVICE_NAME = 'vpc'

        logging.debug(f'START:: {self.SERVICE_NAME} {self.OPERATION_NAME}')

        try:

            # params
            # additional_params = {
                # 'Filter.1.Name': 'vpc-id',
                # 'Filter.1.Value.1': vpc_id,
            # }

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

        subnetIds = []
        for val in response_dict['DescribeSubnetsResponse']['subnetSet']['item']:
            xml_subnet = val.emit_xml()
            parsed_subnet = jxmlease.parse(xml_subnet)
            x = str(parsed_subnet['item']['subnetId'])
            subnetIds.append(x)
            
        logging.debug(
            f'END:: {self.SERVICE_NAME} {self.OPERATION_NAME} Subnet IDs:: {subnetIds}')

        return subnetIds
