import boto3
import csv
import sys
import os
import pandas as pd

from os import environ
inputToolAction = os.environ['Execution']
inputServiceCheck = os.environ['Service Check']
print(inputToolAction)
print(inputServiceCheck)
REQUIRED_ENV_VARS = {"HotfixId_2019", "HotfixId_2012"}
diff = REQUIRED_ENV_VARS.difference(environ)
if len(diff) > 0:
    raise EnvironmentError(f'Failed because {diff} are not set')
