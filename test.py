import boto3
import csv
import sys
import os
import pandas as pd

inputToolAction = os.environ['Execution']
inputServiceCheck = os.environ['Service Check']
inputServerType = os.environ['Server Type']
default_value="NA"
print(inputToolAction)
print(inputServerType)

#inputHotfix2012 = (os.environ.get(['HotfixID_2012']))
#inputHotfix2019 = (os.environ.get(['HotfixID_2019']))

server = os.environ.get('HotfixID_2012', 'youtube.com')
server2 = os.environ.get('HotfixID_2019', 'NA')


print(server)
print(server2)
