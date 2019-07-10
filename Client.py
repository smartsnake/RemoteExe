import argparse
import os
import sys
import json
import zipfile
import paramiko
import fabric
from scp import SCPClient

parser = argparse.ArgumentParser()
debug = False

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

#Run Program on remote computer.
def execute(connection):
    #Unzipping Remote file
    if(debug):
            print('Unzipping ' + config['project_folder'] + '.zip')
    cmd = 'powershell Expand-Archive ' + config['project_folder'] + '.zip . -Force'
    connection.run(cmd, hide='err')

    #Deleting zip
    if(debug):
            print('Deleting ' + config['project_folder'] + '.zip')
    cmd = 'del ' + config['project_folder'] + '.zip'
    connection.run(cmd)

    #Compile Program
    if(config['compile'] != None and config['compile'] != ""):
        if(debug):
            print('Compiling program...')
        connection.run(config['compile'])
    
    #Run Program
    print("Run Project: " + config['project_folder'])
    result = connection.run(config['run'], hide='err')


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
host = config['host']
user = config['username']
password = config['password']

connection = fabric.Connection(
    host=host,
    user=user,
    connect_kwargs={
        "password": password,
    },
)

connection.put(config['project_folder'] + '.zip')
if(debug):
    print('Project Zip file pushed to Remote.')

execute(connection)

connection.close()


print("Successful!")
