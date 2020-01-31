import requests
from bs4 import BeautifulSoup
import hashlib
import re
import urllib.parse
import time
import random
# local import
from PageModel.MenuPageModel import MenuPage
from PageModel.PageItem import PageItem
from ResultCode.ReplyCodes import ReplyCodes as rCodes


class Haoshuyou:
    cooKie = None
    session = None
    formHash = None
    fid = None
    starTime = None
    endTime = None
    logFileName = ''
    logFilePath = ''
    UserName = ''
    PassWord = ''
    currentYb = int(0)
    Ybcount = int(0)
    visited = list()
    lastVisited = list()
    messages = ["[color=Red]楼主发贴辛苦了，谢谢楼主分享！[/color]我觉得[color=blue]好书友论坛[/color]是注册对了！",
                "楼主太厉害了！楼主，我觉得[color=blue]好书友[/color]真是个好地方！",
                "这个帖子不回对不起自己！我想我是一天也不能离开[color=blue]好书友[/color]。",
                "我看不错噢 谢谢楼主！[color=blue]好书友[/color]越来越好！",
                "论坛不能没有像楼主这样的人才啊！我会一直支持[color=blue]好书友[/color]。",
                "既然你诚信诚意的推荐了，那我就勉为其难的看看吧！[color=blue]好书友[/color]不走平凡路。",
                "感谢楼主分享~",
                "[color=blue]支持一下楼主[/color]",
                "进来看看，支持一下楼主"]
    plates = ["http://www.93haoshu.com/forum-2-1.html",
              "http://www.93haoshu.com/forum-72-1.html",
              "http://www.93haoshu.com/forum-56-1.html"]
    plateNames = ["同人小说", "全本小说", "常规小说"]

    def __init__(self):
        self.Menu = None
        self.session = None
        self.Ybcount = 0

    # 获取http头
    def __getHeader(self):
        return{
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.93haoshu.com',
            'Origin': 'http: // www.93haoshu.com',
            'Referer': 'http://www.93haoshu.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    # 获取MD5值
    def getMD5(self, data):
        mmd5 = hashlib.md5()
        mmd5.update(data.encode(encoding='utf-8'))
        return mmd5.hexdigest()

    # 进行url编码
    def getUrlEncode(self, message):
        return urllib.parse.quote(message)

    # 日志
    def log(self, Message):
        msg = str.format("[{0}] {1}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), Message)
        #   输出到cmd
        print(msg)
        #   写入日志
        with open(self.logFilePath, 'a+') as file:
            file.write(msg + "\n")
            file.flush()

    """
    ##  登陆论坛，获取 cookies 和 session
    """
    def login(self, acc, passwd):
        try:
            self.session = requests.session()
            loginUrl = 'http://www.93haoshu.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
            npass = self.getMD5(passwd)
            postData = {
                'fastloginfield': 'username',
                'username': acc,
                'password': npass,
                'quickforward': 'yes',
                'handlekey': 'ls'
            }
            with self.session.post(url=loginUrl, headers=self.__getHeader(), data=postData, timeout=8) as response:
                response.encoding = 'gbk'
                bs_obj = BeautifulSoup(response.text, 'html.parser')
                fh = bs_obj.find('a', {'href': re.compile("member*")})
                self.formHash = fh['href'][-1:-9:-1][::-1]
                self.cooKie = self.session.cookies
                #   获取银币数目
                self.currentYb = self.getMyYb()                
                self.log("Login success...\n\n")
            time.sleep(1)
        except Exception as exception:
            self.log("Login failed!!! exception : " + exception.__str__())
            raise Exception("登陆出错！！！")

    """
    ##  登出论坛
    """
    def logout(self):
        try:
            url = "http://www.93haoshu.com/member.php?mod=logging&action=logout&formhash={0}".format(self.formHash)
            with self.session.get(url=url, headers=self.__getHeader(), timeout=8) as response:
                response.encoding = 'gbk'
                self.log("退出登录...")
        except Exception as exception:
            self.log("退出论坛出错！！！")

    """
    ##  进入主题页面，获取各个帖子的地址及信息
    """
    def getMenu(self, pageUrl):
        try:
            with self.session.get(url=pageUrl, headers=self.__getHeader(), timeout=8) as response:
                response.encoding = 'gbk'
                bs_obj = BeautifulSoup(response.text, 'html.parser')
                plists = bs_obj.find_all('tbody', {'id': re.compile("normalthread_*")})
                # 获取fid
                self.fid = bs_obj.find('input', {'name': 'srhfid'})['value']
                # 每个plist，先清空菜单
                self.Menu = MenuPage()
                for item in plists:
                    # print(plists[0].td.a['href'])  地址
                    tds = item.find_all('td', {'class': 'by'})
                    # print(tds[0].cite.a.get_text() + ' ' + tds[0].em.span.string + '\n') #creator
                    # print(tds[1].cite.a.get_text() + ' ' + tds[1].em.span.string) #lastvisitor
                    # num = plists[0].find('td', {'class': 'num'}).em.string
                    temp = PageItem(item.td.a['href'], item.td.a['href'].split('-')[1],
                                    tds[0].cite.a.get_text(), tds[0].em.span.string,
                                    tds[1].cite.a.get_text(), tds[1].em.span.string,
                                    item.find('td', {'class': 'num'}).em.string)
                    self.Menu.pageItemsCount += 1
                    self.Menu.pageList.append(temp)
                self.log("Menu loaded...")
                time.sleep(1)
        except Exception as exception:
            self.log("getMenu failed!!! exception : " + exception.__str__())
            raise Exception("获取板块错误！！！")

    #   获取另一个http头
    def buildHeader(self, tid):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.93haoshu.com',
            'Origin': 'http://www.93haoshu.com',
            'Referer': 'http://www.93haoshu.com/thread-{0}-1-1.html'.format(tid),
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    """
    ##  进行回复
    """
    def sendResponse(self, rUrl, message, tid):
        try:
            with self.session.post(url=rUrl, data=message, headers=self.buildHeader(tid), timeout=8) as response:
                response.encoding = 'gbk'
                return response.text
            time.sleep(1)
        except Exception as exception:
            raise Exception("发表回复出错！！！")

    #   判断是否回复成功
    def isReplySuccess(self, responseText):
        if responseText.__contains__('每小时限制'):
            return False, rCodes.CODE_ReplyReachLimit
        elif responseText.__contains__('回复发布成功'):
            return True, rCodes.CODE_ReplySuccess
        #	临时的论坛错误
        #elif responseText.__contains__('40001'):
        #    return True, rCodes.CODE_ReplySuccess
        else:
            return False, rCodes.CODE_ReplyFailedAnyway

    #   这也是回复头
    def buildHeader2(self, url):
        return {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.93haoshu.com',
            'Origin': 'http://www.93haoshu.com',
            'Referer': url,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    """
    ##  进入页面
    """
    def enterUrl(self, url, refer):
        with self.session.get(url=url, headers=self.buildHeader2(refer), timeout=8) as response:
            response.encoding = 'gbk'
            self.log("Enter page...")
        time.sleep(1)

    """
    ##  获取要回复的信息
    """
    def getMessage(self):
        index = random.randint(0, len(self.messages) - 1)
        return self.messages[index]

    """
    ##  获取要回复的板块
    """
    def getPlate(self):
        index = random.randint(0, len(self.plates) - 1)
        self.log("此次回复板块：" + self.plateNames[index])
        return self.plates[index]

    # 用于记录已经访问过的帖子 -- 加载
    def loadLastVisited(self):
        try:
            self.log("---------------------------------------------\n")
            self.log('加载本地访问记录...')
            with open("Log/{0}/visited".format(self.UserName), "a+") as visitFile:
                for line in visitFile.readlines():
                    self.lastVisited.append(line)
            time.sleep(1)
        except Exception as exception:
            self.log("读取访问记录出错！！！")

    # 用于记录已经访问过的帖子 -- 写入
    def writeVisited(self):
        try:
            self.log('正在录入本次访问记录...')
            with open("Log/{0}/visited".format(self.UserName), "a+") as visitFile:
                for item in self.visited:
                    visitFile.write(item + "\n")
                    visitFile.flush()
            time.sleep(1)
            self.log('记录录入完毕...')
        except Exception as exception:
            self.log("写入访问记录出错！！！")

    """
    ##  获取要回复的主题
    """
    def getTargetPage(self):
        replyPage = None
        if len(self.lastVisited) <= 0:
            #   self.log("此次回复主题：" + self.Menu.pageList[0].pageUrl)
            # 存入
            #   self.visited.append(self.Menu.pageList[0].tid)
            #   直接返回第一个
            replyPage = self.Menu.pageList[0]
        #   遍历列表
        for temp in self.Menu.pageList:
            # 记录中不存在，则存入记录并返回
            if (temp not in self.lastVisited) and (temp not in self.visited):
                #   存入帖子ID
                #   self.visited.append(temp.tid)
                #   self.log("此次回复主题：" + temp.pageUrl)
                replyPage = temp
                break
        self.log("此次回复主题：" + replyPage.pageUrl)
        return replyPage  # 如果都已经回复过了，则直接回复第一个

    """
    ##  获取银币数目
    """
    def getMyYb(self):
        try:
            url = "http://www.93haoshu.com/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu"
            with self.session.get(url=url, headers=self.__getHeader(), timeout=8) as response:
                response.encoding = 'gbk'
                bs_obj = BeautifulSoup(response.text, 'lxml')
                return int(bs_obj.find('span', {'id': 'hcredit_2'}).get_text()[0:-1])
            time.sleep(1)
        except Exception as exception:
            raise Exception("获取银币数目出错！！！")
