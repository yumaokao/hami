# hami

## hamiui
### commandline
Need to install app-debug.apk again, to make `am instrument` work.
`am instument` works, `python cron.py` works.

```sh
# connectedAndroidTest
$ ./gradlew cAT

# build apks
$ ./gradlew :app:assembleDebug :app:assembleDebugAndroidTest
$ adb install -r app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
$ adb install -r app/build/outputs/apk/debug/app-debug.apk
$ adb shell "am instrument -w -r -e debug false -e class tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner"
```

### reboot
```sh
$ adb shell reboot
$ adb shell input keyevent 82
$ python cron.py
```

### screencap
```sh
$ adb shell screencap -p /data/local/tmp/hami.png && adb pull /data/local/tmp/hami.png ./
$ python -m http.server
```
