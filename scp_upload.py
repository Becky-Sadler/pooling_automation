import paramiko
from scp import SCPClient
import sys
import yaml

connection_config = yaml.safe_load(open("scp_config.yml"))

scp_information = connection_config['scp_information']
 
host = scp_information['Host']
username = scp_information['Username']
passphrase = scp_information['Passphrase']
SSH_path = scp_information['SSH_path_to_key']
remote_path = scp_information['remote_path']
local_path = scp_information['local_path']


print(host)
print(username)
print(passphrase)
print(SSH_path)
print(remote_path)
print(local_path)

'''with paramiko.SSHClient() as client:
	client.set_missing_host_key_policy(paramiko.client.WarningPolicy)
	connection = client.connect(hostname=robot_ip, username='root', passphrase='mypassphrase', key_filename='/path/to/ot2_ssh_key')
	'''