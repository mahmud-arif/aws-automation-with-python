import boto3

ec2_client = boto3.client('ec2', region_name="eu-west-3")

instance_ids_paris = []

reservations_paris = ec2_client.describe_instances()['Reservations']
for res in reservations_paris:
    instances = res['Instances']
    for ins in instances:
        instance_ids_paris.append(ins["InstanceId"])

response = reservations_paris.create_tags(
     Resources=instance_ids_paris,
     Tags=[
         {
             'Key': 'environment',
             'Value': 'Prod'
         }
     ]
)
