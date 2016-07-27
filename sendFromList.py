#!/usr/bin/env python2

import myLib as e

from myauth import email_account 

def getList():
    f=open('sendList.csv','r')
    m=f.readlines()
    f.close()
    m=[i.strip().split(',') for i in m]
    m=[i for i in m if len(i) >= 2]
    for i in m:
        if len(i) > 2:
            i[2] = ",".join(i[2::])
            del(i[3::])
    return m



my_msg="""
%s:

Test message

"""


def main():
    for name,email,subject in getList():
        m=e.sm.CreateMessage(email_account, email, subject, my_msg % str(name.capitalize()) )
        e.sm.SendMessage(e.service, 'me', m)


if __name__ == '__main__':
    main()

