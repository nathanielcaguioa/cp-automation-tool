import boto3
import csv
import sys
import os
import time
import pandas as pd

def mainFunction():

    csvFile = os.environ['Server List - CSV']
    mainList = sortServerList(csvFile)

    for index, mainServerList in enumerate(mainList):
        if index == 0:
            sendCommandSettings(mainServerList,'us-east-1')
        elif index == 1:
            sendCommandSettings(mainServerList,'us-west-2')
        elif index == 2:
            sendCommandSettings(mainServerList,'ca-central-1')
        elif index == 3:
            sendCommandSettings(mainServerList,'eu-central-1')
        elif index == 4:
            sendCommandSettings(mainServerList,'eu-west-1')
        elif index == 5:
            sendCommandSettings(mainServerList,'ap-southeast-1')
        elif index == 6:
            sendCommandSettings(mainServerList,'ap-southeast-2')
            
def sendCommandSettings(sendServerList,sendRegion):
    if not sendServerList:
        print ("No server provided in this region: " + sendRegion)
    else:
        setSSMCommandSetting(sendServerList,sendRegion)


def envVarCheck(envVar):
  if envVar == ',':
    envVar = "NA"
  else:
    envVar = os.environ[envVar]

  envVar = (envVar[:-1])
  return envVar

def setSSMCommandSetting(set_serverlist,setRegion):

    from datetime import date
    inputToolAction = os.environ['Execution']
    setDocument = 'sre-infra-automationtool'
    ssm_client = boto3.client('ssm',region_name=setRegion)
    runToday = date.today()
    runToday = runToday.strftime("%d%m%Y")
    

    for i in range(0, len(set_serverlist), 30):
        limited_serverlist = set_serverlist[i : i + 30]
        print(limited_serverlist)
        if inputToolAction == 'Restart Action':
            setCommandId = fnRebootServer(limited_serverlist,ssm_client,runToday,setDocument)
        elif inputToolAction == 'Windows Update Health Check Action':
            setCommandId = fnCheckWindowsUpdate(limited_serverlist,ssm_client,runToday,setDocument)
        elif inputToolAction == 'Service Action':
            setCommandId = fnActionService(limited_serverlist,ssm_client,runToday,setDocument)
    
        #Checking status of command
        checkCommandStatus(curSession=ssm_client,commandId=setCommandId,instances=limited_serverlist)
        print("Printing output...")
        #printing output
        for instance in limited_serverlist:
            output = ssm_client.get_command_invocation(CommandId=setCommandId,InstanceId=instance)
            results = str(output['StandardOutputContent'])
            instanceIDresult = str(output['InstanceId']) 
            commandIDresult = str(output['CommandId'])          
            print("Instance ID: " + instanceIDresult + "\nCommand ID: " + commandIDresult + "\n" + results)


def sortServerList(sortCSVfile):
    inputServerType = os.environ['Server Type']
    filter_df = pd.read_csv(sortCSVfile)
    sortServerType = caseServerType(inputServerType)


    if sortServerType == "db-execute":
        filterProduct = filter_df.query('servertype.str.contains("DB|APFS|WEB")')
    elif sortServerType == "wadm-execute":
        filterProduct = filter_df.query('servertype.str.contains("WADM")')
    elif sortServerType == "app-execute":
        filterProduct = filter_df.query('servertype.str.contains("APP")')
    elif sortServerType == "all-execute":
        filterProduct = filter_df

    sortRegion = caseRegion(rowRegion)
    sortUSEAInstances = []
    sortUSWEInstances = []
    sortCACEInstances = []
    sortEUWEInstances = []
    sortEUCEInstances = []
    sortAPSPInstances = []
    sortAPAUInstances = []
    
    for index, row in filterProduct.iterrows():
        rowServerName = row['servername']
        rowInstanceId = row['instanceid']
        rowRegion = rowServerName[0:4]

        sortServerExist = verInstance(rowInstanceId,sortRegion)
        sortSSMStatus = verInstanceSSMStatus(rowInstanceId,sortRegion)
        if sortServerExist == "running" and sortSSMStatus == "Online":

            if rowRegion == "USEA":
                sortUSEAInstances.append(rowInstanceId)
            elif rowRegion == "USWE":
                sortUSWEInstances.append(rowInstanceId)
            elif rowRegion == "CACE":
                sortCACEInstances.append(rowInstanceId)
            elif rowRegion == "EUCE":
                sortEUCEInstances.append(rowInstanceId)
            elif rowRegion == "EUWE":
                sortEUWEInstances.append(rowInstanceId)
            elif rowRegion == "APSP":
                sortAPSPInstances.append(rowInstanceId)
            elif rowRegion == "APAU":
                sortAPAUInstances.append(rowInstanceId)
    sortList = [sortUSEAInstances, sortUSWEInstances, sortCACEInstances, sortEUCEInstances, sortEUWEInstances, sortAPSPInstances, sortAPAUInstances]
    return sortList

def verInstanceSSMStatus(verInstanceId,verRegion):
    ssm_client = boto3.client('ssm',region_name=verRegion)
    try:
        response = ssm_client.describe_instance_information(
            Filters=[{
                    'Key': 'InstanceIds',
                    'Values': [
                        verInstanceId,
                    ]
                }
            ]
        )
        return(response['InstanceInformationList'][0]['PingStatus'])
    except:
        print(verInstanceId + " there is a CONNECTION LOST in SSM. Cannot do RUNCommmand.")
        return ("An exception occurred")

def verInstance(verInstanceId,verRegion):
    
    try:
        ec2_client = boto3.client('ec2',region_name=verRegion)
        response = ec2_client.describe_instance_status(
            InstanceIds=[verInstanceId],
        )
        verStatus = (response['InstanceStatuses'][0]['InstanceState']['Name'])
        return verStatus
    except:
        print(verInstanceId + " has an issue with this instance.")
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
    if region == 'CACE':
        return "ca-central-1"
    elif region == 'EUWE':
        return "eu-west-1"
    elif region == 'EUCE':
        return "eu-central-1"     
    if region == 'APSP':
        return "ap-southeast-1"
    elif region == 'APAU':
        return "ap-southeast-2" 

        

def checkCommandStatus(curSession,commandId,instances):
    inProgress = True

    #If instances is not a list, convert it to a list

    if not isinstance(instances, list):
        instances = [instances]
    x = 0
    while x < 3:    
        ssmStatus = []
        #print("Waiting 5 seconds before checking status...")
        time.sleep(10)
        for ssmInstances in instances:
            #print(ssmInstances)
            output = curSession.get_command_invocation(
            CommandId=commandId,
            InstanceId=ssmInstances
            )
            ssmStatus.append(str(output['StatusDetails']))
            #print("Command ID: " + str(output['CommandId']) + " Instance: " + \
                #str(output['InstanceId']) + " Status: " + str(output['StatusDetails']))

        #Check back in 5 minutes to avoid hammering the commection with status requests
        if (ssmStatus != 'Success'):
            #print("Waiting 5 secs before checking back")
            time.sleep(5)
        else:
            break
        x=x+1
    

mainFunction()
