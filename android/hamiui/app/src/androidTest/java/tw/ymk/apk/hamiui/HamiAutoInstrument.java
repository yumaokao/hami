package tw.ymk.apk.hamiui;

import android.os.Environment;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;
import android.support.test.uiautomator.By;
import android.support.test.uiautomator.BySelector;
import android.support.test.uiautomator.Direction;
import android.support.test.uiautomator.UiDevice;
import android.support.test.filters.SdkSuppress;
import android.support.test.uiautomator.UiObject2;
import android.support.test.uiautomator.Until;
import android.util.Log;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.lang.Float;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.io.File;
import java.io.FileWriter;
import java.io.FileInputStream;

import org.json.JSONObject;
import org.json.JSONArray;

import com.android.volley.RequestQueue;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.Volley;
import com.android.volley.toolbox.StringRequest;

import static org.hamcrest.core.IsNull.notNullValue;
import static org.junit.Assert.*;

/**
 * Instrumentation test, which will execute on an Android device.
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
@RunWith(AndroidJUnit4.class)
@SdkSuppress(minSdkVersion = 18)
public class HamiAutoInstrument {
    private static final String TAG = "HAMIUI";
    private static final String BASIC_SAMPLE_PACKAGE = "com.she.eReader";
    private static final int SCROLL_TIMEOUT = 1000;
    private static final int LAUNCH_TIMEOUT = 10000;
    private static final int WAIT_UI_TIMEOUT = 10000;
    private static final int EPISODE_BREAK_TIMES = 3;
    private static final int NEWLY_BREAK_TIMES = 7;
    private static final int WAIT_TIMEOUT = 30000;
    private static final int WAIT_1MIN_TIMEOUT = 60000;
    private static final int DOWNLOAD_TIMEOUT = 300000;
    private static final float CLEAR_THRESHOLD= 1.0f;

    private UiDevice mDevice;
    private static ArrayList<String> mJsonBooks = new ArrayList<String>();

    @Before
    public void startHamiActivityFromHomeScreen() {
        // Initialize UiDevice instance
        mDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
        // Start from the home screen
        mDevice.pressHome();
        // Wait for launcher
        final String launcherPackage = getLauncherPackageName();
        assertThat(launcherPackage, notNullValue());
        mDevice.wait(Until.hasObject(By.pkg(launcherPackage).depth(0)), LAUNCH_TIMEOUT);

        // Launch the app
        Context context = InstrumentationRegistry.getContext();
        final Intent intent = context.getPackageManager()
                .getLaunchIntentForPackage(BASIC_SAMPLE_PACKAGE);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);    // Clear out any previous instances
        context.startActivity(intent);

        // Wait for the app to appear
        mDevice.wait(Until.hasObject(By.pkg(BASIC_SAMPLE_PACKAGE).depth(0)), LAUNCH_TIMEOUT);
    }

    @Test
    public void useAppContext() throws Exception {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();
        Log.d(TAG, "package name " + appContext.getPackageName());
        assertEquals("tw.ymk.apk.hamiui", appContext.getPackageName());
    }

    @Test
    public void useVolleyRequest() throws Exception {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();
        assertEquals("tw.ymk.apk.hamiui", appContext.getPackageName());

        RequestQueue queue = Volley.newRequestQueue(appContext);
        String url = "http://www.google.com";
        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
            new Response.Listener<String>() {
                @Override
                public void onResponse(String response) {
                    // Display the first 500 characters of the response string.
                    Log.d(TAG, "Volley Request: Response is: "+ response.substring(0,500));
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    Log.d(TAG, "Volley Request: That didn't work!");
                }
            });
        // Add the request to the RequestQueue.
        queue.add(stringRequest);

        try {
            Thread.sleep(WAIT_UI_TIMEOUT);
        } catch (Exception e) {
        }
    }

    @Test
    public void autoHamiDownload() throws Exception {
        checkAds();
        // writeJsonFile();
        readHamiJsonBooks();
        updateBooks();
        clearBooks();
        iterateBooks();
    }

    private boolean writeJsonFile() {
        try {
            JSONObject obj = new JSONObject();
            obj.put("Name", "YMK");
            Log.d(TAG, "writeJsonFile: json " + obj.toString());

            Context appContext = InstrumentationRegistry.getTargetContext();
            File path = appContext.getExternalFilesDir(null);
            Log.d(TAG, "writeJsonFile: private dir " + path);
            if (!path.isDirectory()) {
                if (!path.mkdirs()) {
                    Log.d(TAG, "writeJsonFile: private dir " + path + " not created");
                    return false;
                }
            }
            FileWriter filew = new FileWriter(path + "/test.json");
            filew.write(obj.toString());
            filew.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return true;
    }

    private boolean readHamiJsonBooks() {
        String hamijsonfn = "/data/local/tmp/hami.json";
        String jsonstr = "";
        try {
            File file = new File(hamijsonfn);
            FileInputStream fin = new FileInputStream(file);
            int length = fin.available();
            byte[] buffer = new byte[length];
            fin.read(buffer);
            fin.close();
            jsonstr = new String(buffer, "UTF-8");
            // Log.d(TAG, "hamijson length " + length);
            // Log.d(TAG, "hamijson: [" + jsonstr + "]");
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            JSONArray books = new JSONArray(jsonstr);
            for (int i = 0; i < books.length(); i++) {
                JSONObject book = books.getJSONObject(i);
                String bname = book.getString("name");
                // TITLE...-0100261388.pdf
                // Log.d(TAG, "book[" + i + "]: " + bname.substring(0, bname.length() - 15));
                mJsonBooks.add(bname.substring(0, bname.length() - 15));
            }
            Log.d(TAG, "mJsonBooks length " + mJsonBooks.size());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return true;
    }

    private boolean checkAds() {
        UiObject2 object = null;
        object = mDevice.wait(Until.findObject(By.textContains("下次再評")), WAIT_UI_TIMEOUT);
        if (object != null)
            object.click();

        return true;
    }

    private String updateBooks() {
        UiObject2 object = null;

        // 設定
        object = waitObject2(By.res("com.she.eReader:id/main_footer_tab4_txtV"));
        object.click();

        // 上次更新時間：2017-03-22 上午 11:10 成功
        object = waitObject2(By.textStartsWith("上次更新時間"), DOWNLOAD_TIMEOUT);
        Log.d(TAG, "last updated: " + object.getText());
        String last_updated = object.getText();

        // 立即更新書單
        object = waitObject2(By.res("com.she.eReader:id/rl_update_booklist"));
        object.click();

        // 上次更新時間：2017-03-22 上午 11:10 成功
        mDevice.wait(Until.gone(By.res("com.she.eReader:id/iv_update_booklist")), WAIT_1MIN_TIMEOUT);
        object = waitObject2(By.textStartsWith("上次更新時間"), DOWNLOAD_TIMEOUT);
        Log.d(TAG, "updated: " + object.getText());

        return object.getText();
    }

    private boolean clearBooks() {
        UiObject2 object = null;
        // 設定
        object = waitObject2(By.res("com.she.eReader:id/main_footer_tab4_txtV"));
        object.click();
        // 空間管理
        object = waitObject2(By.textStartsWith("剩餘"), WAIT_UI_TIMEOUT);
        Log.d(TAG, "空間管理: [" + object.getText() + "]");
        String lasts[] = object.getText().split(" ");
        if (lasts.length == 2) {
            if (lasts[1].equals("GB")) {
                try {
                    float gb = Float.parseFloat(lasts[0].substring(4));
                    if (gb > CLEAR_THRESHOLD) {
                        Log.d(TAG, "Not clear: " + gb + " GB > " + CLEAR_THRESHOLD + " GB.");
                        return false;
                    }
                } catch (Exception e) {
                }
            }
        }
        object.click();
        // 全部書籍
        object = waitObject2(By.res("com.she.eReader:id/tv_all_size"));
        Log.d(TAG, "全部書籍: " + object.getText());
        if (object.getText().contains("約0MB")) {
            Log.d(TAG, "Not clear: 全部書籍 is alreay 約0MB");
        } else {
            object = waitObject2(By.res("com.she.eReader:id/delete_all"));
            object.click();
            // 是
            object = waitObject2(By.res("com.she.eReader:id/custom_button_finish"));
            object.click();
        }
        // <
        object = waitObject2(By.res("com.she.eReader:id/btGoBack"));
        object.click();
        return true;
    }

    private int iterateBooks() {
        UiObject2 object = null;
        List<UiObject2> books = new ArrayList<UiObject2>();
        boolean scroll = true;
        int downloads = 0;

        // 書單
        object = waitObject2(By.res("com.she.eReader:id/main_footer_tab2_txtV"));
        object.click();

        // 新上架書籍
        object = waitObject2(By.textContains("新上架書籍"));
        object.click();

        int already = 0;
        List<String> readbooknames = new ArrayList<String>();
        while (scroll) {
            books = mDevice.wait(Until.findObjects(By.res("com.she.eReader:id/tv_booklist_item_book_name")), WAIT_TIMEOUT);
            List<UiObject2> newbooks = new ArrayList<UiObject2>(books);
            List<String> booknames = new ArrayList<String>();

            // List<String> booknames = newbooks.stream().map(b -> b.getText()).collect(Collectors.toList());
            for (UiObject2 obj : newbooks) {
                booknames.add(obj.getText());
            }

            for (String bookname : booknames) {
                if (readbooknames.contains(bookname)) {
                    Log.d(TAG, "scroll book: " + bookname + " just read before");
                    continue;
                }
                UiObject2 obj = waitObject2(By.textContains(bookname));
                obj.click();
                if (downloadEpisodes() > 0) {
                    // YMK DEBUG
                    // already = 0;
                    already++;
                } else {
                    already++;
                }
                readbooknames.add(bookname);
                UiObject2 back = waitObject2(By.res("com.she.eReader:id/rl_toolbar_back"));
                back.click();
            }

            if (already > NEWLY_BREAK_TIMES)
                break;
            // scoll down
            object = waitObject2(By.res("com.she.eReader:id/book_listV"));
            scroll = object.scroll(Direction.DOWN, 0.5F);
        }

        return downloads;

    }

    private Episode getEpisodeInfo() {
        UiObject2 object = null;
        UiObject2 info = null;
        String book_name;
        String author;
        String publisher;
        String format;
        String publishdate;
        String category;
        Episode epi;

        // wait to load book info
        object = waitObject2(By.res("com.she.eReader:id/chapter_info_container"));
        info = waitObject2(By.res("com.she.eReader:id/rl_description"));
        info.click();

        // It's weird that object could not be obtained from object/device other than it's parent
        // Check with following
        /* object = waitObject2(By.res("com.she.eReader:id/main_layout"));
        Log.d(TAG, "main_layout: getChildCount() " + object.getChildCount());
        object = object.getChildren().get(0);
        Log.d(TAG, "main_layout: child[0].getChildCount() " + object.getChildCount());
        object = object.getChildren().get(0);
        Log.d(TAG, "main_layout: child[0][0].getChildCount() " + object.getChildCount());
        UiObject2 child0 = object.getChildren().get(0);
        Log.d(TAG, "description_out_container ?:  " + child0.getResourceName());
        UiObject2 child0id = object.findObject(By.res("com.she.eReader:id/description_out_container"));
        Log.d(TAG, "child0id ?:  " + child0id);
        UiObject2 devchild0id = mDevice.findObject(By.res("com.she.eReader:id/description_out_container"));
        Log.d(TAG, "devchild0id ?:  " + devchild0id); */

        /* try {
            Thread.sleep(1000);
        } catch (Exception e) {
        } */
        // So needed to get upper object to parse EpisodeInfo
        UiObject2 rootobj = waitObject2(By.res("com.she.eReader:id/main_layout"));
        assertThat(rootobj, notNullValue());
        rootobj = rootobj.getChildren().get(0).getChildren().get(0);
        assertThat(rootobj, notNullValue());
        object = rootobj.findObject(By.res("com.she.eReader:id/book_name"));
        assertThat(object, notNullValue());
        book_name = object.getText();
        object = rootobj.findObject(By.res("com.she.eReader:id/author"));
        assertThat(object, notNullValue());
        author = object.getText();
        object = rootobj.findObject(By.res("com.she.eReader:id/publisher"));
        assertThat(object, notNullValue());
        publisher = object.getText();
        object = rootobj.findObject(By.res("com.she.eReader:id/format"));
        assertThat(object, notNullValue());
        format = object.getText();
        object = rootobj.findObject(By.res("com.she.eReader:id/publishdate"));
        assertThat(object, notNullValue());
        publishdate = object.getText();
        object = rootobj.findObject(By.res("com.she.eReader:id/category"));
        assertThat(object, notNullValue());
        category = object.getText();

        // Dump dumpWindowHierarchy
        /* try {
            String hamidumpfn = "hamidump.txt";
            File path = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            path.mkdirs();
            Log.d(TAG, "dumpWindowHierarchy: public dir " + path);
            File file = new File(path, hamidumpfn);
            Log.d(TAG, "dumpWindowHierarchy: B " + path + "/" + hamidumpfn);
            mDevice.dumpWindowHierarchy(file);
            Log.d(TAG, "dumpWindowHierarchy: A " + path + "/" + hamidumpfn);
        } catch (Exception e) {
            e.printStackTrace();
        } */

        /* object = waitObject2(By.res("com.she.eReader:id/book_name"));
        book_name = object.getText();
        Log.d(TAG, "book_name: " + object.getText());
        object = waitObject2(By.res("com.she.eReader:id/author"));
        author = object.getText();
        Log.d(TAG, "author: " + object.getText());
        object = waitObject2(By.res("com.she.eReader:id/publisher"));
        publisher = object.getText();
        Log.d(TAG, "publisher: " + object.getText());
        object = waitObject2(By.res("com.she.eReader:id/format"));
        format = object.getText();
        Log.d(TAG, "format: " + object.getText());
        object = waitObject2(By.res("com.she.eReader:id/publishdate"));
        publishdate = object.getText();
        Log.d(TAG, "publishdate: " + object.getText());
        object = waitObject2(By.res("com.she.eReader:id/category"));
        category = object.getText();
        Log.d(TAG, "category: " + object.getText()); */

        info.click();

        epi = new Episode(book_name, author, publisher, format, publishdate, category);
        return epi;
    }

    private int downloadEpisodes() {
        List<UiObject2> covers = new ArrayList<UiObject2>();
        UiObject2 current = null;
        UiObject2 last = null;
        Episode episode = null;
        int already = 0;
        int downloaded = 0;

        covers = mDevice.wait(Until.findObjects(By.res("com.she.eReader:id/bookcover_container")), WAIT_UI_TIMEOUT);
        if (covers.size() < 1)
            return -1;
        current = covers.get(0);
        episode = getEpisodeInfo();
        if (downloadEpisode(episode, covers.size()))
            downloaded++;
        else
            already++;
        while (!current.equals(last)) {
            last = current;
            covers = mDevice.wait(Until.findObjects(By.res("com.she.eReader:id/bookcover_container")), WAIT_UI_TIMEOUT);
            if (covers.size() == 1)
                break;
            current = covers.get(covers.size() -1);
            current.click();
            episode = getEpisodeInfo();
            if (downloadEpisode(episode, covers.size()))
                downloaded++;
            else
                already++;
            // downloaded > EPISODE_BREAK_TIMES for bname not matched in mJsonBooks
            if (already > EPISODE_BREAK_TIMES || downloaded > EPISODE_BREAK_TIMES)
                break;
            covers = mDevice.wait(Until.findObjects(By.res("com.she.eReader:id/bookcover_container")), WAIT_UI_TIMEOUT);
            if (covers.size() == 2)
                break;
        }
        return downloaded;
    }

    private boolean downloadEpisode(Episode episode, int cureps) {
        // check format is PDF
        if (!episode.getFormat().equals("PDF")) {
            return false;
        }

        // 閱讀
        UiObject2 object = waitObject2(By.res("com.she.eReader:id/btn_download_read"));
        String download_read = object.getText();
        if (object.getText().equals("閱讀")) {
            return false;
        }

        // check already in mJsonBooks or not
        String bname = episode.getBookName();
        if (bname.charAt(0) == '.') {
            // Log.d(TAG, " book_name " + bname + " has .");
            bname = bname.substring(1, bname.length());
        }
        if (!(bname.contains("中國時報精華版") || bname.contains("工商時報精華版"))) {
            if (mJsonBooks.contains(bname)) {
                // Log.d(TAG, " book_name " + bname + " already in mJsonBooks");
                return false;
            } else {
                Log.d(TAG, " book_name " + bname + " not in mJsonBooks");
            }
        }

        // TODO(yumaokao): comment out if mJsonBooks works with fresh run
        // check publishdate
        /* String category = episode.getCategory();
        Calendar now = Calendar.getInstance();
        if (category.equals("雜誌-報紙")) {
            now.add(Calendar.DATE, -3);
        } else {
            now.add(Calendar.MONTH, -2);
        }
        Date before = now.getTime();
        Date publishdate = episode.getPublishDate();
        if (cureps > 1 && category.startsWith("雜誌") && publishdate.before(before)) {
            return false;
        } */

        // 下載
        object = waitObject2(By.res("com.she.eReader:id/btn_download_read"));
        object.click();
        long starttime = System.currentTimeMillis();
        object = waitObject2(By.res("com.she.eReader:id/btn_download_read"));
        while (!object.getText().equals("閱讀")) {
            if (object.getText().equals("下載")) {
                object.click();
            }
            try {
                Thread.sleep(WAIT_UI_TIMEOUT);
            } catch (Exception e) {
            }
            if (System.currentTimeMillis() - DOWNLOAD_TIMEOUT > starttime) {
                return false;
            }
            object = waitObject2(By.res("com.she.eReader:id/btn_download_read"));
        }

        Log.d(TAG, "downloaded episode " + episode);
        return true;
    }

    private UiObject2 waitObject2(BySelector selector) {
        return waitObject2(selector, WAIT_TIMEOUT);
    }

    private UiObject2 waitObject2(BySelector selector, long timeout) {
        UiObject2 object = null;
        object = mDevice.wait(Until.findObject(selector), timeout);
        if (object == null)
            object = mDevice.wait(Until.findObject(selector), timeout / 2);
        if (object == null)
            fail();
        return object;
    }

    /**
     * Uses package manager to find the package name of the device launcher. Usually this package
     * is "com.android.launcher" but can be different at times. This is a generic solution which
     * works on all platforms.`
     */
    private String getLauncherPackageName() {
        // Create launcher Intent
        final Intent intent = new Intent(Intent.ACTION_MAIN);
        intent.addCategory(Intent.CATEGORY_HOME);

        // Use PackageManager to get the launcher package name
        PackageManager pm = InstrumentationRegistry.getContext().getPackageManager();
        ResolveInfo resolveInfo = pm.resolveActivity(intent, PackageManager.MATCH_DEFAULT_ONLY);
        return resolveInfo.activityInfo.packageName;
    }
}
