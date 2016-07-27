#!/usr/bin/env python2
from __future__ import print_function
import httplib2
import base64
from apiclient import discovery
from oauth2client import client as oauth2client
import datetime

import publib
import csv

import os
import myauth
(PUB_CREDENTIALS,PUB_SCOPE,SUBSCRIPT,TOPIC)=myauth.setPubSub()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PUB_CREDENTIALS
PUBSUB_SCOPES = PUB_SCOPE
subscription=SUBSCRIPT



def create_pubsub_client(http=None):
    credentials = oauth2client.GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
        credentials = credentials.create_scoped(PUBSUB_SCOPES)
    if not http:
        http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('pubsub', 'v1', http=http)

client=create_pubsub_client(http=None)

def readProcess():
    with open('flatfile.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sendMessages(row['email'],row['subject'],row['msg'].replace('\\n','\n'),row['id'])


def sendMessages(email,subject,msg,id1):
    message1 = {}
    message1['email']=str(email)
    message1['subject']=str(subject)
    message1['msg']=str(msg)
    message1['accounting']=[id1,1,1,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    message1['timeStamp']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    message1 = base64.b64encode(str(message1))


    # Create a POST body for the Pub/Sub request
    body = {
    'messages': [
        {'data': message1},

    ]
    }

    resp = client.projects().topics().publish(
        topic=TOPIC, body=body).execute()

    message_ids = resp.get('messageIds')
    if message_ids:
        for message_id in message_ids:
           # Process each message ID
            print(message_id)


def sendHeartBeat(id1):
    message1 = {}
    message1['HeartBeat']=str(id1)
    message1['accounting']=[id1,1,1,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    message1['timeStamp']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



    message1 = base64.b64encode(str(message1))


    # Create a POST body for the Pub/Sub request
    body = {
    'messages': [
        {'data': message1},
    ]
    }

    resp = client.projects().topics().publish(
        topic=TOPIC, body=body).execute()

    message_ids = resp.get('messageIds')
    if message_ids:
        for message_id in message_ids:
           # Process each message ID
            print(message_id)

                        
if __name__ == '__main__':
    readProcess()



