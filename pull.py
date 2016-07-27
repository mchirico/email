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
import base64

from myauth import get_credentials

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
    




def saveMsg(r):
    MAIL=''
    MSG=''
    try:
        for i in r['payload']['headers']:
            if 'name' in i:
                if i['name']=='Return-Path':
                    MAIL=i['value']
                    print(MAIL)
    except:
        return
    if 'payload' in r:
        if 'parts' in r['payload']:
            for i in r['payload']['parts']:
                if i['mimeType'] == 'text/plain':
                    try:
                        s=i['body']['data']
                        s2=base64.b64decode(s)
                        s2=s2.replace('\n','{RET}').replace('\r','').replace(',','{COMMA}')
                        MSG=s2
                    except:
                        print("Issue with header...skipping")
    d=datetime.datetime.now()
    timeStamp=conv(d).strftime("%Y-%m-%d %H:%M:%s")
    if MSG == '':
        return
    f=open('mailLogtext.csv','a')
    f.write(timeStamp+','+MAIL+','+MSG+'\n')
    f.close()
    print("Message saved: "+str(MAIL))




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

I'm getting over a 100 emails per day for jobs and positions. It's
easier for me to keep track of what you're looking for on the
following form, which is only a few questions.

   http://goo.gl/forms/XNs91xGMvq


Thank you,

Mike Chirico
mike.chirico@cwxstat.com

"""
    if 'messages' in msg:
      for i in msg['messages']:
        r = service.users().messages().get(userId='me',id=i['id']).execute()
        try:
            saveMsg(r)
        except:
            print("error in saveMsg(r)...still going")
        snippet=''
        if 'snippet' in r:
            snippet = r['snippet']
            snippet = snippet.encode('ascii',errors='ignore')
            snippet.replace('\n','{RET}')
            snippet.replace(",",'{COMMA}')
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
        if email != 'mike.chirico@cwxstat.com' and email != '' and subject != '':
            #m=sm.CreateMessage('mike.chirico@cwxstat.com', email, subject, my_msg)
            #sm.SendMessage(service, 'me', m)
            service.users().messages().delete(userId='me',id=i['id']).execute()
            deleted=1
            subject = subject.encode('ascii',errors='ignore')
            log(email+','+'DELETING'+','+str(subject.replace(',','{COMMA}'))+','+str(snippet))
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

