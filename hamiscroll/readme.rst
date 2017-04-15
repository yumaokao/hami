HamiBook-Scroll
===============

initial
-------
* how to generate this chrome-extension
  code:: sh
  # https://www.npmjs.com/package/generator-chrome-extension
  $ mkdir hamibook-scroll && cd $_ 
  $ yo chrome-extension
  # BDD, ...

  $ gulp babel

* from a cloned repo
  code:: sh
  # git clone
  $ npm install && bower install

build
-----
* build extension
  code:: sh
  $ gulp build
  # in chrome select dist/ directory

open book with id
-----------------
* get titles for range of ids
  code:: sh
  $ sh ./query.sh 0100261000 0100261010

* open book in chrome
  code:: sh
  $ top > fancyboxOpenBook('book_id=0100261090&pkgid=PKG_10001&isTrial=0&chapter=&page=');

android
-------
* automatically reverse pdfs
  code:: sh
  $ python gits/stages/hamibook-scroll/android/rev.py

reference
---------

.. vim:fileencoding=UTF-8:ts=2:sw=2:sta:et:sts=2:ai
