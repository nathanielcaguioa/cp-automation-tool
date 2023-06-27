import boto3
import csv
import sys
import os
import pandas as pd

inputToolAction = os.environ['ToolAction']
inputServerType = os.environ['HotfixId_2019']
print(inputToolAction)
if(inputServerType):
  print(type(inputServerType))

else:
  print("No value")
  
