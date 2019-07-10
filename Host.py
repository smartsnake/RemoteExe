import os
import json
import zipfile

alwaysListen = True
debug = True

def processConfig(config_file):
#---------loading project config--------------
    with open(config_file) as f:
        if(debug):
            print('Loading config.')
        config = json.load(f)
        cmd = 'rm ' + config_file
        if(debug):
            print('Deleting ' + config_file)
        os.system(cmd)
        runProgram(config)

def runProgram(config):
    if(debug):
            print('Unzipping ' + config['project_folder'])
    zip_ref = zipfile.ZipFile(config['project_folder'] + '.zip', 'r')
    zip_ref.extractall('..')
    zip_ref.close()

    if(debug):
            print('Deleting ' + config['project_folder'] + '.zip')
    cmd = 'rm ' + config['project_folder'] + '.zip'
    os.system(cmd)

    #Compile Program
    if(config['compile'] != None):
        if(debug):
            print('Compiling program...')
        os.system(config['compile'])

    #Run Program
    print("Run Complete: " + config['project_folder'])
    os.system(config['run'])


while alwaysListen:
    for file in os.listdir('.'):
        if file.endswith('.project'):
            #print(file)
            if(debug):
                print('Found project: ' + file)
            processConfig(file)
            break
    else:
        print("Not found")