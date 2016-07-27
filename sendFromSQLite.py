#!/usr/bin/env python2
from __future__ import print_function
import sqlite3
import myLib as e
from myauth import email_account 




def sendFromDatabase():
    con = sqlite3.connect("database.sqlite")
    cur = con.cursor()
    for row in cur.execute('SELECT id,name,email,subject,msg,sent FROM email'):
        r=[str(i) for i in row]
        id=r[0]
        name=r[1]
        email=r[2]
        subject=r[3]
        msg=r[4].replace('\\n','\n')
        m=e.sm.CreateMessage(email_account, email, subject, msg )
        e.sm.SendMessage(e.service, 'me', m)
    cur.close()
    con.commit()
    con.close()    




def main():
    sendFromDatabase()


if __name__ == '__main__':
    main()

