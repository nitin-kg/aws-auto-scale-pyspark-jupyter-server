import os
import logging
from requests_aws4auth import AWS4Auth
from dotenv import load_dotenv


class ServiceRegistry:

    SERVICES = {}

    load_dotenv()

    @classmethod
    def generate_auth_params(cls, service):
        AUTHPARAMS = AWS4Auth(os.getenv('AWS_ACCESS_KEY_ID'), os.getenv(
            'AWS_SECRET_ACCESS_KEY'), os.getenv('REGION'), service)

        logging.info(f'AWS AuthParam:: {AUTHPARAMS.__dict__}')
        logging.info(
            f'AWS SignKey:: {AUTHPARAMS.signing_key.__dict__}')

        return AUTHPARAMS

    @classmethod
    def register_service(cls, service_name, endpoint, operations):
        cls.SERVICES[service_name] = {
            'endpoint': endpoint,
            'operations': operations,
        }

    @classmethod
    def generate_service_url(cls, service_name, operation_name, additional_params=None):
        service_info = cls.SERVICES.get(service_name)

        if not service_info:
            raise ValueError(
                f"Service '{service_name}' not found in the registry.")

        operation_info = next(
            (op for op in service_info['operations'] if operation_name in op), None)

        if not operation_info:
            raise ValueError(
                f"Operation '{operation_name}' not found for service '{service_name}'.")

        endpoint = service_info['endpoint']

        is_dry_run = os.getenv('DryRun')
        region = os.getenv('REGION')

        AUTHPARAMS = cls.generate_auth_params(endpoint)

        if endpoint == 'ec2':
            version = '2016-11-15'
        elif endpoint == 'autoscaling':
            version = '2011-01-01'
        else:
            version = '2015-12-01'
        api_uri = f"https://{endpoint}.{region}.amazonaws.com/?Version={version}&DryRun={is_dry_run}"

        # Add default params from service registry
        params = operation_info[operation_name]
        for param, value in params.items():
            api_uri += f"&{param}={value}"

        # Add additional parameters if provided
        if additional_params:
            for param, value in additional_params.items():
                api_uri += f"&{param}={value}"

        logging.debug(
            f'Service:: {service_name} Operation:: {operation_name} API Endpoint:: {api_uri}')

        return api_uri, AUTHPARAMS


# Registering services and operations
ServiceRegistry.register_service('ami', 'ec2', [
    {
        'createImage': {
            'Action': 'CreateImage',
            'Description': 'AMI created via aws api',
            'Name': 'CCSA_AWS_API_Image',
        }
    },
    {'describeImages': {'Action': 'DescribeImages'}},
    {'createLaunchTemplate': {
        'Action': 'CreateLaunchTemplate',
        'VersionDescription': '1',
        'LaunchTemplateName': 'CCSA_AWS_API_Launch_Template',
        'LaunchTemplateData.InstanceType': 't2.micro',
    }}
])

ServiceRegistry.register_service('securityGroup', 'ec2', [
    {
        'createSecurityGroup': {
            'Action': 'CreateSecurityGroup',
            'GroupDescription': 'Security group created via aws api',
            'GroupName': 'CCSA_AWS_API_Security_Group'
        }
    },
    {'describeSecurityGroups': {'Action': 'DescribeSecurityGroups'}},
    {
        'Create_8888_TCP_Ingress': {
            'Action': 'AuthorizeSecurityGroupIngress',
            'IpPermissions.1.IpProtocol': 'tcp',
            'IpPermissions.1.FromPort': '8888',
            'IpPermissions.1.ToPort': '8888',
            'IpPermissions.1.IpRanges.1.CidrIp': '0.0.0.0/0',
            'IpPermissions.1.IpRanges.1.Description': 'CCSA_Rule_1_JUPYTER',
        },
        'Create_22_SSH_Ingress': {
            'Action': 'AuthorizeSecurityGroupIngress',
            'IpPermissions.1.IpProtocol': 'tcp',
            'IpPermissions.1.FromPort': '22',
            'IpPermissions.1.ToPort': '22',
            'IpPermissions.1.IpRanges.1.CidrIp': '184.188.101.162/32',
            'IpPermissions.1.IpRanges.1.Description': 'CCSA_Rule_2_SSH',
        }
    }
])

ServiceRegistry.register_service('alb', 'elasticloadbalancing', [
    {
        'createLoadBalancer': {
            'Action': 'CreateLoadBalancer',
            'Scheme': 'internet-facing',
            'Name': 'CCSA-AWS-API-LoadBalancer',
            'Type': 'application',
            'IpAddressType': 'ipv4',
        }},
    {'describeLoadBalancer': {'Action': 'DescribeLoadBalancers'}},
    {'createListener': {
        'Action': 'CreateListener',
        'Protocol': 'HTTP',
        'DefaultActions.member.1.Type': 'forward',
        'Port': '8888'
    }},
])

ServiceRegistry.register_service('vpc', 'ec2', [
    {'describeSubnets': {'Action': 'DescribeSubnets'}}])

ServiceRegistry.register_service('targetGroup', 'elasticloadbalancing', [
    {'createTargetGroup': {
        'Action': 'CreateTargetGroup',
        'Name': 'CCSA AWS API Target Group',
        'Port': '8888',
        'TargetType': 'instance',
        'Protocol': 'HTTP',
        'IpAddressType': 'ipv4'
    }}
])

ServiceRegistry.register_service('autoscaling', 'autoscaling', [
    {'createAutoScalingGroup': {
        'Action': 'CreateAutoScalingGroup',
        'AvailabilityZone.member.1': 'us-east-2',
        'AutoScalingGroupName': 'CCSA-AWS-API-Autoscaling-Group',
        'LaunchConfigurationName': 'CCSA_AWS_API_Launch_Template',
        'LoadBalancerNames.member.1': 'CCSA-AWS-API-LoadBalancer',
        'MinSize': '0',
        'MaxSize': '3',
        'DesiredCapacity': '1',
        'DefaultCooldown': '30',
    }},
    {'describeAutoScalingGroups': {'Action': 'DescribeAutoScalingGroups'}},
    {'PutScalingPolicy': {
        'Action': 'PutScalingPolicy'
    }},
])
