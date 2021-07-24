import requests
import json
import sys
import os
import time
from win32com.shell import shellcon, shell            


DEBUG=False


def get_vars():
    if DEBUG:
        dirname=os.path.dirname(__file__)#, filename = os.path.split(os.path.abspath(sys.argv[0]))
    else:
        dirname=shell.SHGetFolderPath(0, shellcon.CSIDL_LOCAL_APPDATA, 0, 0).replace('\\','/')+'/Notifyi/'
   
    with open(os.path.join(dirname,'AppConfig.dat')) as json_file:
        data = json.load(json_file)
        JOB_REQUEST_URL=data['JOB_REQUEST_URL']
        LOCAL_DATA_DIR= data['LOCAL_DATA_DIR']
        USERS_FILE=data['USERS_FILE']
    return JOB_REQUEST_URL, LOCAL_DATA_DIR, USERS_FILE
 
 

if __name__ == "__main__":
    
    JOB_REQUEST_URL, LOCAL_DATA_DIR, USERS_FILE= get_vars()
    
    filename=LOCAL_DATA_DIR+USERS_FILE
    with open(filename,'r') as f:
        registered_users=[line.strip().split() for line in f.readlines()]
    title=None
    message=None

    if len(sys.argv)>4 or len(sys.argv)<2:
        raise SystemExit(f"Usage: Notifyi <username> <title> <message>")
    
    username=sys.argv[1]

    found_user=[[u,k] for u,k in registered_users if u==username]

    if len(found_user)<1:
        raise SystemExit(f"User not registered. Register User first in Notifyi User Manager")
    
    
    user=found_user[0]
    if len(sys.argv)>3:
        message=sys.argv[3]
    if len(sys.argv)>2:
        title=sys.argv[2]
    for i in range(5):
        r = requests.post(JOB_REQUEST_URL, data={'key': user[1],'username':user[0],'title':title,'message':message})
        if r.status_code==200:
            print('Job Sent to Server!')
            break
        else:
            print('Job could not be send, retrying in 1 second..')
            time.sleep(1)