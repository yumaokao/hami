package tw.ymk.apk.hamiui;

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

    @Override
    public String toString() {
        return "bookname " + book_name + ", format " + format
               + ", pubdate " + publishdate + ", category " + category;
    }
}
