# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import time
import schedule
import subprocess


def hamiui():
    # adb shell am instrument -w -r   -e debug false
    #   -e class tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload
    #   tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner
    # ssh 192.168.10.136 -p 8022 python hami/rev.py
    try:
        subprocess.check_call('adb -s 056da2b2344483e8 shell'
                + ' am start -n com.termux/com.termux.app.TermuxActivity', shell=True)
        subprocess.check_call('date', shell=True)
        subprocess.check_call('adb -s 056da2b2344483e8 shell'
                + ' am instrument -w -r   -e debug false -e class'
                + ' tw.ymk.apk.hamiui.HamiAutoInstrument#autoHamiDownload'
                + ' tw.ymk.apk.hamiui.test/android.support.test.runner.AndroidJUnitRunner', shell=True)
        subprocess.check_call('scp rev.py ymknexus5:hami/rev.py', shell=True)
        subprocess.check_call('ssh ymknexus5 python hami/rev.py', shell=True)
        subprocess.check_call('python hamiorg/hamiorg.py', shell=True)
        subprocess.check_call('date', shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
    except:
        print('unknown error')


def main():
    schedule.every().hours.do(hamiui)
    schedule.every().day.at("00:30").do(hamiui)
    schedule.every().day.at("07:15").do(hamiui)
    schedule.every().day.at("07:30").do(hamiui)
    schedule.every().day.at("07:45").do(hamiui)
    schedule.every().day.at("08:15").do(hamiui)
    schedule.every().day.at("16:15").do(hamiui)
    schedule.every().day.at("16:30").do(hamiui)
    schedule.every().day.at("16:45").do(hamiui)
    schedule.every().day.at("17:15").do(hamiui)

    hamiui()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
