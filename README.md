# snapshotalyzer-30000

Demo project to manage AWS EC2 instance snapshots

## About

This project is a demo, and uses boto3 to manage AWS EX2 instance snapshots.

## Configuration

shotty uses the configuration file created by the AWS cli. eg.

`aws configuration --profile awsprofile`

## Running

`pipenv run "python shotty/shotty.py <command> <subcommand> <--project=PROJECT>"`

*Command* is instances, volumes, or snapshots
*subcommand* depends on command
*project* is optional
