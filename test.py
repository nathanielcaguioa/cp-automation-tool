import boto3
import csv
import sys
import os
import pandas as pd

def envVarCheck(envVar):
  print(envVar)
  if envVar == ',':
    envVar = "NA"
  else:
    envVar = os.environ[envVar]

  envVar = (envVar[:-1])
  return envVar

inputToolAction = os.environ['Execution']
inputServiceCheck = os.environ['Service Check']
inputServerType = os.environ['Server Type']
inputServiceName = os.environ['ServiceName']
inputHotfix2012 = os.environ['HotfixId2012']
inputHotfix2019 = os.environ['HotfixId2012']

inputServiceName = envVarCheck('ServiceName')
inputHotfix2012 = envVarCheck('HotfixId2019')
inputHotfix2019 = envVarCheck('HotfixId2012')

print(inputServiceName)
print(inputHotfix2012)
print(inputHotfix2019)

#Env_new = envVarCheck('HotfixId2019')
#Env_old = envVarCheck('HotfixId2012')
#print(Env_old)
#print(Env_new)





