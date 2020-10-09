import paramiko
from scp import SCPClient
import sys
import yaml
import glob
import os

connection_config = yaml.safe_load(open("scp_config.yml"))

scp_information = connection_config['scp_information']
 
host = scp_information['Host']
username = scp_information['Username']
passphrase = scp_information['Passphrase']
SSH_path = scp_information['SSH_path_to_key']
remote_path = scp_information['remote_path']

# Creating the SSHClient
def connect_via_ssh(host, username, pathphrase, SSH_path):
    SSHclient = paramiko.SSHClient()
    SSHclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSHclient.connect(hostname=host, username=username, passphrase = passphrase, key_filename=SSH_path)
    return SSHclient

ssh = connect_via_ssh(host, username, passphrase, SSH_path)
scp = SCPClient(ssh.get_transport())

file_list = (glob.glob("*.csv"))

user_input = input("Do you want to upload the following file(s): %s? (yes/no): "%(str(file_list).strip('[]')))
	# Check the input value

if user_input == 'yes':
	print('Success')
	for file in file_list:
		absolute_path = os.path.abspath(file)
		scp.put(absolute_path, remote_path)
elif user_input == 'no':
	print('File(s) will not be uploaded to OT-2. Please remove incorrect files from directory and run upload script again.')
else:
	print('Invalid input ')



