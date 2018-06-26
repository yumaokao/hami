.PHONY: all .

all:
	@ echo "hami android emulator"

# $ $(make .)
.:
	@ echo export PATH=$$HOME/Android/Sdk/platform-tools:$$HOME/Android/Sdk/tools/bin:$$HOME/Android/Sdk/tools:$$PATH

delete-avd: SHELL:=/bin/bash
delete-avd:
	@ [ -n $$(avdmanager list avd | grep hami) ] || avdmanager delete avd -n hami

create-avd:
	@ # sudo mount -o remount,size=8G,noatime /tmp
	@ yes | sdkmanager --licenses 
	@ sdkmanager --install "system-images;android-28;google_apis_playstore;x86_64"
	@ avdmanager --verbose create avd -c 4096M -k "system-images;android-28;google_apis_playstore;x86_64" -n hami -d "Nexus 5X"
	@ echo "hw.keyboard=yes" >> $$HOME/.android/avd/hami.avd/config.ini

run-avd:
	@ $$(which emulator) -avd hami -sdcard $$HOME/.android/avd/hami.avd/sdcard.img &

install-hami:
	@ # https://www.apkmonk.com/download-app/com.she.eReader/4_com.she.eReader_2018-06-11.apk/
	@ adb install ./com.she.eReader_*.apk
