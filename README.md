# Email RESTful API System


This is a possible option to the following [Technical Interview Questions](https://gist.github.com/davisshaver/3ea536accc8b7611d34e67699036d8b8#file-engineer-md)

However, let's change some of the requirements:

First, we'll assume that this is a real requirement. It's not an interview question, which changes things. That means, it's a good untested idea.  And, without quickly getting a working prototype up and running, we'll have now way to test ideas out on users.  Plus, proof of concept is very important.  Also, it goes without saying, since it's an email system (even the prototype) security is a top concern and so is sharing this working prototype with untrusted 3rd parties.

### Adding the following requirements

* Assume this isn't an interview question, but a real problem (That changes things).
* Build a working prototype in a matter of hours.
* Security is a high concern with the working prototype (Assume it's really going to be used). 
* Demonstrate how 10,000+ emails can be delivered per day; however, verify 300 per day.
* Prototype must be available as a Docker image (other people need to try out ideas). Plus, we don't want to waste a lot of time getting someone up-to-speed on how to run this design.
* The prototype must be decoupled.  We'll make parts of this prototype decoupled leveraging Pub/Sub.  Hence any part could be done in any language, they would just need to be able to communicate with the Pub/Sub system.
* We need to collect responses -- can't just send out email (that's spamy). Need to put in interactive hooks.


### Relaxing the following requirements

* We don't care about code design -- that has to be working within a few hours, it will be a live working prototype; but, we're problem going to throw away most of the code. 


## Software Used in Prototype

Google software was used in this prototype for the following reasons.

* We want the security of Gmail. Note (custom domains could be used).
* We want to leverage a secure, reliable Pub/Sub system, where we can allocate, assign and or delete keys as needed.
* We want to prototype to be scaleable. Our year concern is working on unexpected peripheral issues. 



## Quick Verification

Running the docker image.

    ./runDocker.sh
    root@6b12a003e50d: ./pubScribPub.py  # This send messages (not email yet), into the cloud
    root@6b12a003e50d: ./pubScribWaitForMessageAndSend.py  # This will receive message from the cloud and send Email.

Okay, quick recap on the above.  We're not sure how we're going to get the content in an email.  It's going to be obtained through some RESTful API.  The *pubScribPub.py* will be used to collect that data. It can be run from anywhere -- Raspberry Pi, Docker Image on AWS, Mac OS.  This is a completely isolated Publish Scribe component, which has it's own security credentials on a secure.json file.  The key in this file only gives access to the Topic.  We're using Google's topic, so we don't have to worry about setup and ssl.

Also, since we're using a Pub/Scrib system, leverage fan-in or fan-out to produce more clients.  In fact, we could add 100's of subscribers.

### Continuing with commands

    root@6b12a003e50d: ./checkForConfirm.py  # Verify msg in cloud get received


We'll have a separate program *checkForConfirm.py* that verifies messages sent into the cloud were received at the other end.  Each message has an id, and we can put this id into a database.

    root@6b12a003e50d:  ./pull.py  # This program will pull down email responses


You can see a close up of some of the actual output in this[PDF].(https://github.com/mchirico/email/blob/master/docs/closeUpofProcesses.pdf)


# Issues

Google limits 2,000 emails per day, per account [Google Policy](https://support.google.com/a/answer/166852?hl=en); however, since this system is decoupled, several email accounts can be used.  Therefore, using 5 accounts, we could reach our goal of 10,000 emails per day.

Database?  It wasn't possible to complete a bigQuery working prototype in a few hours.  However, with an extra hour this is *VERY* possible.  You can see some of the raw code in *bigQuery.py*

The Docker example doesn't work for you... True. You'll need to setup your own security keys.  Note the Docker command to access these keys locally, without giving the whole world access.

    docker run -it --rm -v ~/.credentialsEmail:/root/.credentialsEmail mchirico/email /bin/bash  -c 'cd /email && /bin/bash' 

    






