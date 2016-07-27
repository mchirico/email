#!/usr/bin/env python2
"""


"""
from __future__ import print_function
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


import uuid


try:
    import subprocess
except ImportError:
    pass

try:
    import shlex
except ImportError:
    pass


import os,time,sys,signal,getopt,popen2,re,glob


import errno
def Mkdir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass




def signal_handler(signal, frame):
        sys.exit(0)



class LOG():
      def __init__(self,file='logfile'):
          self.file=file
      def Open(self,FILE=""):
          if FILE != "":
              self.file=FILE
          self.f=open(self.file,'w')
# Below...add your own stuff
      def SplitOpen(self,FILE):
          m=FILE.split('_')
          self.file="./result/parse."+m[1]+"."+m[-1].split('.')[0]
          self.Open()
      def Write(self,s):
          self.f.write(s+'\n')
      def Close(self):
          self.f.close()


log=LOG()




def Open(FILE):
    f=open(FILE)
    m=f.readlines()
    f.close()
    m=[i.strip().split() for i in m]
    return m



# Runs ssh command
def runcmd(N,len=0):
    scmd=N
    if hasattr(popen2,'popen3'):    
	    r,w,e = popen2.popen3(scmd)
	    m=r.readlines()
	    e.readlines()
	    r.close()
	    e.close()
	    w.close()
	    return [os.getpid(),m]
    else:
            sscmd=shlex.split(scmd)
            r,e = subprocess.Popen(sscmd,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
            return [os.getpid(),[r]]





def main(N):
	print("program "+sys.argv[0]+" called with "+str(len(sys.argv)) +" parameters")
	if len(sys.argv) > 1:
		print(sys.argv)
		print(runcmd("uptime"))
                files=glob.glob(sys.argv[1])
                for file in files:
                    print(file)


if __name__ == '__main__':
        signal.signal(signal.SIGINT, signal_handler)
        main(sys.argv)
