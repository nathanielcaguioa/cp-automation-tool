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
inputServiceName = (os.environ['ServiceName'][:-1])
inputHotfix2012 = (os.environ['HotfixId2012'][:-1])
inputHotfix2019 = (os.environ['HotfixId2012'][:-1])

#Env_new = envVarCheck('HotfixId2019')
#Env_old = envVarCheck('HotfixId2012')
#print(Env_old)
#print(Env_new)





