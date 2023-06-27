import boto3
import csv
import sys
import os
import pandas as pd

inputToolAction = os.environ['Execution']
inputServiceCheck = os.environ['Service Check']
print(inputToolAction)
print(inputServiceCheck)
if 'HotfixId_2019' in os.environ:
    print('Environment variable exists!')
else:
    print('Environment variable does not exist.')
