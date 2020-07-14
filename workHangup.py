# 挂机使用
import sys
import os
import datetime
import time
from Haoshuyou import Haoshuyou


#   延迟函数
def delay(message, second):
    ll = len(str(second))
    spot = ['\\', '-', '/', '|']
    while second >= 0:
        print(str.format("\r{0} {3} : {1:>{2}d} s", message, second, ll, spot[second % spot.__len__()]), end='')
        second = second - 1
        time.sleep(1)
    print('\n')


EXIT_SIGN = False
if __name__ == '__main__':
    worker = Haoshuyou()
    worker.UserName = str(sys.argv[1]).strip()
    worker.PassWord = str(sys.argv[2]).strip()
    workMode = int(sys.argv[3])
    #  检测用户目录
    if os.path.exists("Hangup/{0}".format(worker.UserName)) is not True:
        os.makedirs("Hangup/{0}".format(worker.UserName))
        # 开始时间
    worker.starTime = datetime.datetime.now()
    # 日志名时间戳和路径
    worker.logFileName = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    worker.logFilePath = "Hangup/{0}/{1}".format(worker.UserName, worker.logFileName)
    worker.log('开始挂机...\n')
    while worker.awardStatus:
        try:
            worker.log('正在登录...')
            worker.login(worker.UserName, worker.PassWord)
            while True:
                try:
                    delayTime = 60 * 3
                    worker.tickEnter(worker.PROTOCOL + worker.MAIN_HOST)
                    if worker.awardStatus is False:
                        EXIT_SIGN = True
                        break
                    #while delayTime >= 0:
                    # slist = ["\\", "|", "/", "-"]
                    # \r 默认将指针返回到最开始后输出（在原位置再次输出）
                    delay('=== 程序正在运行中', delayTime)
                    # print(str.format("\r=== 程序正在运行中：{0} {1:>3d} s", slist[delayTime % 4], delayTime), end='')
                    # print('\r=== 程序运行中：' + slist[delayTime % 4] + ' ' + str(delayTime) + ' s', end='')
                    time.sleep(1)
                    delayTime = delayTime - 1
                except KeyboardInterrupt as kex:
                    print('\n')
                    worker.log('检测到中断信号，程序退出...\n')
                    EXIT_SIGN = True
                    break
                except Exception as ex:
                    worker.log(ex.__str__())
                    break
        except Exception as ex:
            worker.log(ex.__str__())
        if EXIT_SIGN:
            break
        else:
            delay('即将重新登陆：', 5)
            worker.log('重新登录...\n')
    try:
        worker.logout()
    except:
        pass
    worker.log('***************************')
    worker.log('*\t\t结束挂机\t\t*')
    worker.log('***************************\n')
