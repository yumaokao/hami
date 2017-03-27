# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import time
import schedule
import subprocess


def hamiui():
    # adb shell am instrument -w -r   -e debug false
    #   -e class tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload
    #   tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner
    # ssh 192.168.10.136 -p 8022 python hami/rev.py
    subprocess.check_call('adb shell am instrument -w -r   -e debug false -e class'
            + ' tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload'
            + ' tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner', shell=True)
    subprocess.check_call('ssh 192.168.10.136 -p 8022 python hami/rev.py', shell=True)
    subprocess.check_call('date', shell=True)


def main():
    schedule.every().hours.do(hamiui)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
