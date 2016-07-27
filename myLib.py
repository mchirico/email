#!/usr/bin/env python2

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import time
from pytz import timezone
import pytz
eastern = timezone('US/Eastern')

import sendEmail as sm
import json

from myauth import get_credentials
from myauth import email_account 

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def conv(d):
    timezone='US/Eastern'
    native=d
    if type(d)  == type('str'):
       native=datetime.datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
    if time.timezone == 0:
        return native.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
    else:
        return native


def log(s):
    d=datetime.datetime.now()
    timeStamp=conv(d).strftime("%Y-%m-%d %H:%M:%s")
    f=open('mailLog.csv','a')
    f.write(timeStamp+','+str(s)+'\n')
    f.close()
    



credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

msg = service.users().messages().list(userId='me').execute()
my_msg="""

This is my test message

"""


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    msg = service.users().messages().list(userId='me').execute()
    my_msg="""

test message 2

"""
    if 'messages' in msg:
      for i in msg['messages']:
        r = service.users().messages().get(userId='me',id=i['id']).execute()
        deleted=0
        subject=''
        email=''
        for k in r['payload']['headers']:
            if 'name' in k:
                if k['name'].lower() == 'subject':
                    subject=k['value']
                    print(subject)
                if k['name'].lower() == 'from':
                    email=k['value']
        if email != email_account and email != '' and subject != '':
            service.users().messages().delete(userId='me',id=i['id']).execute()
            deleted=1
            log(email+','+'Would have sent but only ran who - DELETING')
            print('deleted email:',email)
        if deleted == 0:
            service.users().messages().delete(userId='me',id=i['id']).execute()
            log(email+','+'just deleted')            
            print('Just DELETE: deleted email:',email)            

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
      #  print(label['name'])
         1==1


if __name__ == '__main__':
    main()

