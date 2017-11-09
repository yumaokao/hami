#!/usr/bin/env python3
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import os
import argparse
import zlib
import pdfrw
from pdfrw import PdfReader
from pdfrw.findobjs import find_objects

VERSION = '0.2.0'


def extract(p):
    def _extract(c):
        if not isinstance(c, pdfrw.objects.pdfdict.PdfDict):
            return
        # print('  {}'.format(c))
        if c.Filter == '/FlateDecode':
            s = zlib.decompress(bytes(c.stream, encoding='latin-1'))
            s = str(s, encoding='latin-1')
        else:
            s = c.stream

        s = s.split()
        ts = []
        # only 'BT', 'TF', 'TJ', 'Tj', 'ET', ', "
        for i, t in enumerate(s):
            if t == 'BT' or t == 'ET'or t.endswith('Tj') or t.endswith('TJ'):
                ts.append(t)
                continue
            if t.endswith('"') or t.endswith("'"):
                print(t)
            if t == 'Tf':
                ts.append(' '.join(s[i-2:i+1]))
        return ts

    def _font(f):
        if f.ToUnicode is None:
            return []
        u = f.ToUnicode
        if u.Filter == '/FlateDecode':
            s = zlib.decompress(bytes(u.stream, encoding='latin-1'))
            s = str(s, encoding='latin-1')
        else:
            s = u.stream

        # beginbfchar
        beginchar = False
        charmaps = {}
        for l in s.splitlines():
            if not beginchar:
                if l.endswith('beginbfchar'):
                    beginchar = True
                continue
            else:
                if l.endswith('endbfchar'):
                    beginchar = False
                    continue
                k = l.split()[0].strip('><')
                r = l.split()[1].strip('><')
                v = ''
                for i in range(len(r) // 4):
                    v += chr(int(r[i * 4 : i * 4 + 4], 16))
                charmaps[k] = v
        return charmaps


    # fonts
    if p.Resources.Font is None:
        return []
    fonts = {}
    for fn in p.Resources.Font.keys():
        f = p.Resources.Font[fn]
        fonts[fn] = _font(f)
        print('  Font {}'.format(fn))
        # print(fonts[fn])
        # break

    # texts
    texts = []
    if isinstance(p.Contents, pdfrw.objects.pdfarray.PdfArray):
        for c in p.Contents:
            texts.extend(_extract(c))
    else:
        texts.extend(_extract(p.Contents))

    # decode
    rstrs = ''
    f = None
    for t in texts:
        # print(t)
        if t.endswith('Tf'):
            f = fonts[t.split()[0]]
            continue
        if t.endswith('Tj'):
            cs = t[:-2].strip('><')
            for i in range(len(cs) // 4):
                k = cs[i * 4 : i * 4 + 4]
                rstrs += (f[k])
            continue
        if t.endswith('TJ'):
            ts = t[:-2].strip('][')
            for cs in ts.split('<'):
                cs = cs.split('>')[0]
                for i in range(len(cs) // 4):
                    k = cs[i * 4 : i * 4 + 4]
                    rstrs += (f[k])
    print(rstrs)


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

    for i, p in enumerate(pdf.pages):
        print('Page {}'.format(i))
        extract(p)
        break

    # import ipdb
    # ipdb.set_trace()


if __name__ == "__main__":
    main()
