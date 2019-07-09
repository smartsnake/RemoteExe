import os
import json
import zipfile

#config = None
def processConfig(config_file):
#---------loading project config--------------
    with open(config_file) as f:
        config = json.load(f)
        cmd = 'rm ' + config_file
        os.system(cmd)
        runProgram(config)

def runProgram(config):
    zip_ref = zipfile.ZipFile(config['project_folder'] + '.zip', 'r')
    zip_ref.extractall('..')
    zip_ref.close()

    cmd = 'rm ' + config['project_folder'] + '.zip'
    print(cmd)
    os.system(cmd)

    #Run Program
    os.system(config['run'])
    
    #print("Running")

#while True:
for file in os.listdir('.'):
    if file.endswith('.project'):
        #print(file)
        processConfig(file)
        break
else:
    print("Not found")