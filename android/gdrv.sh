
LOCAL_PDF_DIR="/storage/sdcard0/Download/hamis/"
GDRV_PDF_DIR="/publics/hamis/"

GDRV_PDF_FILES=$(gdrv list "$GDRV_PDF_DIR")

cd $LOCAL_PDF_DIR && ls | while read B
do
    BID=${B##*-}
    BID=${BID%%.pdf}
    # echo "$BID"

    echo -n "$B... "
    echo $GDRV_PDF_FILES | grep -q "$BID" && echo "Already" || gdrv push "$B" $GDRV_PDF_DIR
    # gdrv list $GDRV_PDF_DIR | grep "$B" > /dev/null && echo "Already" || gdrv push $GDRV_PDF_DIR "$B"
done
