#!/usr/bin/env python
"""
Reference:
https://googlecloudplatform.github.io/gcloud-python/latest/bigquery-usage.html

Maybe need to fix more documentation:




"""



from gcloud import bigquery
from gcloud.bigquery import SchemaField

import myauth
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = myauth.getKey()

client = bigquery.Client()
dataset = client.dataset('Email')
if not dataset.exists():
    dataset.create()
    #dataset.delete()

table = dataset.table(name='email')

#table = dataset.table(TABLE_NAME, SCHEMA)
#table.create()         

table.schema = [SchemaField('email', 'STRING', mode='required'),
                SchemaField('subject', 'STRING', mode='required'),
                SchemaField('msg', 'STRING', mode='required'),
                SchemaField('id', 'STRING', mode='required'),    
                ]




job = client.load_table_from_storage('load-from-storage-job2', table, 'gs://pigpub/flatfile.csv')
job.source_format = 'CSV'
job.skip_leading_rows = 1
job.print_header = True
#job.write_disposition = 'truncate'
job.begin()
job.created
job.state


# Ref: https://googlecloudplatform.github.io/gcloud-python/latest/bigquery-usage.html
query = """\
SELECT 
 FROM dataset_name.persons
"""


ROWS_TO_INSERT = [
            (u'mchirico@gmail.com', u'This is a sample subject',u'Hi Mike:\r\r This is a test\r\rEnd',u'01'),
            (u'mike.chirico@cwxstat.com', u'This is a sample subject',u'Hi Mike:\r\r This is a test\r\rEnd',u'01'),    

        ]

table.insert_data(ROWS_TO_INSERT)
