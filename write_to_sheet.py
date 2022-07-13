import os
from random import randrange

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from app import creds
from app.creds.constants import SHEET_ID


"""
Эта ветка для Видео о записи в электронные таблицы Google Sheets
с помощью API Google Sheets 
https://youtu.be/RV-aN_WEFPE
"""

def get_service_simple():
    return build('sheets', 'v4', developerKey=creds.api_key)


def get_service_sacc():
    """
    Могу читать и (возможно) писать в таблицы кот. выдан доступ
    для сервисного аккаунта приложения
    sacc-1@privet-yotube-azzrael-code.iam.gserviceaccount.com
    :return:
    """
    creds_json = os.path.dirname(__file__) + "/creds/creds.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


sheet = get_service_sacc().spreadsheets()


# https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/sheets_v4.spreadsheets.html
def get_values():
    # values = [[randrange(10, 99)]]    # ячейка
    # values = [[randrange(10, 99) for _ in range(0, 6)]]   # строка данных
    # values = [[randrange(10, 99)] for _ in range(0, 3)]    # колонка данных
    values = [[randrange(10, 99) for _ in range(0, 3)] for _ in range(0, 3)]    # записываем матрицу 3х3
    return values


# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
'''resp = sheet.values().update(
    spreadsheetId=sheet_id,
    range="Лист2!H1",
    valueInputOption="RAW",
    body={'values' : get_values() }).execute()'''


# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
resp = sheet.values().append(
     spreadsheetId=SHEET_ID,
     range="Лист1!A1",
     valueInputOption="RAW",     # аргумент, который отвечает за то, как будут парсится вставленные данные
     # insertDataOption="INSERT_ROWS",     # Есть разница и ее легко увидеть , заполнив таблицу [(1,1,1),(1, ,1),(1,1,1)] , т.е. ячейка B2 свободна и вставлять массив 3*3 в нее. insert_rows - вставит 3 строки целиком, сместив низ таблицы, а OVERWRITE - вставит ровно в B2 а все правее и ниже перезапишет.
     body={'values' : get_values() }).execute()


# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate
# body = {
#     'valueInputOption' : 'RAW',
#     'data' : [
#         {'range' : 'Лист2!D2', 'values' : get_values()},
#         {'range' : 'Лист2!H4', 'values' : get_values()}
#     ]
# }

# resp = sheet.values().batchUpdate(spreadsheetId=sheet_id, body=body).execute()


print(resp)
