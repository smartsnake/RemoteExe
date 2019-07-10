import os
import json
import zipfile
import time

alwaysListen = True
debug = True

def processConfig(config_file):
#---------loading project config--------------
    with open(config_file) as f:
        if(debug):
            print('Loading config.')
        config = json.load(f)
        cmd = 'del ' + config_file
        if(debug):
            print('Deleting ' + config_file)
        f.close()
        os.system(cmd)
        runProgram(config)

def runProgram(config):
    if(debug):
            print('Unzipping ' + config['project_folder'] + '.zip')
    zip_ref = zipfile.ZipFile(config['project_folder'] + '.zip', 'r')
    zip_ref.extractall('.')
    zip_ref.close()

    if(debug):
            print('Deleting ' + config['project_folder'] + '.zip')
    cmd = 'del ' + config['project_folder'] + '.zip'
    os.system(cmd)

    if(debug):
        print('Changing Dir: ' + config['project_folder'])
    #cmd = 'cd ' + config['project_folder']
    #os.system(cmd)
    os.chdir(config['project_folder'])

    #Compile Program
    if(config['compile'] != None):
        if(debug):
            print('Compiling program...')
        os.system(config['compile'])

    #Run Program
    print("Run Project: " + config['project_folder'])
    os.system(config['run'])

    #Moving up dir
    os.chdir('..')


while alwaysListen:
    #Waits 10 sec to check for new project file
    time.sleep(10)
    for file in os.listdir('.'):
        if file.endswith('.project'):
            #print(file)
            if(debug):
                print('Found project: ' + file)
            processConfig(file)
            print('Program Finished.')
            break
    # else:
    #     print("Not found")