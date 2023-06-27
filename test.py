import boto3
import csv
import sys
import os
import pandas as pd

inputToolAction = os.environ['Execution']
inputServiceCheck = os.environ['Service Check']
#inputServiceType = os.environ['Server Type']
mandatory_env_var = ["HotfixId_2019", "HotfixId_2012", "Service Name"]
default_value="NA"
print(inputToolAction)
print(inputServiceCheck)

print(os.environ.get('HotfixId_2019', default_value))
print(os.environ.get('HotfixId_2012', default_value))

