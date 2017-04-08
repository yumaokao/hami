# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import time
import schedule
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools


class Hamiorg:
    APPLICATION_NAME = 'hamiorg'
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = 'https://www.googleapis.com/auth/drive'

    def __init__(self):
        storage = Storage('credentials.json')
        credentials = storage.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, storage)
            if credentials:
                storage.put(credentials)

        http = credentials.authorize(httplib2.Http())
        self.service = build('drive', 'v3', http=http)

    def __call__(self):
        results = self.service.about().get(fields='kind, storageQuota').execute()
        print(results.get('storageQuota'))

        '''
        print(service.about().get(fields='kind, storageQuota').execute().get('kind'))
        results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        print(items)
        '''


def main():
    org = Hamiorg()
    schedule.every().hours.do(org)
    schedule.every().day.at("00:30").do(org)

    org()
    '''
    while True:
        schedule.run_pending()
        time.sleep(1)
    '''


if __name__ == "__main__":
    main()
