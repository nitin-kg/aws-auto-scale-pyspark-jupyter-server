import logging
import requests
import polling
from ami import AMI
from security_group import SecurityGroup

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger




if __name__ == "__main__":
    logging.basicConfig(filename='aws_service.log',
                        encoding='utf-8', level=logging.DEBUG, filemode='w')

    arn_logger = setup_logger('first_logger', 'arn_logger.log')

    try:

        ami = AMI()
        image_id = ami.create()
        polling.poll(
            lambda: ami.validate(image_id) == 'available',
            step=60,
            poll_forever=True
        )
        arn_logger.debug(f'AMI ID:: {image_id}')
        
        sg = SecurityGroup()
        security_group_id = sg.create()
        is_sg_created = sg.validate(security_group_id)
        arn_logger.debug(f'Security Group ID:: {security_group_id}')
        # ingress rules


    # handle generic errors
    except requests.exceptions.ConnectionError:
        print("Error Connecting:", requests.exceptions.ConnectionError)
    except requests.exceptions.Timeout:
        print("Timeout Error:", requests.exceptions.Timeout)
    except requests.exceptions.RequestException:
        print("OOps: Something Else", requests.exceptions.RequestException)
    except SystemExit:
        print('Error with execution, exiting with exit 1')
