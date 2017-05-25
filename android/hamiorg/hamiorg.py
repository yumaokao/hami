# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import re
import os
# import time
import json
import requests
import schedule
import httplib2

from functools import reduce

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools


class Hamiorg:
    APPLICATION_NAME = 'hamiorg'
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = 'https://www.googleapis.com/auth/drive'
    KEEP_LAST = 360
    KEEP_LAST_MAGS = 180

    def __init__(self):
        storage = Storage('credentials.json')
        credentials = storage.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, storage)
            if credentials:
                storage.put(credentials)

        http = credentials.authorize(httplib2.Http())
        self.service = build('drive', 'v3', http=http)
        self.org_dirs = ['全部', '最新', '最新/雜誌', '最新/報紙', '最新/書籍', '類別']
        self.org_dir_ids = {}
        self.bookid_re = re.compile('-(?P<bookid>\d{10}).pdf$')
        self.bookdata_re = re.compile('var _BOOK_DATA = (?P<bookdata>.*);')
        # self.seriesname_re = re.compile('')

    def __call__(self):
        self.hamiorg()
        # quota = self.about_quota()
        # print(quota)

    def _mkdirp_adir(self, prefix, adir):
        dbnames = os.path.split(adir)
        # print(dbnames)
        if not dbnames[0] == '':
            prefix = self._mkdirp_adir(prefix, dbnames[0])

        qbase = "mimeType='application/vnd.google-apps.folder' and '{}' in parents and name='{}'"
        fields = 'nextPageToken, files(id, name)'
        q = qbase.format(prefix, dbnames[1])
        alldirs = self.service.files().list(q=q, spaces='drive', fields=fields).execute().get('files', [])
        if len(alldirs) > 1:
            raise ValueError('there are more than one hami dirs')

        if len(alldirs) == 0:
            ndir = {'mimeType': 'application/vnd.google-apps.folder',
                    'name': dbnames[1], 'parents': [prefix]}
            cdir = self.service.files().create(body=ndir, fields='id').execute()
            return cdir['id']
        else:
            return alldirs[0]['id']

    def mkdirp_org_dirs(self, adirs=None):
        mdirs = self.org_dirs if adirs is None else adirs
        prefix = self.hamis['id']
        org_dir_ids = {d: self._mkdirp_adir(prefix, d) for d in mdirs}
        self.org_dir_ids = org_dir_ids
        print(org_dir_ids)

        return self

    def get_book_info(self, b):
        match = self.bookid_re.search(b['name'])
        if match is None:
            raise ValueError('Error RE bookid; {}'.format(b['name']))
        bookid = match.group('bookid')
        url = ('http://bookstore.emome.net/reader/viewer?type=own&book_id={}&pkgid=PKG_10001'.format(bookid))
        r = requests.get(url)
        match = self.bookdata_re.search(r.text)
        if match is None:
            return {}

        binfo = json.loads(match.group('bookdata'))
        keys = ['book_id', 'book_name', 'book_author', 'book_cp', 'book_isbn_name', 'book_category_name',
                'format', 'book_cover_large', 'book_releaseTime_t', 'modified_date', 'modified_date_t']
        if len(list(filter(lambda k: k not in binfo, keys))) > 0:
            return {}
        return {k: binfo[k] for k in keys}

    def _add_parent(self, b, pid):
        fields = 'id, name, parents, createdTime'
        if pid not in b['parents']:
            print('push book into')
            nb = self.service.files().update(fileId=b['id'], addParents=pid,
                                             fields=fields).execute()
            return nb
        else:
            return b

    def _remove_parent(self, b, pid):
        fields = 'id, name, parents, createdTime'
        if pid in b['parents']:
            print('pull book out')
            nb = self.service.files().update(fileId=b['id'], removeParents=pid,
                                             fields=fields).execute()
            return nb
        else:
            return b

    def list_books(self, pids=None):
        parentids = pids if pids is not None else [self.hamis['id']]
        qbase = "mimeType!='application/vnd.google-apps.folder' and '{}' in parents"
        fields = 'nextPageToken, files(id, name, parents, createdTime)'

        def _list_books_in_dir(pid):
            q = qbase.format(pid)
            page_token = None
            books = []
            while True:
                response = self.service.files().list(q=q, spaces='drive', pageToken=page_token,
                                                     orderBy='createdTime desc',
                                                     fields=fields).execute()
                books.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
            return books

        bookss = [_list_books_in_dir(pid) for pid in parentids]
        books = reduce(lambda x, y: x.extend(y), bookss)

        # print(books)
        # print(len(books))
        return books

    def find_hamis_dir(self):
        hamisdirs = self.service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='hamis'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)').execute().get('files', [])
        if len(hamisdirs) != 1:
            raise ValueError('there are more than one hami dirs')

        self.hamis = hamisdirs[0]

        return self

    def org_books_in_recent(self):
        books = self.list_books([self.org_dir_ids['最新']])
        print(len(books))

        # make sure in all
        for b in books:
            self._add_parent(b, self.org_dir_ids['全部'])

        # keep lastest
        for b in books[self.KEEP_LAST:]:
            self._remove_parent(b, self.org_dir_ids['最新'])

        for b in books[:120]:
            b.update(self.get_book_info(b))
            if b['book_category_name'] == '雜誌-報紙':
                self._add_parent(b, self.org_dir_ids['最新/報紙'])
            elif b['book_category_name'].startswith('雜誌-'):
                self._add_parent(b, self.org_dir_ids['最新/雜誌'])
            elif b['book_category_name'].startswith('書籍-'):
                self._add_parent(b, self.org_dir_ids['最新/書籍'])
            else:
                pass

        for r in ['最新/報紙', '最新/雜誌', '最新/書籍']:
            rbooks = self.list_books([self.org_dir_ids[r]])
            for b in rbooks:
                self._add_parent(b, self.org_dir_ids['全部'])
            for b in rbooks[self.KEEP_LAST_MAGS:]:
                self._remove_parent(b, self.org_dir_ids[r])

    def _series_name(self, b):
        print(b['book_name'])
        if b['book_isbn_name'] is not None:
            return b['book_isbn_name']
        bname = b['book_name']
        n = bname.split(' ')[0]
        if n[0] == '.':
            n = n[1:]
        return n

    def org_books_in_all(self):
        books = self.list_books([self.org_dir_ids['全部']])
        print(len(books))

        for b in books[:40]:
            b.update(self.get_book_info(b))
            # bname = b['book_isbn_name'] if b['book_isbn_name'] is not None else b['book_cp']
            # adir = '/'.join([b['book_category_name'], bname])
            print(self._series_name(b))

    def hamiorg(self):
        # get self.org_books
        self.find_hamis_dir().mkdirp_org_dirs()

        # org '最新'
        self.org_books_in_recent()

        # '全部'
        # self.org_books_in_all()

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
