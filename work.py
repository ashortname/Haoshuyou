from Haoshuyou import Haoshuyou
from ResultCode.ReplyCodes import ReplyCodes as rCodes
import Tools
import time
import random
import datetime
import sys
import os
from requests import RequestException


def getRandTime(Mode):
    if Mode == 1:
        otime = 120
    else:
        otime = 30
    ext = random.randint(70, 90)
    return otime + ext


#	退出信号
EXIT_NORMAL = False
if __name__ == '__main__':
    worker = Haoshuyou()
    #   工作模式，决定回帖间隔
    workMode = 1
    #	判断参数合法性
    if len(sys.argv) is not 4:
        print("参数有误，退出！！！\n")
        sys.exit()
    #   从命令行获取参数
    worker.UserName = str(sys.argv[1]).strip()
    worker.PassWord = str(sys.argv[2]).strip()
    workMode = int(sys.argv[3])
    #  检测用户目录
    if os.path.exists("Log/{0}".format(worker.UserName)) is not True:
        os.makedirs("Log/{0}".format(worker.UserName))
    #   初始化银币数目
    worker.Ybcount = 0
    #   设置超时时间
    worker.httpTimeOut = 20
    #   尝试加载用户回复，加载失败则启用默认配置
    try:
        tMsgs = Tools.getMessages()
        if len(tMsgs) == 0:
            raise Exception('ContentEmpty!')  
        worker.messages = tMsgs
    except Exception as exception:
        worker.log('加载用户回复失败，启用默认设置！！！')
    #   尝试加载回复板块，加载失败则启用默认配置
    try:
        tSecs = Tools.getSections()
        if len(tSecs) == 0:
            raise Exception('ContentEmpty!')
        worker.Sections = tSecs
    except Exception as exception:
        worker.log('加载回复板块失败，启用默认设置！！！')
    '''
    ##  正式的工作
    '''
    while True:
        try:
            # 开始时间
            worker.starTime = datetime.datetime.now()
            # 日志名时间戳和路径
            worker.logFileName = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
            worker.logFilePath = "Log/{0}/{1}".format(worker.UserName, worker.logFileName)
            # 加载已访问帖子目录
            worker.loadLastVisited()
            # 登陆
            worker.login(worker.UserName, worker.PassWord)
            # 工作
            while True:
                try:
                    # 获取板块
                    plateUrl = worker.getPlate()
                    worker.getMenu(plateUrl)
                    # 获取目标页面
                    page = worker.getTargetPage()
                    worker.enterUrl(page.pageUrl, plateUrl)
                    # 获取回复内容
                    message = worker.getMessage()
                    worker.log(message)
                    # 拼接回复地址
                    sendUrl = "http://www.93haoshu.com/forum.php?mod=post&action=reply&fid={0}&tid={1}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1".format(
                        worker.fid, page.tid)
                    sendData = {
                        'select': '',
                        'message': message.encode('gbk'),
                        'formhash': worker.formHash,
                        'usesig': '1',
                        'subject': '  '
                    }
                    responseText = worker.sendResponse(sendUrl, sendData, page.tid)
                    replyResult, replyCode = worker.isReplySuccess(responseText)
                    worker.log("Reply : {0}".format(replyResult))
                    #   可能是 session 失效了，尝试重新登陆
                    if (replyResult is not True) and replyCode == rCodes.CODE_ReplyFailedAnyway:
                        worker.log("回复失败， 5 秒后尝试重新登陆!!! \n")
                        time.sleep(5)
                        worker.logout()
                        worker.login(worker.UserName, worker.PassWord)
                        continue
                    if (replyResult is not True) and replyCode == rCodes.CODE_ReplyReachLimit:
                        worker.log("\t!!!Error: 发帖已到达限制...\n\n")
                        EXIT_NORMAL = True
                        break
                    #   回帖成功，存入记录
                    if (page not in worker.lastVisited) and (page not in worker.visited):
                        worker.visited.append(page.tid)
	    
                    time.sleep(1)
                    cYb = worker.getMyYb()
                    different = cYb - worker.currentYb
                    worker.Ybcount += different
                    worker.currentYb = cYb
                    worker.log("当前银币： {0} 枚, 本次回复得到银币： {1} 枚, 当前总共获得： {2} 枚\n".format(
                        worker.currentYb, different, worker.Ybcount
                    ))
                    #   等待至少3分钟
                    time.sleep(getRandTime(workMode))
                except KeyboardInterrupt as kex:
                    worker.log('检测到中断信，程序退出...\n')
                    EXIT_NORMAL = True
                    break
                except Exception as exception:
                    worker.log("工作中出现错误!!!  exception: " + exception.__str__())
                    worker.log("5 秒后尝试重新登陆...\n")
                    time.sleep(5)
                    worker.log('try login...')
                    worker.login(worker.UserName, worker.PassWord)
                    continue
        except Exception as exception:
            worker.log("初始化错误!!! " + exception.__str__())
            continue
        except RequestException as reException:
            worker.log('访问错误，尝试重启程序...' + reException.__str__())
            continue
        finally:
            #   写入当次访问记录
            worker.writeVisited()
            #   计算运行时间
            worker.endTime = datetime.datetime.now()
            runTime = worker.endTime - worker.starTime
            worker.log("当次运行总共耗时： {0}， 共回复： {1} 帖， 总计获得银币： {2} 枚\n--------------------------------------------------------------\n\n".format(
                runTime,  len(worker.visited), worker.Ybcount
            ))
            #   登出
            worker.logout()
            #   如果正常退出
            if EXIT_NORMAL is True:
                break
            #   检测到不可自愈错误，1分钟后再试
            print('未处理错误，3 秒后重试！！！\n')
            time.sleep(3)
            print('现在开始重新执行任务...\n')
            time.sleep(1)
    print('\n程序退出...\n')
