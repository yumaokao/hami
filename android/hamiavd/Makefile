
.PHONY: all .
all:
	@ echo "hami android emulator"

# $ $(make .)
.PHONY: .
.:
	@ echo export PATH=$$HOME/Android/Sdk/platform-tools:$$HOME/Android/Sdk/tools/bin:$$HOME/Android/Sdk/tools:$$PATH

.PHONY: delete-avd
delete-avd: SHELL:=/bin/bash
delete-avd:
	@ [ -n $$(avdmanager list avd | grep hami) ] || avdmanager delete avd -n hami

.PHONY: create-avd
create-avd:
	@ # sudo mount -o remount,size=8G,noatime /tmp
	@ yes | sdkmanager --licenses 
	@ sdkmanager --install "system-images;android-28;google_apis_playstore;x86_64"
	@ avdmanager --verbose create avd -c 4096M -k "system-images;android-28;google_apis_playstore;x86_64" -n hami -d "Nexus 5X"
	@ echo "hw.keyboard=yes" >> $$HOME/.android/avd/hami.avd/config.ini
	@ echo "disk.dataPartition.size=4096MB" >> $$HOME/.android/avd/hami.avd/config.ini

.PHONY: run-avd
run-avd:
	@ $$(which emulator) -avd hami -sdcard $$HOME/.android/avd/hami.avd/sdcard.img &

.PHONY: install-hami
install-hami:
	@ # https://www.apkmonk.com/download-app/com.she.eReader/4_com.she.eReader_2018-06-11.apk/
	@ adb install ./com.she.eReader_*.apk

# hamiui
HAMIUI := $(realpath ../hamiui)
.PHONY: hamiui-build_apks
hamiui-build_apks:
	@ cd $(HAMIUI) && ./gradlew :app:assembleDebug :app:assembleDebugAndroidTest

.PHONY: hamiui-run
hamiui-run: hamiui-build_apks
	@ adb install -r $(HAMIUI)/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
	@ adb install -r $(HAMIUI)/app/build/outputs/apk/debug/app-debug.apk
	@ adb shell "am instrument -w -r -e debug false -e class tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner"
