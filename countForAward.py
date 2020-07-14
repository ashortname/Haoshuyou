import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import time
import sys
import os
import datetime
from Haoshuyou import Haoshuyou


if __name__ == '__main__':
    worker = Haoshuyou()
    #	判断参数合法性
    if len(sys.argv) is not 4:
        print("参数有误，退出！！！\n")
        sys.exit()
    worker.UserName = str(sys.argv[1]).strip()
    worker.PassWord = str(sys.argv[2]).strip()
    page = int(sys.argv[3])
    #  检测用户目录
    if os.path.exists("Award/{0}".format(worker.UserName)) is not True:
        os.makedirs("Award/{0}".format(worker.UserName))
    worker.starTime = datetime.datetime.now()
    # 日志名时间戳和路径
    worker.logFileName = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    worker.logFilePath = "Award/{0}/{1}".format(worker.UserName, worker.logFileName)

    cLogin = int(0)
    EXIT = False
    awardCount = [0] * 6
    while not EXIT:
        # 登录
        while True:
            try:
                worker.log('正在登录...')
                worker.login(worker.UserName, worker.PassWord)
                cLogin = 0
                break
            except:
                cLogin = cLogin + 1
                if cLogin >= 8:
                    worker.log('登陆失败次数过多，程序退出...')
                    sys.exit()
                time.sleep(1)
                worker.log('重新登录...')
                time.sleep(4)
        # 计算
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.93book.com',
            'Referer': 'http://www.93book.com/plugin.php?id=it618_award:award',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        }
        # 获取session
        mysession = worker.session
        while True:
            try:
                url = "http://www.93book.com/plugin.php?id=it618_award:ajax&page={0}&formhash={1}&ac=myaward_get".format(page, worker.formHash)
                with mysession.get(url=url, headers=headers, timeout=worker.httpTimeOut) as response:
                    response.encoding = 'gbk'
                    bs_obj = BeautifulSoup(response.text, 'html.parser')
                    fonts = bs_obj.find_all('font', {'color': '#F60'})
                    # 最后一页的下一页
                    if fonts.__len__() == 0:
                        EXIT = True
                        worker.log('全部统计完毕')
                        break
                    for font in fonts:
                        if str(font.string).strip() == '一等奖':
                            awardCount[0] = awardCount[0] + 1
                        elif str(font.string).strip() == '二等奖':
                            awardCount[1] = awardCount[1] + 1
                        elif str(font.string).strip() == '三等奖':
                            awardCount[2] = awardCount[2] + 1
                        elif str(font.string).strip() == '四等奖':
                            awardCount[3] = awardCount[3] + 1
                        elif str(font.string).strip() == '五等奖':
                            awardCount[4] = awardCount[4] + 1
                        elif str(font.string).strip() == '六等奖':
                            awardCount[5] = awardCount[5] + 1
                # 记录
                worker.log('page: ' + str(page))
                worker.log('统计：' + str(awardCount))
                # 下一页
                page = page + 1
                time.sleep(2)
            except Exception as ex:
                worker.log('出错：' + ex.__str__())
                time.sleep(1)
                worker.login('重新登陆...')
                time.sleep(4)
    # 这里是程序退出
