import boto3
import time
import paramiko

# Connect to EC2
ec2 = boto3.client('ec2', region_name="us-east-2")

# Start EC2 instance
instance_id = 'your_instance_id'
print(f'Starting EC2 instance {instance_id}...')
ec2.start_instances(InstanceIds=[instance_id])

# Wait for instance to start
instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
while instance['State']['Name'] != 'running':
    time.sleep(1)
    instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
print(f'EC2 instance {instance_id} is now running')

# Connect to EC2 instance via SSH
private_key = paramiko.RSAKey.from_private_key_file('path/to/private_key.pem')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=instance['PublicDnsName'], username='ec2-user', pkey=private_key)

# Start Docker container
print(f'Starting Docker container...')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('docker run --detach --name container_name image_name')
container_id = ssh_stdout.read().decode().strip()
print(f'Started Docker container with ID: {container_id}')

# Stop Docker container
print(f'Stopping Docker container...')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'docker stop {container_id}')
print(f'Stopped Docker container with ID: {container_id}')

# Close SSH connection
ssh.close()

# Stop EC2 instance
print(f'Stopping EC2 instance {instance_id}...')
ec2.stop_instances(InstanceIds=[instance_id])

# Wait for instance to stop
instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
while instance['State']['Name'] != 'stopped':
    time.sleep(1)
    instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
print(f'EC2 instance {instance_id} is now stopped')
