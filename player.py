import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_players():

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Jeopardy Mailbox Players').sheet1
    return sheet.get_all_records()
