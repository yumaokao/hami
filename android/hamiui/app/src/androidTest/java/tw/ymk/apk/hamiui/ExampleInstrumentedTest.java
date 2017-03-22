package tw.ymk.apk.hamiui;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;
import android.support.test.uiautomator.By;
import android.support.test.uiautomator.BySelector;
import android.support.test.uiautomator.UiDevice;
import android.support.test.filters.SdkSuppress;
import android.support.test.uiautomator.UiObject;
import android.support.test.uiautomator.UiObject2;
import android.support.test.uiautomator.Until;
import android.util.Log;


import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.hamcrest.core.IsNull.notNullValue;
import static org.junit.Assert.*;

/**
 * Instrumentation test, which will execute on an Android device.
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
@RunWith(AndroidJUnit4.class)
@SdkSuppress(minSdkVersion = 18)
public class ExampleInstrumentedTest {

    private static final String BASIC_SAMPLE_PACKAGE = "com.she.eReader";
    private UiDevice mDevice;
    private static final int LAUNCH_TIMEOUT = 5000;

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
        Log.d("hamiui", "package name " + appContext.getPackageName());
        assertEquals("tw.ymk.apk.hamiui", appContext.getPackageName());
    }

    @Test
    public void autoHamiDownload() throws Exception {
        UiObject2 object = null;

        // 設定
        object = waitObject2(By.res("com.she.eReader:id/main_footer_tab4_txtV"), 5000);
        object.click();

        // 立即更新書單
        object = waitObject2(By.res("com.she.eReader:id/rl_update_booklist"), 5000);
        object.click();

        // 上次更新時間：2017-03-22 上午 11:10 成功
        object = waitObject2(By.textStartsWith("上次更新時間"), 30000);
        object = waitObject2(By.textStartsWith("上次更新時間"), 30000);
        Log.d("hamiui", "updated: " + object.getText());

        // 書單
        object = waitObject2(By.res("com.she.eReader:id/main_footer_tab2_txtV"), 5000);
        object.click();

        // 新上架書籍
        object = waitObject2(By.textContains("新上架書籍"), 30000);
        object.click();
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
