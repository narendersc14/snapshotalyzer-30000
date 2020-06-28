import click
import boto3

session=boto3.Session(profile_name='awsprofile')
ec2=session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def cli():
    "Shotty manages snapshots"

#Snapshots Group Begin
@cli.group('snapshots')
def snapshots():
    "Commands for snapshots"

@snapshots.command('list')
@click.option('--project',default=None,help='Only snapshots for project (tag Project:<Name>)')
def list_snapshots(project):
    "List EC2 volume snapshots"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((s.id, v.id, i.id, s.state, s.progress, s.start_time.strftime("%c"))))
    return
#Snapshots Group End

#Volume Group Begin
@cli.group('volumes')
def volumes():
    "Commands for volumes"
@volumes.command('list')
@click.option('--project',default=None,help='Only volumes for project (tag Project:<Name>)')
def list_volumes(project):
    "List EC2 volumes"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(", ".join (( v.id, i.id, v.state, str(v.size) + "GB",
            v.encrypted and "Encrypted" or "Not Encrypted")))
    return
#Volume Group End

#Instances Group Begin
@cli.group("instances")
def instances():
    "Commands for instances"

@instances.command('list')
@click.option('--project',default=None,help='Only instances for project (tag Project:<Name>)')
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        tags={t['Key']:t['Value'] for t in i.tags or []}
        print(', '.join((i.id, i.instance_type, i.placement['AvailabilityZone'],i.state['Name'],
         i.public_dns_name, tags.get('Project','<No Project'))))
    return

@instances.command('stop')
@click.option('--project',default=None,help='Only instances for project (tag Project:<Name>)')
def stop_instances(project):
    "Stop EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0} ...".format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--project',default=None,help='Only instances for project (tag Project:<Name>)')
def start_instances(project):
    "Stop EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        print("Starting {0} ...".format(i.id))
        i.start()
    return

@instances.command('snapshot')
@click.option('--project',default=None,help='Create snapshots for all volumes')
def create_snapshots(project):
    "Create snapshots for EC2 instances"
    instances = filter_instances(project)
    
    for i in instances:
        for v in i.volumes.all():
            print("Creating snapshot for {0}".format(v.id))
            v.create_snapshot(Description="Created by SnapshotAlyzer 30000")
    return

#Instances Group End

if __name__ == '__main__':
    cli()
