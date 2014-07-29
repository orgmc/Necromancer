import time
import thread
import os


def click(sleeptime):
    while True:
        os.popen(""" curl  'http://172.30.10.146:8080/trace?offer_id=65536&aff_id=65536&aff_sub=affsub&aff_sub2=affsub2&aff_sub3=affsub3&aff_sub4=affsub4&aff_sub5=affsub5&aff_sub6=affsub6&aff_sub7=affsub7&aff_sub8=affsub8' -A "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5" -i -l --header "referer:http://www.65536_click_1913.com" -H x-forwarded-for:54.86.55.142 """).read()
        time.sleep(sleeptime)
    thread.exit_thread()

def test(): #Use thread.start_new_thread() to create 2 new threads
    for i in range(10):
        thread.start_new_thread(click,(0.1,))


if __name__=='__main__':
    test()
    time.sleep(24*3600)
