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

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


"""
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.compose','https://www.googleapis.com/auth/gmail.send',
           'https://www.googleapis.com/auth/gmail.modify']
"""
# This is everything
SCOPES = ['https://mail.google.com/']


home_dir = os.path.expanduser('~')
CLIENT_SECRET_FILE = home_dir+'/.credentialsEmail/client_secret.json'


APPLICATION_NAME = 'client1'
email_account = 'aipiggybotdead@gmail.com'


def setPubSub():
    global home_dir
    SUBSCRIPTION='projects/pigdevonly/subscriptions/emailtopic0'
    TOPIC='projects/pigdevonly/topics/emailtopic0'
    return os.path.join(home_dir, '.credentialsEmail/pigdevonly-pi3raspberry.json'),['https://www.googleapis.com/auth/pubsub'],SUBSCRIPTION,TOPIC

def setPubSubConfirm():
    global home_dir
    SUBSCRIPTION='projects/pigdevonly/subscriptions/emailtopic0confirm'
    TOPIC='projects/pigdevonly/topics/emailtopic0confirm'
    return os.path.join(home_dir, '.credentialsEmail/pigdevonly-pi3raspberry.json'),['https://www.googleapis.com/auth/pubsub'],SUBSCRIPTION,TOPIC

# https://console.cloud.google.com/iam-admin/iam/project?project=<your project>
def getKey():
    return os.path.join(home_dir, '.credentialsEmail/emailKeyPigDev.json')



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    global home_dir    
    etc_dir  = home_dir
    credential_dir = os.path.join(etc_dir, '.credentialsEmail')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'cred-email.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials




def get_credentials_specific(USER_EMAIL):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    global home_dir
    if USER_EMAIL=='':
        print('Need valid USER_EMAIL')
        return
    etc_dir  = home_dir
    credential_dir = os.path.join(etc_dir, '.credentialsEmail')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   USER_EMAIL+'.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
