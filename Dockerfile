FROM ubuntu
MAINTAINER Mike Chirico <mchirico@gmail.com>
RUN apt-get update
RUN apt-get install -y python sqlite3 vim
RUN apt-get install -y python-setuptools python-dev build-essential python-pip
RUN apt-get install -y cron vim screen

# Yes, do this twice so it get's cached
RUN pip install --upgrade pip
RUN pip install gunicorn==19.6.0
RUN pip install numpy==1.11.1
RUN pip install pytz
RUN pip install --upgrade google-api-python-client
RUN pip install gcloud


RUN mkdir /email
ADD myLib.py /email
ADD myauth.py /email
ADD pull.py /email
ADD sendEmail.py /email
ADD sendFromList.py /email
ADD sendFromSQLite.py /email
ADD sendList.csv /email
ADD database.sqlite /email
ADD buildSqlite.sh /email
ADD _load.sql /email
ADD checkForConfirm.py /email
ADD myLib.py /email
ADD publib.py /email
ADD pubScribPub.py /email
ADD pubScribWaitForMessageAndSend.py /email
ADD flatfile.csv /email


# docker build -t mchirico/email:latest .
# docker push  mchirico/email


# Chirico commands
# docker run -it --rm mchirico/email /bin/bash
#
# docker run -it --rm -v ~/.credentialsEmail:/root/.credentialsEmail mchirico/email /bin/bash




