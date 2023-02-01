import boto3
from operator import itemgetter

ec2_client = boto3.client("eks", region_name="eu-west-1")
ec2_resource = boto3.resource('ec2', region_name="eu-west-1")

instance_id = "xxxxxx"

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Value': [instance_id]
        }
    ]
)

instance_volume = volumes['Volumes'][0]

snapshots = ec2_client.describe_snapshots(
        OwnerId=["self"],
        Filters=[
            {
                "Name": "volume-id",
                "Values": [instance_volume['VolumeId']]
            }
        ]
    )

latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="eu-west-2b",
    TagSpecifications=[
        {
           'ResourceType': 'volume',
           'Tags': [
               {
                   'Key': 'Name',
                   'Value': "prod"
               }
            ]
        }
    ]
)

while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    if vol.state == 'available':
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'
        )
        break
