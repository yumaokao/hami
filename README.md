# hami

## hamiui
### commandline
Need to install app-debug.apk again, to make `am instrument` work.
`am instument` works, `python cron.py` works.

```sh
$ ./gradlew cAT
$ adb install app/build/outputs/apk/app-debug-androidTest.apk
$ adb install app/build/outputs/apk/app-debug.apk
$ adb shell "am instrument -w -r -e debug false -e class tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner"
```

### reboot
```sh
$ adb shell reboot
$ adb shell input keyevent 82
$ python cron.py
```
