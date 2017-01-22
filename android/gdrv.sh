LOCAL_PDF_DIR="/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"
GDRV_PDF_DIR="/publics/hamis/"

GDRV_PDF_FILES=$(gdrv list "$GDRV_PDF_DIR")
[ -z "$GDRV_PDF_FILES" ] && exit 1

cd $LOCAL_PDF_DIR && ls */*-*.pdf | while read B
do
    BID=${B##*-}
    BID=${BID%%.pdf}
    # echo "$BID"

    echo -n "$B... "
    echo $GDRV_PDF_FILES | grep -q "$BID" && echo "Already" || gdrv push "$B" $GDRV_PDF_DIR
    # gdrv list $GDRV_PDF_DIR | grep "$B" > /dev/null && echo "Already" || gdrv push $GDRV_PDF_DIR "$B"
done
