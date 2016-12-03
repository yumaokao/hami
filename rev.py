#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import sys

def reverse(f):
    with open(f + '.dat', mode='rb') as inf:
        header = inf.read()
    with open(f, mode='rb') as inf:
        data = inf.read()

    with open(f + '.pdf', mode='wb') as outf:
        outf.write(header[::-1])
        outf.write(data[len(header):])
        print(header[::-1])

def main():
        with open(f + '.rev', mode='wb') as outf:
            outf.write(data[::-1])
            print(data[::-1])

def main():
    if len(sys.argv) < 2:
        print('please give me some files to reverse')
        sys.exit(0)

    list(map(lambda f: reverse(f), sys.argv[1:]))

if __name__ == "__main__":
    main()
