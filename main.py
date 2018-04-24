import argparse
import time

import boto3

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument(
    '--access_key_id',
    type=str,
    default="",
    required=True,
    help="aws access_key id")

parser.add_argument(
    '--access_key',
    type=str,
    default="",
    required=True,
    help="aws access_key")

parser.add_argument(
    '--instance_id',
    type=str,
    default="",
    required=True,
    help="Id of the ec2 instance")

parser.add_argument(
    '--action',
    type=str,
    required=True,
    help="start|stop|reboot|status")

parser.add_argument(
    '--region',
    type=str,
    default="us-east-2",
    help="region of the instance")

args = parser.parse_args()

ec2client = boto3.client(
    'ec2',
    aws_access_key_id=args.access_key_id,
    aws_secret_access_key=args.access_key,
    region_name=args.region,
)

instances_parameter = [args.instance_id]

def wait_and_retrive_instance(instances_parameter):
    if not instances_parameter:
        return {}
    waiter = ec2client.get_waiter('instance_status_ok')
    waiter.wait(
        InstanceIds = instances_parameter,
        Filters=[
            {
                "Name": "instance-status.reachability",
                "Values": ["passed"]
            }, {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    )
    print("Instance reachable, fetching instance info")
    instance_info = ec2client.describe_instances(
        InstanceIds = instances_parameter
    )
    return instance_info["Reservations"][0]["Instances"][0]

def print_arguments():
    print('-----------  Configuration Arguments -----------')
    for arg, value in sorted(vars(args).iteritems()):
        print('%s: %s' % (arg, value))
    print('------------------------------------------------')


if __name__ == "__main__":
    print_arguments()
    if args.action == "start":
        response = ec2client.start_instances(
            InstanceIds = instances_parameter
        )
        if len(response["StartingInstances"]) >0 :
            print("Instance started, trying to verify state of the instance, this may take several minutes...")
            instance_info = wait_and_retrive_instance(instances_parameter)
            pub_ip = instance_info["PublicIpAddress"]
            key_pair_name = instance_info["KeyName"]
            print("connect to instance with the command as follows:")
            print("ssh -i " + key_pair_name + ".pem ubuntu@" + pub_ip)
        else:
            print("Instance failed to start")
    elif args.action == "stop":
        response = ec2client.stop_instances(
            InstanceIds = instances_parameter
        )
        if len(response["StoppingInstances"]) > 0:
            print("Instance is stopping, might take several minutes to stop completely...")
        stop_waiter = ec2client.get_waiter('instance_stopped')
        stop_waiter.wait(
            InstanceIds = instances_parameter,
        )
        print("Instance stopped")
    elif args.action == "reboot":
        response = ec2client.reboot_instances(
            InstanceIds = instances_parameter
        )
        print ("Instance rebooting, waiting for reboot to complete...")
        time.sleep(5)
        instance_info = wait_and_retrive_instance(instances_parameter)
        pub_ip = instance_info["PublicIpAddress"]
        key_pair_name = instance_info["KeyName"]
        print("connect to instance with the command as follows:")
        print("ssh -i " + key_pair_name + ".pem ubuntu@" + pub_ip)
    elif args.action == "status":
        instance_info = ec2client.describe_instances(
            InstanceIds = instances_parameter
        )
        print(instance_info["Reservations"][0]["Instances"][0]["State"]["Name"])
    else:
        raise ValueError("action must be one of start|stop|reboot")

