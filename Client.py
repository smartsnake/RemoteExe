import argparse
import os
import sys
import json
import zipfile
import paramiko
from scp import SCPClient

parser = argparse.ArgumentParser()
debug = True

parser.add_argument('-c', action='store', dest='config',
                    help='config.project file')


results = parser.parse_args()

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    if(debug):
        sys.stdout.write("%s\'s progress: %.2f%%   \r\n" % (filename, float(sent)/float(size)*100) )


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if(debug):
    print('-c: ', results.config)

config = None
#---------loading project config--------------
with open(results.config) as f:
    config = json.load(f)

#--------Zip Project Folder-----------
if(config['project_folder'] != None):
    project = config['project_folder']
    zipf = zipfile.ZipFile(project + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(project, zipf)
    zipf.close()
else:
    print('Project Folder is None!')

#--------Sending project zip-------------
ssh = paramiko.SSHClient()
host = config['host']
user = config['username']
password = config['password']

cmd_to_execute = 'mkdir ' + config['project_folder']

ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=password)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)

scp = SCPClient(ssh.get_transport(), progress = progress)
scp.put(config['project_folder'] + '.zip', config['project_folder'] )
scp.put(results.config, config['project_folder'] )
scp.close()
ssh.close()


print("Successful!")
