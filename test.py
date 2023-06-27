import boto3
import csv
import sys
import os
import pandas as pd

def envVarCheck(envVar):
  print(envVar)
  if envVar in os.environ:
    envVar = os.environ[envVar]
  else:
    envVar = "NA"
    
  return envVar

inputToolAction = os.environ['Execution']
inputServiceCheck = os.environ['Service Check']
inputServerType = os.environ['Server Type']
inputHotfix2012 = os.environ['HotfixId2012']
inputHotfix2019 = os.environ['HotfixId2019']
print(inputToolAction)
print(inputHotfix2012)
print(inputHotfix2019)



#server = os.environ.get('HotfixID_2012', 'youtube.com')
#server2 = os.environ.get('HotfixID_2019', 'NA')

Env_new = envVarCheck('HotfixId2019')
Env_old = envVarCheck('HotfixId2012')
print(Env_old)
print(Env_new)





