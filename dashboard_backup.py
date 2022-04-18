import os
import json
import env
import boto3
import datetime
from datadog import initialize, api

# TO GET CURRENT DATE
currentDate = datetime.datetime.now()

# FORMATTING THE DATE WITH FORMAT ```DAY-MONTH_NAME-YEAR```
formattedDate = currentDate.strftime("%d-%B-%Y")

# FILENAME WITH FORMAT ```CurrentDate.json```
filename = formattedDate+".json"

# DATADOG API-KEY and APP-KEY
options = {
    'api_key': env.DATADOG_API_KEY,
    'app_key': env.DATADOG_APP_KEY
}

# PASSING THE ARGUMENTS
initialize(**options)

# API CALL TO GET ALL THE DASHBOARDS
apiResponse = api.Dashboard.get_all()

# CREATING A FILE TO STORE THE RESPONSE
with open(filename, 'w') as convert_file:
    convert_file.write(json.dumps(apiResponse))

# AWS INITIALIZATION TO UPLOAD THE FILE TO S3 Bucket
session = boto3.Session(
    aws_access_key_id=env.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
)
s3 = session.resource('s3')
s3.meta.client.upload_file(
    Filename=filename, Bucket=env.S3_BUCKET_NAME, Key=filename
)

# DELETING THE CREATED FILE
if os.path.exists(filename):
    os.remove(filename)
else:
    print("The file does not exist!!!")
