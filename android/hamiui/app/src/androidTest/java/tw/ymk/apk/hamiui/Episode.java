package tw.ymk.apk.hamiui;

import android.icu.text.SimpleDateFormat;

import java.util.Date;

/**
 * Created by yumaokao on 2017/3/23.
 */

public class Episode {
    private String book_name;
    private String author;
    private String publisher;
    private String format;
    private String publishdate;
    private String category;

    public Episode(String n, String a, String p, String f, String d, String c) {
        book_name = n;
        author = a;
        publisher = p;
        format = f;
        publishdate = d;
        category = c;
    }

    public Episode(String csv) {
        String[] attrs = csv.split(",");
        // this(attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5]);
        book_name = attrs[0];
        author = attrs[1];
        publisher = attrs[2];
        format = attrs[3];
        publishdate = attrs[4];
        category = attrs[5];
    }

    public String getBookName() {
        return book_name;
    }

    public String getFormat() {
        return format;
    }

    public Date getPublishDate() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        Date date = null;
        try {
            date = sdf.parse(publishdate);
        } catch (Exception e) {
        }
        return date;
    }

    public String getCategory() {
        return category;
    }

    public String toCsvString() {
        return book_name + "," + author + "," + publisher + ","
               + format + "," + publishdate + "," + category;
    }

    @Override
    public String toString() {
        return "bookname " + book_name + ", format " + format
               + ", pubdate " + publishdate + ", category " + category;
    }

    @Override
    public boolean equals(Object that) {
        if (!(that instanceof Episode))
            return false;
        Episode epi = (Episode) that;
        if (!(this.book_name.equals(epi.book_name)))
            return false;
        // TODO: equals more ?
        return true;
    }
}
