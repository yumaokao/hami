# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import os
from os import path
from lxml import etree
import subprocess

EXTRACTS_PATH = "/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"
GDRV_PDF_DIR = "/publics/hamis/"
DAILY_NEWSPAPERS = ['聯合報', '聯合晚報', '中國時報精華版', '工商時報精華版', '蘋果日報appledaily', '旺報精華版', '贏家日報']


def reverse_epub(b):
    if not path.isdir(path.join(EXTRACTS_PATH, b)):
        return False
    fn_mime = path.join(EXTRACTS_PATH, b, 'mimetype')
    dn_oebps = path.join(EXTRACTS_PATH, b, 'OEBPS')
    fn_opf = path.join(EXTRACTS_PATH, b, 'OEBPS', 'package.opf')
    if not path.isfile(fn_mime) or not path.isdir(dn_oebps) or not path.isfile(fn_opf):
        return False
    dats = os.listdir(dn_oebps)
    dats = filter(lambda d: os.path.splitext(d)[-1] == '.dat', dats)
    # print(list(dats))
    for dat in dats:
        fn_orig = os.path.splitext(dat)[0]
        fn_dat = os.path.splitext(dat)[-1]
        print(fn_orig)
    print('epub {}'.format(b))


def get_meta_title(fn_xml):
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


def reverse_pdf(b):
    if not path.isdir(path.join(EXTRACTS_PATH, b)):
        return False
    fn_pdf = path.join(EXTRACTS_PATH, b, b + '.pdf')
    fn_dat = path.join(EXTRACTS_PATH, b, b + '.pdf.dat')
    fn_xml = path.join(EXTRACTS_PATH, b, 'meta.xml')
    if not path.isfile(fn_pdf) or not path.isfile(fn_dat) or not path.isfile(fn_xml):
        return False

    print('looking {}: '.format(b), end='')
    # get title
    title = get_meta_title(fn_xml)
    fn_title = path.join(EXTRACTS_PATH, b, '{}-{}.pdf'.format(title, b))

    # check already
    if path.isfile(fn_title):
        print('Already reversed')
        return True

    # reverse pdf
    with open(fn_dat, mode='rb') as inf:
        header = inf.read()
    with open(fn_pdf, mode='rb') as inf:
        data = inf.read()

    # write pdf
    with open(fn_title, mode='wb') as outf:
        outf.write(header[::-1])
        outf.write(data[len(header):])

    print('{}-{}.pdf\n'.format(title, b))
    return True


def push_pdf(b, hamis):
    if not path.isdir(path.join(EXTRACTS_PATH, b)):
        return False
    fn_xml = path.join(EXTRACTS_PATH, b, 'meta.xml')
    if not path.isfile(fn_xml):
        return False

    # get title
    title = get_meta_title(fn_xml)
    fn_title = path.join(EXTRACTS_PATH, b, '{}-{}.pdf'.format(title, b))

    print('pushing {}-{}.pdf: '.format(title, b))

    if not path.isfile(fn_title):
        return False

    if len(list(filter(lambda n: n in title, DAILY_NEWSPAPERS))) > 0:
        # push to newspaper directory
        if len(list(filter(lambda d: b in d, hamis['daily']))) > 0:
            print('Already pushed')
        else:
            subprocess.check_call(['gdrv', 'push', fn_title, '{}{}/'.format(GDRV_PDF_DIR, '報紙')])
    else:
        # push to hami directory
        if len(list(filter(lambda d: b in d, hamis['hami']))) > 0:
            print('Already pushed')
        else:
            subprocess.check_call(['gdrv', 'push', fn_title, GDRV_PDF_DIR])


def get_gdrv_hami_list(path):
    hamis = {}

    books = subprocess.check_output(['gdrv', 'list', path])
    hamis['hami'] = [b.decode('utf-8') for b in books.splitlines()]
    news = subprocess.check_output(['gdrv', 'list', '{}{}/'.format(path, '報紙')])
    hamis['daily'] = [n.decode('utf-8') for n in news.splitlines()]

    return hamis


def main():
    books = os.listdir(EXTRACTS_PATH)
    list(map(lambda b: reverse_pdf(b), books))
    hamis = get_gdrv_hami_list(GDRV_PDF_DIR)
    list(map(lambda b: push_pdf(b, hamis), books))
    # list(map(lambda b: reverse_epub(b), books))


if __name__ == "__main__":
    main()
