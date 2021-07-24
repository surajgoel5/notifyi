import PySimpleGUI as sg
import requests
import json
from enum import Enum
import sys, os
from win32com.shell import shellcon, shell            

DEBUG=False

#Function
class event_key(Enum):
    USER_LIST=1
    MESSAGE_REGISTERED=2
    VERIFY_REGISTERED=3
    DELETE_REGISTERED=4
    USERNAME_INPUT=5
    USERKEY_INPUT=6
    VERIFY_NEW=7
    ADD_NEW=8
    MESSAGE_NEW=9



def get_vars():
    if DEBUG:
        dirname=os.path.dirname(__file__)
    else:
        dirname=shell.SHGetFolderPath(0, shellcon.CSIDL_LOCAL_APPDATA, 0, 0).replace('\\','/')+'/Notifyi/'
   
    with open(os.path.join(dirname,'AppConfig.dat')) as json_file:
        data = json.load(json_file)
        JOB_REQUEST_URL=data['JOB_REQUEST_URL']
        LOCAL_DATA_DIR= data['LOCAL_DATA_DIR']
        USERS_FILE=data['USERS_FILE']
        VERIFICATION_URL=data['VERIFICATION_URL']
    return JOB_REQUEST_URL, LOCAL_DATA_DIR, USERS_FILE,VERIFICATION_URL


def verify_key(username, key):
    verified=False
    server_error=False
    if [username,key] in verified_users:
        verified=True
    else:
  
        req = requests.post(VERIFICATION_URL, data={'key': key})
        # TODO no reply server down 
        if req is None:
            server_error=True
            return  verified, server_error
        if req.status_code!=200:
            server_error=True
            return  verified, server_error
            
        reply=json.loads(req.content)
        #print(reply)
        if reply['valid_request']:
            if reply['found']:
                if reply['username'] == username:
                    verified=True

      
        if verified:
            verified_users.append([username,key])

    return verified, server_error

def read_local_userdata():
    filename=LOCAL_DATA_DIR+USERS_FILE
    with open(filename,'r') as f:
        users=[line.strip().split() for line in f.readlines()]
    return users

def update_local_userdata():
    filename=LOCAL_DATA_DIR+USERS_FILE
    with open(filename,'w') as f:
        [f.write(username+' '+key+'\n') for username, key in registered_users]

#update_local_userdata()
def delete_user(username):
    global registered_users;
    print(username)
    registered_users=[[u,k] for u,k in registered_users if u != username]
    update_local_userdata()


def add_user(username,key):
    global registered_users;
    present_users=[u for u,k in registered_users if u==username]
    if len(present_users)==0:
        registered_users.append([username,key])
        update_local_userdata()
        return True
    else:
        return False

def  get_reg_users_list():
    if len(registered_users) !=0:
        return [u for u,k in registered_users]
    else:
        return []

def disp_error_message(window,eventkey,message=''):
    window.Element(eventkey).Update(value=message)

def update_user_list(window, eventkey=event_key.USER_LIST):
    window.Element(eventkey).Update(values=get_reg_users_list())




JOB_REQUEST_URL, LOCAL_DATA_DIR, USERS_FILE,VERIFICATION_URL= get_vars()




verified_users=[]
registered_users=[]



sg.theme('GrayGrayGray')

registered_users= read_local_userdata()


layout = [
    [sg.Text("Add New User", font=('Helvetica',12))], 
    
    [sg.Text('Username',size=(17,1)),sg.Text('User Key',size=(15,1))],
    [ sg.InputText(key=event_key.USERNAME_INPUT,size=(20,1)), sg.InputText(key=event_key.USERKEY_INPUT,size=(20,1))],


    
    [sg.Button("Verify Key",key=event_key.VERIFY_NEW), sg.Button("Add User",key=event_key.ADD_NEW),sg.Text("",key=event_key.MESSAGE_NEW,size=(18,1))],

 [],
 [],

    [sg.Text("Registered Users", font=('Helvetica',12))], 
    [
        sg.Listbox(
            values=get_reg_users_list(), enable_events=True, size=(40, 5), key=event_key.USER_LIST
        )
    ],
   
     [sg.Button("Verify Key",key=event_key.VERIFY_REGISTERED), sg.Button("Delete",key=event_key.DELETE_REGISTERED),sg.Text("",key=event_key.MESSAGE_REGISTERED,size=(18,1))],
     

    
    ]


# Create the window
window = sg.Window("Notifyi User Manager", layout,icon='icon.ico')

# Create an event loop
while True:
    event, values = window.read()

    if event:
        disp_error_message(window,event_key.MESSAGE_REGISTERED,'');
        disp_error_message(window,event_key.MESSAGE_NEW,'');
        
    if event == event_key.VERIFY_REGISTERED:
        if len(values[event_key.USER_LIST]) == 0:
            error_message = 'Select a user to verify'
            disp_error_message(window,event_key.MESSAGE_REGISTERED,error_message)
        else:    
            to_reg = [ [u,k]  for u,k in registered_users if u == values[event_key.USER_LIST][0] ]
            verified,server_error=verify_key(*to_reg[0])
            if server_error:
                error_message = 'Server Error'
            elif verified:
                error_message = 'User Valid!'
            else:
                error_message = 'User Invalid! Re-register. '
            
            disp_error_message(window,event_key.MESSAGE_REGISTERED,error_message)
    
    if event== event_key.DELETE_REGISTERED:
        if len(values[event_key.USER_LIST]) == 0:
            error_message = 'Select a user to delete'
            disp_error_message(window,event_key.MESSAGE_REGISTERED,error_message) 
        else:
            delete_user(values[event_key.USER_LIST][0])
            update_user_list(window)

    if event==event_key.VERIFY_NEW:
        nuser,nkey=values[event_key.USERNAME_INPUT],values[event_key.USERKEY_INPUT]

        verified,server_error=verify_key(nuser,nkey)
        if server_error:
            error_message = 'Server Error'
        elif verified:
            error_message = 'User Valid!'
        else:
            error_message = 'User Invalid!'

        disp_error_message(window,event_key.MESSAGE_NEW,error_message) 

    if event==event_key.ADD_NEW:
        nuser,nkey=values[event_key.USERNAME_INPUT],values[event_key.USERKEY_INPUT]
        verified,server_error=verify_key(nuser,nkey)
        if server_error:
            error_message = 'Server Error'
        elif verified:
            if add_user(nuser,nkey):
                update_user_list(window)
                error_message = 'User Added!'
            else:
                error_message = 'User Already Exists!'
        else:
            error_message = 'User Invalid!'
        disp_error_message(window,event_key.MESSAGE_NEW,error_message) 

    if event == sg.WIN_CLOSED:
        break

window.close()