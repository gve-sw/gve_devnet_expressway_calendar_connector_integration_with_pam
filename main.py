'''
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''


import requests,json,smtplib
from netmiko import ConnectHandler
import urllib3

urllib3.disable_warnings()

base = ""
apikey = ""
runas = ""
systemName = ""
accountName = ""

e_host = ""
e_username = ""
e_password = ""

def retrieve_pwd():
    header = {'Authorization': 'PS-Auth key='+ apikey +'; runas=' + runas + ' ;'}


    session = requests.Session()
    session.headers.update(header)
    response = session.post('https://'+ base + '/BeyondTrust/api/public/v3/Auth/SignAppin',verify=False)
    pwd_response=session.get('https://'+ base +'/BeyondTrust/api/public/v3//ManagedAccounts?systemName='+ systemName + '&accountName='+ accountName).json()

    data={}
    data['SystemId']=pwd_response['SystemId']
    data['AccountId']=pwd_response['AccountId']
    data['DurationMinutes']=1

    req_response=session.post('https://'+ base + '/BeyondTrust/api/public/v3/Requests', headers={'Content-Type': 'application/json'}, json=data)
    RequestID=""
    RequestID=req_response.text
    cred_reponse=session.get('https://' + base+ '/BeyondTrust/api/public/v3/Credentials/'+ RequestID)

    password=cred_reponse.text

    checkin_req=session.put('https://'+base+ '/BeyondTrust/api/public/v3/Requests/'+ RequestID+ '/Checkin')
    signout_req=session.post('https://' + base+ '/BeyondTrust/api/public/v3/Auth/Signout')

    return password



def config_pwd(pam_password):
    cred = {
    'device_type': 'cisco_tp',
    'host':   e_host,
    'username': e_username,
    'password': e_password
    }

    password=pam_password
    net_connect = ConnectHandler(**cred)
    cmd=f"""xcommand cafe c_cal update_calendar_exchange_config '{{"service_record_id": "recordIdHere", "password": {password}, "emailAddress": "emailHere" }}' """
    send_cmmd=net_connect.send_command_timing(cmd)
    if send_cmmd == "":
        print('ok')
        return "OK"
    print('error')
    return "ERROR - check cronoutput.txt file"

def send_email(output):
    sender = 'senderEmailHere'
    receivers = ['receiverEmailHere']

    message = """From: PAM Integration With Expressway <>
    To: IPT Team <>
    Subject: PAM Integration Result

    """ + f"Script output: {output}"

    try:
        smtpObj = smtplib.SMTP('', 25)
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except Exception as e:
        print(e)
        print("Error: unable to send email")

password=retrieve_pwd()
output = config_pwd(password)
send_email(output) 
