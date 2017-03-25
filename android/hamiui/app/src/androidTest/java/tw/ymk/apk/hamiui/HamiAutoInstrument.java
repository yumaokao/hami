package tw.ymk.apk.hamiui;

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

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


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
    private UiDevice mDevice;
    private static final int LAUNCH_TIMEOUT = 5000;
    private static final int WAIT_TIMEOUT = 30000;

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
    public void autoHamiDownload() throws Exception {
        String date;

        // date = updateBooks();

        iterateBooks();
    }

    private int iterateBooks() {
        UiObject2 object = null;
        List<UiObject2> books = new ArrayList<UiObject2>();
        List<UiObject2> lastbooks = new ArrayList<UiObject2>();
        boolean scroll = true;
        int downloads = 0;

        // 書單
        object = waitObject2(By.res("com.she.eReader:id/main_footer_tab2_txtV"));
        object.click();

        // 新上架書籍
        object = waitObject2(By.textContains("新上架書籍"));
        object.click();

        while (scroll) {
            books = mDevice.wait(Until.findObjects(By.res("com.she.eReader:id/tv_booklist_item_book_name")), WAIT_TIMEOUT);
            List<UiObject2> newbooks = new ArrayList<UiObject2>(books);
            List<String> booknames = new ArrayList<String>();
            newbooks.removeAll(lastbooks);
            // List<String> booknames = newbooks.stream().map(b -> b.getText()).collect(Collectors.toList());

            for (UiObject2 obj : newbooks) {
                booknames.add(obj.getText());
            }

            for (String bookname : booknames) {
                UiObject2 obj = null;
                UiObject2 back = null;

                obj = waitObject2(By.textContains(bookname));
                obj.click();
                downloadEpisodes();
                back = waitObject2(By.res("com.she.eReader:id/rl_toolbar_back"));
                back.click();
                break;
            }

            lastbooks = books;
            // scoll down
            object = waitObject2(By.res("com.she.eReader:id/book_listV"));
            scroll = object.scroll(Direction.DOWN, 0.5F);
            scroll = false;
        }

        return downloads;

    }

    private String updateBooks() {
        UiObject2 object = null;

        // 設定
        object = waitObject2(By.res("com.she.eReader:id/main_footer_tab4_txtV"));
        object.click();

        // 立即更新書單
        object = waitObject2(By.res("com.she.eReader:id/rl_update_booklist"));
        object.click();

        // 上次更新時間：2017-03-22 上午 11:10 成功
        object = waitObject2(By.textStartsWith("上次更新時間"), 30000);
        object = waitObject2(By.textStartsWith("上次更新時間"), 30000);
        Log.d(TAG, "updated: " + object.getText());

        return object.getText();
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

        object = waitObject2(By.res("com.she.eReader:id/book_name"));
        book_name = object.getText();
        object = waitObject2(By.res("com.she.eReader:id/author"));
        author = object.getText();
        object = waitObject2(By.res("com.she.eReader:id/publisher"));
        publisher = object.getText();
        object = waitObject2(By.res("com.she.eReader:id/format"));
        format = object.getText();
        object = waitObject2(By.res("com.she.eReader:id/publishdate"));
        publishdate = object.getText();
        object = waitObject2(By.res("com.she.eReader:id/category"));
        category = object.getText();

        info.click();

        epi = new Episode(book_name, author, publisher, format, publishdate, category);
        return epi;
    }

    private List<String> downloadEpisodes() {
        List<UiObject2> covers = new ArrayList<UiObject2>();
        UiObject2 current = null;
        UiObject2 last = null;
        Episode episode = null;

        covers = mDevice.wait(Until.findObjects(By.res("com.she.eReader:id/bookcover_container")), 5000);
        current = covers.get(0);
        episode = getEpisodeInfo();
        Log.d(TAG, "episode " + episode);
        while (!current.equals(last)) {
            last = current;
            covers = mDevice.wait(Until.findObjects(By.res("com.she.eReader:id/bookcover_container")), 5000);
            current = covers.get(covers.size() -1);
            current.click();
            episode = getEpisodeInfo();
            Log.d(TAG, "episode " + episode);
        }
        return Collections.emptyList();
    }

    private UiObject2 waitObject2(BySelector selector) {
        return waitObject2(selector, WAIT_TIMEOUT);
    }

    private UiObject2 waitObject2(BySelector selector, long timeout) {
        UiObject2 object = null;
        object = mDevice.wait(Until.findObject(selector), timeout);
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
