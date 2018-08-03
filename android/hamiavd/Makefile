
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
	@ [ -z "$$(avdmanager list avd | grep hami)" ] || avdmanager delete avd -n hami

.PHONY: create-avd
create-avd:
	@ # sudo mount -o remount,size=8G,noatime /tmp
	@ yes | sdkmanager --licenses 
	@ sdkmanager --install "system-images;android-25;google_apis;x86_64"
	@ avdmanager --verbose create avd -c 4096M -k "system-images;android-25;google_apis;x86_64" -n hami -d "Nexus 5X"
	@ echo "hw.keyboard=yes" >> $$HOME/.android/avd/hami.avd/config.ini
	@ echo "disk.dataPartition.size=4096MB" >> $$HOME/.android/avd/hami.avd/config.ini

.PHONY: run-avd
run-avd:
	@ # $$(which emulator) -avd hami -sdcard $$HOME/.android/avd/hami.avd/sdcard.img &
	@ $$(which emulator) -memory 2048 -avd hami -sdcard $$HOME/.android/avd/hami.avd/sdcard.img &

.PHONY: tar-avd
tar-avd:
	@ mkdir -p avd
	@ cp $$HOME/.android/avd/hami.ini avd/
	@ cd avd && tar zcf hami.avd.tar.gz $$HOME/.android/avd/hami.avd

.PHONY: install-hami
install-hami:
	@ # https://www.apkmonk.com/download-app/com.she.eReader/4_com.she.eReader_2018-06-11.apk/
	@ adb install ./com.she.eReader_*.apk

.PHONY: install-termux
install-termux:
	@ [ -f com.termux_64.apk ] || wget https://f-droid.org/repo/com.termux_64.apk
	@ [ -f com.termux.boot_5.apk ] || wget https://f-droid.org/repo/com.termux.boot_5.apk
	@ adb install -r com.termux_64.apk
	@ adb install -r com.termux.boot_5.apk

.PHONY: forward-termux
forward-termux:
	@ [ -n "$(adb forward --list | grep tcp:8022)" ] || adb forward tcp:8022 tcp:8022

.PHONY: ssh-termux
ssh-termux: forward-termux
	@ ssh localhost -p 8022

.PHONY: setup-termux
setup-termux:
	@ echo "pkg install openssh"
	@ echo "scp yumaokao@plet.ymk.tw:.ssh/authorized_keys ./.ssh/"
	@ echo "sshd"
	@ echo "mkdir -p ~/.termux/boot"
	@ echo "echo sshd >> ~/.termux/boot/start-sshd"

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

.PHONY: hamiui-logcat
hamiui-logcat:
	@ adb logcat -s HAMIUI:D

# hamiorg
HAMIORG := $(realpath ../hamiorg)
.PHONY: hamiorg-rev
hamiorg-setup: forward-termux
	@ ssh localhost -p 8022 pkg install -y python
	@ ssh localhost -p 8022 pkg install -y python-dev
	@ ssh localhost -p 8022 pkg install -y clang
	@ ssh localhost -p 8022 pkg install -y libxml2-dev
	@ ssh localhost -p 8022 pkg install -y libxslt-dev
	@ ssh localhost -p 8022 pkg install -y libcrypt-dev
	@ ssh localhost -p 8022 pip install --user lxml

hamiorg-rev: forward-termux
	@ ssh localhost -p 8022 mkdir -p hami
	@ scp -P 8022 $(HAMIORG)/hamirev.py localhost:hami/hamirev.py
	@ ssh localhost -p 8022 python hami/hamirev.py
