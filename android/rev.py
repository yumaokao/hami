# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import os
import json
import shutil
import subprocess
from os import path
from lxml import etree

EXTRACTS_PATH = "/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"
GDRV_PDF_DIR = "/publics/hamis/最新/"
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
        # print(fn_orig)
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
        return (False, None)
    fn_xml = path.join(EXTRACTS_PATH, b, 'meta.xml')
    if not path.isfile(fn_xml):
        return (False, None)

    # get title
    title = get_meta_title(fn_xml)
    booknameid = '{}-{}.pdf'.format(title, b)
    fn_title = path.join(EXTRACTS_PATH, b, booknameid)

    print('pushing {}: '.format(booknameid), end='')

    if not path.isfile(fn_title):
        return (False, None)

    # check already in json
    if len(list(filter(lambda d: b in d['name'], hamis['json']))) > 0:
        print('Already pushed (json)')
        return (True, booknameid)

    # check already in recent
    if len(list(filter(lambda d: b in d, hamis['hami']))) > 0:
        print('Already pushed (recent)')
        return (True, booknameid)

    # push to hami recent directory
    print()
    subprocess.check_call(['gdrv', 'push', fn_title, GDRV_PDF_DIR])
    return (True, booknameid)


def save_hami_json(hamis, pushs):
    books = hamis['json']
    print('讀取全部: {}'.format(len(books)))
    pushs = list(filter(lambda p: p[0], pushs))
    pushs = list(filter(lambda p: len(list(filter(lambda d: p[1] in d['name'], books))) == 0, pushs))
    pushs = list(map(lambda p: {'name': p[1]}, pushs))
    books = pushs + books
    print('寫入全部: {}'.format(len(books)))
    with open('/data/local/tmp/hami.json', 'w') as f:
        json.dump(books, f)


def get_gdrv_hami_list(path):
    hamis = {}

    books = subprocess.check_output(['gdrv', 'list', path])
    hamis['hami'] = [b.decode('utf-8') for b in books.splitlines()]

    # local database
    with open('/data/local/tmp/hami.json', 'r') as f:
        books = json.load(f)
    hamis['json'] = books
    # print(json.dumps(books, indent=2))
    return hamis


def remove_old_books(books):
    print('Total books: {}'.format(len(books)))
    over = len(books) - 80
    books = list(map(lambda b: (b, os.stat(path.join(EXTRACTS_PATH, b)).st_mtime), books))
    books = sorted(books, key=lambda b: b[1])
    for b in books[0:over]:
        print('remove {}'.format(b[0]))
        shutil.rmtree(path.join(EXTRACTS_PATH, b[0]))


def main():
    books = os.listdir(EXTRACTS_PATH)
    books.sort()
    list(map(lambda b: reverse_pdf(b), books))
    hamis = get_gdrv_hami_list(GDRV_PDF_DIR)
    pushs = list(map(lambda b: push_pdf(b, hamis), books))
    save_hami_json(hamis, pushs)
    list(map(lambda b: reverse_epub(b), books))
    if len(books) > 80:
        remove_old_books(books)


if __name__ == "__main__":
    main()
