import boto3
import csv
import sys
import os
import pandas as pd

def mainFunction():

    csvFile = 'cp-automation-tool-server-list.csv'
    main_USEA_list, main_USWE_list = sortServerList(csvFile)

    print(main_USEA_list)
    print(main_USWE_list)
    if not main_USEA_list:
        print ("No USEA server in the list.")
    else:
        #setSSMCommandSetting(main_USEA_list,'us-east-1')
        print("USEA")
    
    if not main_USWE_list:
        print ("No USWE server in the list.")
    else:
        print("USWE")
        #setSSMCommandSetting(main_USWE_list,'us-west-2')

def envVarCheck(envVar):
  print(envVar)
  if envVar == ',':
    envVar = "NA"
  else:
    envVar = os.environ[envVar]

  envVar = (envVar[:-1])
  return envVar

def setSSMCommandSetting(set_serverlist,setRegion):

    from datetime import date
    inputToolAction = os.environ['Execution']
    setDocument = 'cp-automationtool'
    ssm_client = boto3.client('ssm',region_name=setRegion)
    runToday = date.today()
    runToday = runToday.strftime("%d%m%Y")


    if inputToolAction == 'Restart Action':
        setCommandId = fnRebootServer(set_serverlist,ssm_client,runToday,setDocument)
    elif inputToolAction == 'Windows Update Health Check Action':
        setCommandId = fnCheckWindowsUpdate(set_serverlist,ssm_client,runToday,setDocument)
    elif inputToolAction == 'Services Action':
        setCommandId = fnActionService(set_serverlist,ssm_client,runToday,setDocument)

    print(setCommandId)


def sortServerList(sortCSVfile):
    inputServerType = os.environ['Server Type']
    filter_df = pd.read_csv(sortCSVfile)
    sortServerType = caseServerType(inputServerType)


    if sortServerType == "db-execute":
        filterProduct = filter_df.query('servertype.str.contains("DB|APFS|Web")')
    elif sortServerType == "wadm-execute":
        filterProduct = filter_df.query('servertype.str.contains("WADM")')
    elif sortServerType == "app-execute":
        filterProduct = filter_df.query('servertype.str.contains("APP")')
    elif sortServerType == "all-execute":
        filterProduct = filter_df

    sortUSEAInstances = []
    sortUSWEInstances = []


    for index, row in filterProduct.iterrows():
        rowServerName = row['servername']
        rowInstanceId = row['instanceid']
        rowRegion = rowServerName[0:4]

        sortRegion = caseRegion(rowRegion)

        sortServerExist = verInstance(rowInstanceId,sortRegion)
        if sortServerExist == "OKAY" and rowRegion == "USEA":
            sortUSEAInstances.append(rowInstanceId)
        elif sortServerExist == "OKAY" and rowRegion == "USWE":
            sortUSWEInstances.append(rowInstanceId)
    
    return sortUSEAInstances,sortUSWEInstances
    


def verInstance(verInstanceId,verRegion):
    
    try:
        ec2_client = boto3.client('ec2',region_name=verRegion)
        response = ec2_client.describe_instance_status(
            InstanceIds=[verInstanceId],
        )
        return "OKAY"
    except:
        return ("An exception occurred")


def filterData(filterFile):
    filter_df = pd.read_csv(filterFile)
    filterInstances = []
    for index, row in filter_df.iterrows():
            
            rowServer = row['instanceid']
            filterInstances.append(rowServer)
    
    return filterInstances
def caseServerType(serverType):
    if serverType == 'DB - APFS - Web':
        return "db-execute"
    elif serverType == 'WADM':
        return "wadm-execute"
    elif serverType == 'APP':
        return "app-execute"     
    elif serverType == 'ALL':
        return "all-execute"   

def fnRebootServer(rbtInstanceId,rbtSession,rbtDate,rbtDocument):
    "test"
    rbtComment = ("Reboot Function" + "-" +rbtDate)
    rbtServiceAction = "CHECK"
    rbtServiceName = "NA"
    rbtHotfix2012 = "NA"
    rbtHotfix2019 = "NA"


    rbtCommandId=runSSMCommand("REBOOT",rbtInstanceId,rbtComment,rbtDocument,rbtSession,rbtServiceAction,rbtServiceName,rbtHotfix2012,rbtHotfix2019)
    return rbtCommandId

def fnActionService(actInstanceId,actSession,actDate,actDocument):
    inputServiceName = envVarCheck('ServiceName')
    inputServiceCheck = os.environ['Service Check']
    actHotfix2012 = "NA"
    actHotfix2019 = "NA"
    actComment = ("Service Function" + "-" +actDate)

    actCommandId=runSSMCommand("SERVICE",actInstanceId,actComment,actDocument,actSession,inputServiceCheck,inputServiceName,actHotfix2012,actHotfix2019)

    return actCommandId
    

def fnCheckWindowsUpdate(chkInstanceId,chkSession,chkDate,chkDocument):
    inputHotfix2012 = envVarCheck('HotfixId2012')
    inputHotfix2019 = envVarCheck('HotfixId2019')
    chkServiceAction = "CHECK"
    chkServiceName = "NA"

    chkComment = ("Windows Update Verification Function" + "-" +chkDate)

    chkCommandId=runSSMCommand("HOTFIX",chkInstanceId,chkComment,chkDocument,chkSession,chkServiceAction,chkServiceName,inputHotfix2012,inputHotfix2019)

    return chkCommandId




def runSSMCommand(runAction,runInstances,runComment,runDocument,curSession,runServiceAction,runServiceName,runHotfix2012,runHotfix2019):
    ssmResponse = curSession.send_command(
                    Targets=[{"Key": "InstanceIds", "Values": runInstances}],
                    Comment=runComment,
                    DocumentName=runDocument,
                    MaxConcurrency='100%',
                    Parameters={'ToolAction':[runAction],'ServiceAction':[runServiceAction],'ServiceNames':[runServiceName],'Hotfixwin2012':[runHotfix2012],'Hotfixwin2019':[runHotfix2019]
                                },
                    MaxErrors='100%',
                    TimeoutSeconds=900)

    return ssmResponse['Command']['CommandId']


def caseRegion(region):
    if region == 'USEA':
        return "us-east-1"
    elif region == 'USWE':
        return "us-west-2"
    elif region == 'ALL':
        return "all"     
    

mainFunction()
