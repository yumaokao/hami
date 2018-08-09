# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import csv
import json
import shutil
import warnings
from os import path
from lxml import etree
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

EXTRACTS_PATH = "/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"
HAMIUI_PATH = "/storage/emulated/0/Android/data/tw.ymk.apk.hamiui/files"


class HamiRevOrg:
    def __init__(self):
        self.bookdirs = os.listdir(EXTRACTS_PATH)
        self.bookdirs.sort()
        self.revbooks = []

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
        dirname = os.path.dirname(os.path.realpath(__file__))
        settingsfn = os.path.join(dirname, 'settings.yaml')
        clicfgfn = os.path.join(dirname, 'client_secrets.json')
        gauth = GoogleAuth(settings_file=settingsfn)
        gauth.LoadClientConfigFile(client_config_file=clicfgfn)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            gauth.CommandLineAuth()
        self.drive = GoogleDrive(gauth)
        return self

    def find_hamis_dir(self):
        hamisdirs = self.drive.ListFile(
            {'q': "mimeType='application/vnd.google-apps.folder' and name='hamis'"}
        ).GetList()
        if len(hamisdirs) != 1:
            raise ValueError('there are more than one hami dirs')
        self.hamis = hamisdirs[0]
        return self


def main():
    hamirevorg = HamiRevOrg()
    hamirevorg.auth().find_hamis_dir()
    # hamirevorg.reverse().get_downloaded_csv()


if __name__ == "__main__":
    main()
