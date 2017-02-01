# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import os
from os import path
import sys
from lxml import etree

EXTRACTS_PATH="/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"
# REVERSED_PATH="/sdcard/Download/hamis/"


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


def reverse_pdf(b):
    if not path.isdir(path.join(EXTRACTS_PATH, b)):
        return False
    fn_pdf = path.join(EXTRACTS_PATH, b, b + '.pdf')
    fn_dat = path.join(EXTRACTS_PATH, b, b + '.pdf.dat')
    fn_xml = path.join(EXTRACTS_PATH, b, 'meta.xml')
    if not path.isfile(fn_pdf) or not path.isfile(fn_dat) or not path.isfile(fn_xml):
        return False

    print('looking {}'.format(b))
    # get title
    with open(fn_xml) as inf:
        root = etree.parse(inf).getroot()
        titles = list(filter(lambda c: c.tag == 'bookname', root))
        if len(titles) != 1:
            return False
        title = titles[0].text.replace('/', '.')
        title = title[1:] if title[0] == '.' else title
        fn_title = path.join(EXTRACTS_PATH, b, '{}-{}.pdf'.format(title, b))
        # print(title)

    #check already
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


def main():
    books = os.listdir(EXTRACTS_PATH)
    list(map(lambda b: reverse_pdf(b), books))
    # list(map(lambda b: reverse_epub(b), books))


if __name__ == "__main__":
    main()
