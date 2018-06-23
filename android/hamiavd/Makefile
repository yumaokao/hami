.PHONY: all .

all:
	@ echo "hami android emulator"

# $ $(make .)
.:
	@ echo export PATH=$$HOME/Android/Sdk/tools/bin/:$$PATH

delete-avd:
	@ [ -n $$(avdmanager list avd | grep hami) ] || avdmanager delete avd -n hami
