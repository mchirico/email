#!/usr/bin/env python2
"""


"""
from __future__ import print_function
import httplib2
import base64
import ast
from apiclient import discovery
from oauth2client import client as oauth2client
from myauth import email_account
import myLib as e


import publib

PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
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


def sendEmail(email,subject,msg):
    m=e.sm.CreateMessage(email_account, email, subject, msg )
    e.sm.SendMessage(e.service, 'me', m)

def process(data):
    try:
        d=ast.literal_eval(data)
        if 'HeartBeat' in d:
            print("HeartBeat:"+str(d['HeartBeat']))
            publib.sendMsg(d['HeartBeat'])
        if 'email' in d:
            pass
        else:
            print('No email')
            return            
            
        if 'timeStamp' in d:
            pass
        else:
            print('No timeStamp')
            return            

        if 'subject' in d:
            pass
        else:
            print('No subject')
            return


        if 'msg' in d:
            print(d['msg'])
        else:
            print('No message')

        if 'accounting' in d:
            print("SENDING confirmation")
            publib.sendMsg(d['accounting'][0])
                
        sendEmail(d['email'],d['subject'],d['msg'])
        print(d)            
    except:
        print('process failure:>'+data+'< ')
        








batch_size = 100
body = {
        # Setting ReturnImmediately to false instructs the API to wait
            # to collect the message up to the size of MaxEvents, or until
                # the timeout.
    'returnImmediately': False,
    'maxMessages': batch_size,
    }



while True:

    resp = client.projects().subscriptions().pull(
        subscription=subscription, body=body).execute()

    received_messages = resp.get('receivedMessages')
    if received_messages is not None:
        ack_ids = []
        for received_message in received_messages:
            pubsub_message = received_message.get('message')
            if pubsub_message:
                # Process messages
                data = base64.b64decode(str(pubsub_message.get('data')))
                print(data)
                process(data)
                # Get the message's ack ID
                ack_ids.append(received_message.get('ackId'))

        # Create a POST body for the acknowledge request
        ack_body = {'ackIds': ack_ids}
#        print ack_body

        # Acknowledge the message.
        client.projects().subscriptions().acknowledge(
            subscription=subscription, body=ack_body).execute()

