#!/usr/bin/env python3
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import os
import argparse
import zlib
from pdfrw import PdfReader
from pdfrw.findobjs import find_objects

VERSION = '0.2.0'


def main():
    parser = argparse.ArgumentParser(description='hamipdf')
    parser.add_argument('-v', '--verbose', help='show more debug information', action='count', default=0)
    parser.add_argument('-V', '--version', action='version', version=VERSION, help='show version infomation')
    parser.add_argument('pdfs', nargs='+', metavar='PDF', help='pdf files')
    args = parser.parse_args()

    # print(args.pdfs)
    pdf = PdfReader(args.pdfs[0])
    # for obj in find_objects(pdf.pages):
    #     print(obj)

    print(zlib.decompress(bytes(pdf.pages[0].Contents[0].stream, encoding='latin-1')))
    import ipdb
    ipdb.set_trace()
    for obj in find_objects(pdf.pages[1]):
        print(obj)


if __name__ == "__main__":
    main()
