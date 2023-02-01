import boto3
import schedule

ec2_client = boto3.client('ec2', region_name="eu-west-1")
ec2_resource = boto3.resource('ec2', region_name="eu-west-1")

reservations = ec2_client.describe_instances()

for reservation in reservations['Reservations']:
    instances = reservation['Instances']
    for instance in instances:
        print(f"Status of instance {instance['InstanceId']} is {instance['State']['Name']}")


def check_instance_status():
    statuses = ec2_client.describe_instance_status()
    for status in statuses["InstanceStatuses"]:
        ins_status = status['InstanceStatus']['Status']
        sys_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']
        print(f"Instance {status['InstanceId']} is {state} with instance status  {ins_status} and system status is {sys_status }")


schedule.every(5).seconds.do(check_instance_status)

while True:
    schedule.run_pending()
