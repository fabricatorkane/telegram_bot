import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os

sheet_id = '1LE10RehEQPon2bcAvr3CnYmyZM3Np2EP8P5KF9ZcuPM'


def get_service_sacc():
    '''
    Могу читать и (возможно) писать в таблицы кот. выдан доступ
    для сервисного аккаунта приложения
    sacc-1@privet-yotube-azzrael-code.iam.gserviceaccount.com
    '''
    creds_json = os.path.dirname(__file__) + "/creds/creds.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


sheet = get_service_sacc().spreadsheets()


def write_out_to_googlesheet(user_data, user_telegram):
    values = []
    values.append(user_telegram)
    values.append(user_data.get('user_name'))     # вот тут бы просто перебрать, а не говнякать хардкодом
    values.append(user_data.get('user_application'))
    resp = sheet.values().append(
                spreadsheetId=sheet_id,
                range="Лист1!A1",
                valueInputOption="RAW",
                body={'values': [values]}).execute()
