.PHONY: all .

all:
	@ echo "hami android emulator"

# $ $(make .)
.:
	@ echo export PATH=$$HOME/Android/Sdk/tools/bin:$$HOME/Android/Sdk/tools:$$PATH

delete-avd:
	@ [ -n $$(avdmanager list avd | grep hami) ] || avdmanager delete avd -n hami

create-avd:
	@ # sudo mount -o remount,size=8G,noatime /tmp
	@ yes | sdkmanager --licenses 
	@ sdkmanager --install "system-images;android-28;google_apis_playstore;x86_64"
	@ avdmanager --verbose create avd -c 4096M -k "system-images;android-28;google_apis_playstore;x86_64" -n hami -d "Nexus 5X"

run-avd:
	@ $$(which emulator) -avd hami -sdcard $$HOME/.android/avd/hami.avd/sdcard.img &

install-hami:
	@ adb install ./Hami*.apk
