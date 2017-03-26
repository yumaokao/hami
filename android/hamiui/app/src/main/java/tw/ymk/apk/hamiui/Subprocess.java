package tw.ymk.apk.hamiui;

import android.util.Log;

/**
 * Created by yumaokao on 2017/3/26.
 */

public class Subprocess {
    private static final String TAG = "hamiui.subprocess";

    public static class Result {
        public int error;
        public String stdout;
        public String stderr;

        public Result(int error, String stdout, String stderr) {
            this.error = error;
            this.stdout = stdout;
            this.stderr = stderr;
        }
    }

    public static int check_call(String command) {
        Log.d(TAG, "check_call: " + command);
        int error = -1;
        try {
            Process process = Runtime.getRuntime().exec(command);
            error = process.waitFor();
            Log.e(TAG, "Return: " + error);
        } catch (Exception e) {
            Log.e(TAG, "Error: " + command);
            e.printStackTrace();
        }
        return error;
    }
}
