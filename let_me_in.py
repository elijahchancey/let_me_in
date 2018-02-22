#!/usr/bin/env python3

import ipgetter
import argparse
import sys
import socket
import boto3
import getpass
import datetime

parser = argparse.ArgumentParser(
    description=
    "Creates an Inbound TCP Security Rule for the Security Group Name and Port you specify. The Source IP is automatically set to your Public IP address. The description is automatically set using your username and system hostname."
)
parser.add_argument("security_group_name", help="security group")
parser.add_argument("port", help="port")
args = parser.parse_args()

# Verify exactly two arguments were specified. Yeah, I know it says 3 and not 2.
if len(sys.argv) != 3:
    parser.print_help()
    exit(1)

print('This Inbound Security Rule is about to be added:')

# Security Group Name
security_group_name = args.security_group_name
print('Security Group Name: ' + security_group_name)

client = boto3.client('ec2')
response_describe_security_groups = client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [security_group_name]}])
security_group_id = response_describe_security_groups["SecurityGroups"][0]["GroupId"]
print('Security Group Id:   ' + security_group_id)

my_ip = ipgetter.myip()
my_ip_cidr = my_ip + '/32'
print('My IP Address:       ' + my_ip_cidr)

port = args.port
print('Port:                TCP/' + port)

my_hostname = socket.gethostname().replace(".local","")
my_username = getpass.getuser()
now = datetime.datetime.now()
now_date = now.strftime("%Y-%m-%d")

rule_description = now_date + '.' + my_username + '.' + my_hostname 
print('Rule Description:    ' + rule_description)

verification = input("Type 'yes' to continue: ")
if verification != 'yes':
    print("You must type 'yes' to continue.")
    exit(1)

client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[{
        'FromPort': int(port),
        'IpProtocol': 'TCP',
        'IpRanges': [
            {
                'CidrIp': my_ip_cidr,
                'Description': rule_description
            },
        ],
        'ToPort': int(port)
    }])

print ('Rule Added.')
