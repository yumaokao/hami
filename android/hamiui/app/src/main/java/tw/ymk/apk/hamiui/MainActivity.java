package tw.ymk.apk.hamiui;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "hamiui";
    Button button_hamigo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        button_hamigo = (Button) findViewById(R.id.button_hamigo);
    }

    public void hamigo_click(View v) {
        Log.d(TAG, "hamiauto_download");
        new UiAutomatorThread().run();
    }

    class UiAutomatorThread extends Thread {
        private String command = "am instrument --user 0 -w -r   -e debug false"
                + " -e class tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload"
                + " tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner";

        @Override
        public void run() {
            super.run();
            int error = Subprocess.check_call(command);
            Log.d(TAG, "UiAutomator result: " + error);
        }
    }
}
