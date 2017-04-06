# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import time
import schedule
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools


APPLICATION_NAME = 'hamiorg'
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = 'https://www.googleapis.com/auth/drive'

client_id = "1037484691223.apps.googleusercontent.com"
client_secret = "oyJtlM6GhYvBQFvxstqLnDFI"


def hamiorg():
    storage = Storage('credentials.json')
    credentials = storage.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, storage)
        if credentials:
            storage.put(credentials)

    http = credentials.authorize(httplib2.Http())
    service = build('drive', 'v3', http=http)


def main():
    schedule.every().hours.do(hamiorg)
    schedule.every().day.at("00:30").do(hamiorg)
    schedule.every().day.at("07:30").do(hamiorg)
    schedule.every().day.at("08:30").do(hamiorg)
    schedule.every().day.at("16:30").do(hamiorg)
    schedule.every().day.at("17:30").do(hamiorg)

    hamiorg()
    '''
    while True:
        schedule.run_pending()
        time.sleep(1)
    '''


if __name__ == "__main__":
    main()
