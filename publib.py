#!/usr/bin/env python2
from __future__ import print_function
import httplib2
import base64
from apiclient import discovery
from oauth2client import client as oauth2client
import datetime
import time



import os
import myauth
(PUB_CREDENTIALS,PUB_SCOPE,SUBSCRIPT,TOPIC)=myauth.setPubSubConfirm()
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





def checkForMessage():
    data=None
    batch_size = 100
    body = {
        # Setting ReturnImmediately to false instructs the API to wait
            # to collect the message up to the size of MaxEvents, or until
                # the timeout.
    'returnImmediately': True,
    'maxMessages': batch_size,
    }

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
#                print(data)
#                process(data)
                # Get the message's ack ID
                ack_ids.append(received_message.get('ackId'))

        # Create a POST body for the acknowledge request
        ack_body = {'ackIds': ack_ids}
#        print ack_body

        # Acknowledge the message.
        client.projects().subscriptions().acknowledge(
            subscription=subscription, body=ack_body).execute()
    return data        




def sendHeartBeat(id1):
    message1 = {}
    message1['HearBeat']=str(id1)
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
           pass
           #print(message_id)



def sendMsg(msg):
    message1 = base64.b64encode(str(msg))

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

                        

def timeCheck(msg,num=3,sec=3):
    print("waiting for confirmation")
    for i in range(0,num):
        sendHeartBeat('timeCheck'+str(i)+':'+str(msg))
        return_msd = checkForMessage()
        if return_msd != None:
            if msg.find(return_msd) >= 0:
                print("CONFIRMED!!....")
                return return_msd
        time.sleep(sec)
        sendHeartBeat('timeCheck_2'+str(i)+':'+str(msg))
    
