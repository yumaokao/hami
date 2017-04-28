# hami

## hamiui
### commandline
```sh
$ ./gradlew cAT
$ adb shell "am instrument -w -r -e debug false -e class tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner"
```
