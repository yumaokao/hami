# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import re
import time
import json
import requests
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
        self.bookid_re = re.compile('-(?P<bookid>\d{10}).pdf$')
        self.bookdata_re = re.compile('var _BOOK_DATA = (?P<bookdata>.*);')

    def __call__(self):
        self.hamiorg()
        quota = self.about_quota()
        print(quota)

    def get_book_info(self, bookid):
        url = ('http://bookstore.emome.net/reader/viewer?type=own&book_id={}&pkgid=PKG_10001'.format(bookid))
        r = requests.get(url)
        match = self.bookdata_re.search(r.text)
        if match is None:
            return {}
        return json.loads(match.group('bookdata'))

    def org_books(self, books):
        for b in books:
            print(b)
            match = self.bookid_re.search(b['name'])
            if match is None:
                print('Error RE bookid; {}'.format(b['name']))
                continue
            bookid = match.group('bookid')
            print(bookid)
            bookinfo = self.get_book_info(bookid)
            print(bookinfo)
            break

    def list_books_in_hamis(self, hamis):
        q="mimeType!='application/vnd.google-apps.folder' and '{}' in parents".format(hamis['id'])

        books = []
        page_token = None
        while True:
            response = self.service.files().list(q=q, spaces='drive', pageToken=page_token,
                                                 fields='nextPageToken, files(id, name)').execute()
            books.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return books

    def find_hamis_dir(self):
        hamisdirs = self.service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='hamis'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)').execute().get('files', [])
        if len(hamisdirs) == 1:
            return hamisdirs[0]
        return []

    def hamiorg(self):
        hamis = self.find_hamis_dir()
        books = self.list_books_in_hamis(hamis)
        orged_books = self.org_books(books)

    def about_quota(self):
        results = self.service.about().get(fields='kind, storageQuota').execute()
        return results.get('storageQuota')


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
