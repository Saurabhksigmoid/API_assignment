from pathlib import Path
import requests
import json
from collections import defaultdict
#from xlsxwriter.workbook import Workbook
import datetime
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail
from datetime import datetime
#from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64
import smtplib
from email.mime.text import MIMEText

from_date_payload = "2022-09-05T00:00:00+00:00"
to_date_payload = "2022-09-12T23:59:59+00:00"
# from_date = "2022-09-08T00:00:00+00:00"
# to_date = "2022-08-31T23:59:59.000Z"
# cost_min_by_rg = 10
# cost_max_by_rg = 100000
# resource_min_cost = 10
subscription_id ='subscription_id'
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuYXp1cmUuY29tLyIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0Lzk1ZTY2ZWNjLWYyYzItNDY0Yi04NGQ5LThmZGE0MDdiYzkyMy8iLCJpYXQiOjE2NzQ2NTEwMzYsIm5iZiI6MTY3NDY1MTAzNiwiZXhwIjoxNjc0NjU0OTM2LCJhaW8iOiJFMlpnWU1neE1KUmNOTjlRcG1UUDFzN0w4bE5NQUE9PSIsImFwcGlkIjoiZDQ4YWQyNDUtNTAyNi00NmUwLWJlYTgtYjMyYjcxMjM2MDZlIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM"
}

payload = json.dumps({
            "type": "ActualCost",
            "dataSet": {
                "granularity": "Daily",
                "aggregation": {
                "totalCost": {
                    "name": "Cost",
                    "function": "Sum"
                }
                },
                "sorting": [
                {
                    "direction": "descending",
                    "name": "UsageDate"
                }
                ],
                "grouping": [
                {
                    "type": "Dimension",
                    "name": "SubscriptionName"
                }
                ]
            },
            "timeframe": "Custom",
            "timePeriod": {
                "from": from_date_payload,
                "to": to_date_payload
            }
            })
            
url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.CostManagement/query?api-version=2021-10-01".format(
            subscription_id)
        # url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.CostManagement/Query?api-version=2019-11-01".format(subscription_id)
response = requests.request("POST", url, headers=headers, data=payload)
out = json.loads(response.text)
final_response = {}
final_response['rows'] = out["properties"]['rows']
todays_cost = out["properties"]['rows'][0][0]
same_day_last_weeks_cost = out["properties"]['rows'][-1][0]
final_response['rows'] = out["properties"]['rows']
final_response['cost_change'] = [((todays_cost - same_day_last_weeks_cost)/same_day_last_weeks_cost)*100]


# Create the email message
msg = MIMEText(final_response)
msg['Subject'] = 'Azure Monitoring'
msg['From'] = 'saurabh.kambli@sigmoidanalytics.com'
msg['To'] = 'smansi@sigmoidanalytics.com'

# Send the email
server = smtplib.SMTP('smtp.example.com')
server.sendmail('saurabh.kambli@sigmoidanalytics.com', 'smansi@sigmoidanalytics.com', msg.as_string())
server.quit()