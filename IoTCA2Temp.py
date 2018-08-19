import json
import sys
import time
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Docs OAuth credential JSON file
GDOCS_OAUTH_JSON = '/home/pi/Desktop/IoTCA2-dt-temperature-47369201d8b8.json'
 
# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'IoTCA2 Temperature Record DT'

temp = sys.argv[1]

def login_open_sheet(oauth_key_file, spreadsheet):
  try:
    scope =  ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open(spreadsheet).sheet1
    return worksheet
  except Exception:
    sys.exit(1)


worksheet = None

if worksheet is None:
    worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

try:
    worksheet.append_row((datetime.datetime.now(), temp))
except:
    worksheet = None