import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from app import creds
from app.creds.constants import SHEET_ID


def get_service_simple():
    """Читаем только по api_key"""
    return build('sheets', 'v4', developerKey=creds.api_key)


def get_service_sacc():
    """
    Читаем с помощью сервисного аккаунта
    """
    creds_json = os.path.dirname(__file__) + "/creds/creds.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())

    return build('sheets', 'v4', http=creds_service)


# service = get_service_simple()
service = get_service_sacc()
sheet = service.spreadsheets()


# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
# resp = sheet.values().get(spreadsheetId=sheet_id, range="Лист1!A1:A999").execute()

# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet
resp = sheet.values().batchGet(spreadsheetId=SHEET_ID, ranges=["Лист1", "Лист2"]).execute()   # батчевые методы, которые схлопывают в один запрос несколько действий

print(resp)
