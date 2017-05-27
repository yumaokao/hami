# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import re
import os
# import time
import json
import argparse
import requests
import schedule
import httplib2
import concurrent.futures

import magsname

from functools import reduce

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools


VERSION = '0.2.0'


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
        print("----")
        print("[{}] - [{}][{}]".format(b['book_name'], b['book_category_name'], b['book_isbn_name']))

        # isbn_name is the best
        if b['book_isbn_name'] is not None:
            return b['book_isbn_name']

        # if it's a book, just return without '.'
        if b['book_category_name'].startswith('書籍-'):
            return re.sub(r'^\.', '', b['book_name'])

        # if it's a japan mag, remove 2017年...
        if b['book_category_name'] == '雜誌-日文':
            bname = re.sub(r'^\.', '', b['book_name'])
            return re.sub(r' 20\d{2}年.*【日文版】', '【日文版】', bname)

        if b['book_category_name'] == '雜誌-報紙':
            bname = re.sub(r'^\.', '', b['book_name'])
            bname = re.sub(r'\s*20\d{6}$', '', bname)
            bname = re.sub(r'^20\d{6}', '', bname)
            bname = re.sub(r'^\d{4}', '', bname)
            bname = re.sub(r'\d{4}.*$', '', bname)
            return bname

        if b['book_category_name'].startswith('雜誌-'):
            bname = re.sub(r'^\.', '', b['book_name'])
            bname = re.sub(r'20\d{2}年.*$', '', bname)
            bname = re.sub(r'\s*第\d+期.*$', '', bname)
            return bname

        raise ValueError('Assertion: none type matched')
        # return b['book_name']

    def _get_cat(self, b):
        b.update(self.get_book_info(b))
        cat = magsname.get_mags_cat(b)
        if cat is not None:
            # print(cat)
            pid = self._mkdirp_adir(self.org_dir_ids['類別'], cat)
            self._add_parent(b, pid)
        return cat

    def org_books_in_all(self):
        books = self.list_books([self.org_dir_ids['全部']])
        print(len(books))


        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self._get_cat, books[:])

        """
        for b in books[:]:
        # for b in books:
            b.update(self.get_book_info(b))
            cat = magsname.get_mags_cat(b)
            if cat is not None:
                # print(cat)
                pid = self._mkdirp_adir(self.org_dir_ids['類別'], cat)
                self._add_parent(b, pid)
        """


    def hamiorg(self):
        # get self.org_books
        self.find_hamis_dir().mkdirp_org_dirs()

        # org '最新'
        self.org_books_in_recent()

    def standalone(self):
        # get self.org_books
        self.find_hamis_dir().mkdirp_org_dirs()

        # '全部'
        self.org_books_in_all()

    def about_quota(self):
        results = self.service.about().get(fields='kind, storageQuota').execute()
        return results.get('storageQuota')


def main():
    parser = argparse.ArgumentParser(description='hamiorg')
    parser.add_argument('-v', '--verbose', help='show more debug information', action='count')
    parser.add_argument('-V', '--version', action='version', version=VERSION, help='show version infomation')
    parser.add_argument('-s', '--standalone', action='store_true', help='run as standalone')
    args = parser.parse_args()

    if args.standalone:
        org = Hamiorg()
        org.standalone()
        return

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
