import logging
import requests
import polling
import os
from ami import AMI
from security_group import SecurityGroup
from vpc import VPC
from load_balancer import LoadBalancer
from target_group import TargetGroup
from auto_scaling_group import AutoScalingGroup

formatter = logging.Formatter(
    '%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')


def setup_logger(name, log_file, level=logging.INFO):

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


if __name__ == "__main__":

    logging.basicConfig(filename='aws_service.log',
                        encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')

    arn_logger = setup_logger('ARN Tracker', 'arn_logger.log')

    try:

        # ami = AMI()
        # image_id = ami.create()
        # polling.poll(
        #     lambda: ami.validate(image_id) == 'available',
        #     step=60,
        #     poll_forever=True
        # )
        # arn_logger.debug(f'AMI ID:: {image_id}')

        # sg = SecurityGroup()
        # security_group_id = sg.create()
        # is_sg_created = sg.validate(security_group_id)
        # if not is_sg_created:
        #     exit(1)
        
        # arn_logger.debug(f'Security Group ID:: {security_group_id}')
        # # ingress rule - 1: tcp port 8888 for jupyter notebook
        # rule_1_id = sg.create_ingress_rule(
        #     os.getenv('TEST_SECURITY_GROUP_ID'), 'Create_8888_TCP_Ingress')
        # arn_logger.info(f'Create_8888_TCP_Ingress Rule_1_ID:: {rule_1_id}')
        # # ingress rule - 2: ssh port 22 for PC connection
        # rule_2_id = sg.create_ingress_rule(
        #     os.getenv('TEST_SECURITY_GROUP_ID'), 'Create_22_SSH_Ingress')
        # arn_logger.info(f'Create_22_SSH_Ingress Rule_2_ID:: {rule_2_id}')

        # launch_template_id = ami.create_launch_template(
        #     image_id=os.getenv('TEST_IMAGE_ID'), security_group_id=os.getenv('TEST_SECURITY_GROUP_ID'))
        # arn_logger.info(f'Launch Template ID:: {launch_template_id}')

        # # fetch subnets
        # vpc = VPC()
        # subnet_ids = vpc.describeSubnets()
        # arn_logger.info(f'VPC Subnet IDs:: {subnet_ids}')

        # # # load balancer
        # load_balancer = LoadBalancer()
        # load_balancer_arn = load_balancer.create(subnet_ids=subnet_ids, security_group_id=os.getenv('TEST_SECURITY_GROUP_ID'))

        # polling.poll(
        #     lambda: load_balancer.validate(load_balancer_arn) == 'active',
        #     step=60,
        #     poll_forever=True
        # )
        # arn_logger.info(f'Load Balancer ARN:: {load_balancer_arn}')

        # # # target group
        # target_group = TargetGroup()
        # target_group_arn = target_group.create(os.getenv('TEST_VPC_ID'))
        # arn_logger.info(f'Target Group ARN:: {target_group_arn}')

        # # listener
        # listener_arn = load_balancer.create_listener(load_balancer_arn=os.getenv('TEST_LB_ARN'), target_group_arn=os.getenv('TEST_TG_ARN'))
        # arn_logger.info(f'Listener ARN:: {listener_arn}')

        # auto scaling group
        auto_scaling_group = AutoScalingGroup()
        auto_scaling_group_arn = auto_scaling_group.create(subnet_ids=os.getenv('TEST_SUBNET_IDS'), target_group_arn=os.getenv('TEST_TG_ARN'))
        arn_logger.info(f'Auto Scaling Group ARN:: {auto_scaling_group_arn}')


    # handle generic errors
    except requests.exceptions.ConnectionError:
        print("Error Connecting:", requests.exceptions.ConnectionError)
    except requests.exceptions.Timeout:
        print("Timeout Error:", requests.exceptions.Timeout)
    except requests.exceptions.RequestException:
        print("OOps: Something Else", requests.exceptions.RequestException)
    except SystemExit:
        print('Error with execution, exiting with exit 1')
