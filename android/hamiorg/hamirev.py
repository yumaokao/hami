# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import os
import json
import shutil
from os import path
from lxml import etree

EXTRACTS_PATH = "/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"

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


def main():
    books = os.listdir(EXTRACTS_PATH)
    books.sort()
    list(map(lambda b: reverse_pdf(b), books))


if __name__ == "__main__":
    main()
