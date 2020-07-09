# 挂机使用
import sys
import os
import datetime
import time
from Haoshuyou import Haoshuyou

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
            while worker.awardStatus:
                try:
                    delayTime = 60 * 3
                    worker.tickEnter(worker.PROTOCOL + worker.MAIN_HOST)
                    while delayTime >= 0:
                        slist = ["\\", "|", "/", "-"]
                        delayTime = delayTime - 1
                        # \r 默认将指针返回到最开始后输出（在原位置再次输出）
                        print('\n')
                        print('\r=== 程序运行中：' + slist[delayTime % 4] + ' ' + str(delayTime) + ' s', end='')
                        time.sleep(1)
                    print('\n')
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
            break
        if EXIT_SIGN:
            break
        worker.log("等待...")
        time.sleep(5)
        worker.log('重新登录...\n')
    worker.log('结束挂机...\n')
