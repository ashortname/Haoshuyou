import Tools
import time
import datetime
import sys
import os
import _thread
from requests import RequestException
from Haoshuyou import Haoshuyou
from ResultCode.ReplyCodes import ReplyCodes as rCodes


#   退出信号
EXIT_NORMAL = False
if __name__ == '__main__':
    worker = Haoshuyou()
    #   直接输入参数
    worker.spaceUrl = "http://www.93haoshu.com/home.php?mod=space&uid=337019"
    worker.formHash = "f4e5a46d"
    worker.cooKie = "UM_distinctid=1704bb9cefd1cf-05bef36d225706-b791b36-144000-1704bb9cefe830; REDX_2132_widthauto=1; CNZZDATA1278106234=2134778519-1581817004-null%7C1587023601; REDX_2132_saltkey=MK1d2KAJ; REDX_2132_lastvisit=1587539559; REDX_2132_ulastactivity=6e0bkwx%2Fm2rhM8FFYcxFlQPsW69WV%2B5uf3kNZMwiLp3vCjt1bkLU; REDX_2132_auth=0ff3I7NrEWYJBJXXPtRPyL3EO4YtvhO2Z8iS5fWIJz%2BmtXoxB7HV56M%2B1FO4lJ28a8WdQJXJem0nurIEKbI72djtB5I; REDX_2132_lastcheckfeed=337019%7C1587543171; REDX_2132_security_cookiereport=3a351jcMheo1iQErGeAHierVxyaxpMzljXrgmG3B9SlWa80WxmPj; REDX_2132_nofavfid=1; REDX_2132_styleuid=337019; REDX_2132_styleid=2; REDX_2132_visitedfid=76; REDX_2132_smile=1D1; _nodecache_cc_fce4e481f9823a7d=4ae741468fa6787629b5670a583f30f2-1587544912; REDX_2132_sid=LJ0uM1; REDX_2132_lip=36.157.146.158%2C1587544950; REDX_2132_sendmail=1; REDX_2132_st_t=337019%7C1587545646%7C1509cd4251a8de5b404fb718b59a49db; REDX_2132_forum_lastvisit=D_76_1587545646; REDX_2132_checkpm=1; REDX_2132_lastact=1587545652%09forum.php%09viewthread; REDX_2132_st_p=337019%7C1587545652%7C8886c3e2af9eea8e54e22553a13d975b; REDX_2132_viewid=tid_511206"
    workMode = 2
    #  检测用户目录
    if os.path.exists("Log/{0}".format(worker.UserName)) is not True:
        os.makedirs("Log/{0}".format(worker.UserName))
    #   初始化银币数目
    worker.Ybcount = 0
    #   设置超时时间
    worker.httpTimeOut = 30
    #   尝试加载用户回复，加载失败则启用默认配置
    worker.messages = Tools.getMessages()
    #   尝试加载回复板块，加载失败则启用默认配置
    worker.Sections = Tools.getSections()
    # 开始时间
    worker.starTime = datetime.datetime.now()
    # 日志名时间戳和路径
    worker.logFileName = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    worker.logFilePath = "Log/{0}/{1}".format(worker.UserName, worker.logFileName)
    #  如果是 windows
    if Tools.is_os_of('windows'):
        '''
        ##  显示运行时间
        '''
        #   必须初始化
        Tools.gTime = int(0)
        Tools.day = int(0)
        _thread.start_new_thread(Tools.doShowTime, (worker.UserName,))
    '''
        ##  正式的工作
        '''
    while True:
        try:
            # 加载已访问帖子目录
            worker.loadLastVisited()
            # 登陆
            # worker.log('正在登录...')
            # worker.login(worker.UserName, worker.PassWord)
            worker.tryWork()
            time.sleep(5)
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
                    replyResult, replyCode, replyResponse = worker.isReplySuccess(responseText)
                    worker.log("Reply : {0}".format(replyResult))
                    #   可能是 session 失效了，尝试重新登陆
                    if (replyResult is not True) and replyCode == rCodes.CODE_ReplyFailedAnyway:
                        continue
                    if (replyResult is not True) and replyCode == rCodes.CODE_ReplyReachLimit:
                        worker.log("\t!!!Error: 发帖已到达限制...\n\n")
                        EXIT_NORMAL = True
                        break
                    #   回帖成功，存入记录
                    if (page not in worker.lastVisited) and (page not in worker.visited):
                        worker.visited.append(page.tid)
                    #   回帖数加一
                    worker.postCount = worker.postCount + 1

                    time.sleep(1)
                    #   计算银币
                    cYb = worker.getMyYb()
                    different = cYb - worker.currentYb
                    worker.Ybcount += different
                    worker.currentYb = cYb
                    worker.log("当前银币： {0} 枚, 当前回帖： {1} 帖， 本次回复得到银币： {2} 枚, 当前总共获得： {3} 枚\n".format(
                        worker.currentYb, worker.postCount, different, worker.Ybcount
                    ))
                    #   等待至少3分钟
                    time.sleep(Tools.getRandTime(workMode))
                except KeyboardInterrupt as kex:
                    worker.log('检测到中断信号，程序退出...\n')
                    EXIT_NORMAL = True
                    break
                except Exception as exception:
                    worker.log("工作中出现错误!!!  exception: " + exception.__str__())
                    worker.log("5 秒后尝试重新登陆...\n")
                    time.sleep(5)
                    continue
        except Exception as exception:
            #   抛出的登录失败
            if '失败' in exception.__str__():
                EXIT_NORMAL = True
                break
            worker.log("初始化错误!!! " + exception.__str__())
            continue
        except RequestException as reException:
            worker.log('访问错误，尝试重启程序...' + reException.__str__())
            continue
        finally:
            #   计算运行时间
            worker.endTime = datetime.datetime.now()
            runTime = worker.endTime - worker.starTime
            worker.log(
                "当次运行总共耗时： {0}， 共回复： {1} 帖， 总计获得银币： {2} 枚\n--------------------------------------------------------------\n\n".format(
                    runTime, worker.postCount, worker.Ybcount
                ))
            #   写入当次访问记录
            worker.writeVisited()
            #   如果正常退出
            if EXIT_NORMAL is True:
                break
            #   检测到不可处理错误，1分钟后再试
            print('未处理错误，10 秒后重试！！！\n')
            time.sleep(9)
            print('现在开始重新执行任务...\n')
            time.sleep(1)
    print('\n程序退出...\n')
