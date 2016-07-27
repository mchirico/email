#!/bin/bash
docker run -it --rm -v ~/.credentialsEmail:/root/.credentialsEmail mchirico/email /bin/bash  -c 'cd /email && /bin/bash'
