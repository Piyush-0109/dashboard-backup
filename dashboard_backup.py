import os
import env
import json
import boto3
import shutil
import datetime
from datadog import initialize, api

# DATADOG INITIALIZATION
options = {
    'api_key': env.DATADOG_API_KEY,
    'app_key': env.DATADOG_APP_KEY
}

initialize(**options)

# API CALL TO GET ALL THE DASHBOARDS ID'S
try:
    apiResponse = api.Dashboard.get_all()
    dashbaordIdsList = [element["id"]
                        for element in apiResponse.get('dashboards')]
except:
    print("Error In Calling The API!!!")

# FORMATTING THE DATE WITH FORMAT ```DAY-MONTH_NAME-YEAR```
formattedDate = datetime.datetime.now().strftime("%d-%B-%Y")

# CREATING A FOLDER WITH TODAY'S DATE
workingDirectory = os.getcwd()  # gets the current working directory


# here formattedDate is the name of the folder i.e: current date
path = os.path.join(workingDirectory, formattedDate)

if os.path.isdir(path):
    shutil.rmtree(path)  # deletes the directory if already exsists

os.mkdir(path)  # creates a directory

for i in dashbaordIdsList:
    try:
        # API call to datadog for getting single dashboard data
        dashboardData = api.Dashboard.get(i)
        fileTitle = dashboardData.get('title')
        formattedFileTitle = fileTitle.replace(" ", "")
        file_name = formattedFileTitle+".json"

        # Creating file with application name to store the json data
        with open(file_name, 'w') as fp:
            fp.write(json.dumps(dashboardData))
            shutil.move(workingDirectory+"/"+file_name, path+"/"+file_name)
            pass
    except:
        print("Error in calling the API!!!")

shutil.make_archive(formattedDate, 'zip', path)  # Compressing the Folder

fileToUpload = formattedDate+".zip"

# AWS INITIALIZATION TO UPLOAD THE FILE TO S3 Bucket
session = boto3.Session(
    aws_access_key_id=env.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
)
s3 = session.resource('s3')
s3.meta.client.upload_file(
    Filename=fileToUpload, Bucket=env.S3_BUCKET_NAME, Key=fileToUpload
)

# DELETING THE CREATED FILE
if os.path.exists(fileToUpload):
    os.remove(fileToUpload)
else:
    print("The file does not exist!!!")

if os.path.exists(path):
    shutil. rmtree(path)
else:
    print("The file does not exist!!!")
