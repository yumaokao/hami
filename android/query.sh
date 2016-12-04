for I in $(seq $1 $2);
do
I=$(printf '%010d' $I)
echo -n "$I ";
curl -H 'Accept:*/*' -H 'Accept-Encoding:gzip, deflate, sdch' \
    -H 'Accept-Language:zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4' \
    -H 'Connection:keep-alive' \
    -H 'Host:bookstore.emome.net' \
    -H 'If-Modified-Since:Fri, 02 Dec 2016 16:22:34 GMT' \
    -H 'User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36' \
    "http://bookstore.emome.net/reader/viewer?type=own&book_id=$I&pkgid=PKG_10001&isTrial=0&chapter=&page=" 2>&1 | grep '<title>';
done
