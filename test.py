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

inputHotfix2012 = (os.environ.get('HotfixId_2019'))
inputHotfix2019 = (os.environ.get('HotfixId_2012'))

print(inputHotfix2012)
print(inputHotfix2019)
