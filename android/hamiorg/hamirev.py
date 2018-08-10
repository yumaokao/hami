# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import csv
import json
import shutil
import argparse
import warnings
from os import path
from lxml import etree
from apiclient.discovery import build
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow

VERSION = '0.2.0'
EXTRACTS_PATH = "/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"
HAMIUI_PATH = "/storage/emulated/0/Android/data/tw.ymk.apk.hamiui/files"


class HamiRevOrg:
    def __init__(self, args):
        self.args = args
        self.bookdirs = os.listdir(EXTRACTS_PATH)
        self.bookdirs.sort()
        self.revbooks = []
        self.hami_dirs = {
            '全部': None, '最新': None, '最新/雜誌': None, '最新/報紙': None,
            '最新/書籍': None, '類別': None, '日期': None}

    def get_downloaded_csv(self):
        fn_csv = path.join(HAMIUI_PATH, 'downloaded-episodes.csv')
        if not path.isfile(fn_csv):
            raise FileNotFoundError('{} is not a file.'.format(fn_csv))
        with open(fn_csv, newline='') as f_csv:
            epireader = csv.reader(f_csv, delimiter=',')
            for epi in epireader:
                print(epi)
        return self

    def reverse(self):
        def _get_meta_title(fn_xml):
            title = ''
            with open(fn_xml) as inf:
                root = etree.parse(inf).getroot()
                titles = list(filter(lambda c: c.tag == 'bookname', root))
                if len(titles) != 1:
                    return False
                title = titles[0].text.replace('/', '.')
                title = title[1:] if title[0] == '.' else title
                # print(title)
            return title

        def _reverse_pdf(b):
            if not path.isdir(path.join(EXTRACTS_PATH, b)):
                raise NotADirectoryError('{} is not a dir.'.format(b))
            fn_pdf = path.join(EXTRACTS_PATH, b, b + '.pdf')
            fn_dat = path.join(EXTRACTS_PATH, b, b + '.pdf.dat')
            fn_xml = path.join(EXTRACTS_PATH, b, 'meta.xml')
            if not path.isfile(fn_pdf):
                raise FileNotFoundError('{} is not a file.'.format(fn_pdf))
            if  not path.isfile(fn_dat):
                raise FileNotFoundError('{} is not a file.'.format(fn_dat))
            if  not path.isfile(fn_xml):
                raise FileNotFoundError('{} is not a file.'.format(fn_xml))

            print('looking {}: '.format(b), end='')
            # get title
            title = _get_meta_title(fn_xml)
            fn_title = path.join(EXTRACTS_PATH, b, '{}-{}.pdf'.format(title, b))

            # check already
            if path.isfile(fn_title):
                print('[{}] Already reversed'.format(title))
                return fn_title

            # reverse pdf
            with open(fn_dat, mode='rb') as inf:
                header = inf.read()
            with open(fn_pdf, mode='rb') as inf:
                data = inf.read()

            # write pdf
            with open(fn_title, mode='wb') as outf:
                outf.write(header[::-1])
                outf.write(data[len(header):])

            print('{}-{}.pdf'.format(title, b))
            return fn_title
        self.revbooks = list(map(lambda b: _reverse_pdf(b), self.bookdirs))
        return self

    def auth(self):
        # auth for drive
        client_secrects_file = os.path.join('hami', 'client_secrets.json')
        scopes = ['https://www.googleapis.com/auth/drive']
        credsfn = os.path.join('hami', 'credentials.json')
        if os.path.isfile(credsfn):
            creds = credentials.Credentials.from_authorized_user_file(
                credsfn, scopes=scopes)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrects_file, scopes = scopes)
            creds = flow.run_console()
            if creds and creds.valid:
                with open(credsfn, 'w') as f:
                    json.dump({'refresh_token': creds.refresh_token,
                               'client_id': creds.client_id,
                               'client_secret': creds.client_secret}, f)
        self.drive = build('drive', 'v3', credentials=creds)
        return self

    def mkdirp(self, prefix, adir):
        dbnames = os.path.split(adir)
        if not dbnames[0] == '':
            prefix = self.mkdirp(prefix, dbnames[0])
        qbase = "mimeType='application/vnd.google-apps.folder' and '{}' in parents and name='{}'"
        fields = 'nextPageToken, files(id, name)'
        q = qbase.format(prefix, dbnames[1])
        alldirs = self.drive.files().list(q=q, spaces='drive', fields=fields).execute().get('files', [])
        if len(alldirs) > 1:
            raise ValueError('there are more than one hami dirs')
        if len(alldirs) == 0:
            ndir = {'mimeType': 'application/vnd.google-apps.folder',
                    'name': dbnames[1], 'parents': [prefix]}
            cdir = self.drive.files().create(body=ndir, fields='id').execute()
            return cdir['id']
        else:
            return alldirs[0]['id']

    def find_hamis_dir(self):
        hamisfinder = self.drive.files().list(
            q="mimeType='application/vnd.google-apps.folder' and name='hamis'",
            spaces='drive',
            fields='nextPageToken, files(id, name)')
        hamisdirs = hamisfinder.execute().get('files', [])
        if len(hamisdirs) == 0:
            self.mkdirp('root', 'hamis')
            hamisdirs = hamisfinder.execute().get('files', [])
        if len(hamisdirs) != 1:
            raise ValueError('there are more than one hami dirs or no hami')
        self.hami_root= hamisdirs[0]
        # hami_dirs
        prefix = self.hami_root['id']
        self.hami_dirs = {k: self.mkdirp(prefix, k) for k in self.hami_dirs.keys()}
        if (self.args.verbose > 0):
            print(self.hami_dirs)
        return self


def main():
    parser = argparse.ArgumentParser(description='hamirevorg')
    parser.add_argument('-v', '--verbose', help='show more debug information', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=VERSION, help='show version infomation')
    args = parser.parse_args()

    hamirevorg = HamiRevOrg(args)
    hamirevorg.auth().find_hamis_dir()
    # hamirevorg.reverse().get_downloaded_csv()


if __name__ == "__main__":
    main()
