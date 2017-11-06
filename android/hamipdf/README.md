# hamipdf

## requires

``` sh
$ python -m venv venv
$ source venv/bin/activate
$ pip install pdfrw
```

## qpdf
``` sh
$ qpdf --qdf --object-streams=disable pdfs/input.pdf out.pdf
$ vim out.pdf
```
