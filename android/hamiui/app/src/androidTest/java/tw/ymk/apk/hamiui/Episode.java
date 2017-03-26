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

    @Override
    public String toString() {
        return "bookname " + book_name + ", format " + format
               + ", pubdate " + publishdate + ", category " + category;
    }
}
