import json
import os
import time
import random
import platform
from PageModel.SectionModel import Section

'''
##  获取要回复的版块
##  出错返回默认值
'''
def getSections():
    results = []
    try:
        with open('Config/sections.json', encoding='utf-8') as file:
            sections = file.read()
            secs = json.loads(sections)
            for temp in secs:
                t = Section(temp['secName'], temp['secUrl'])
                results.append(t)
    except:
        print('未检测到用户板块配置，启用默认设置！！！\n')
        return getSectionsDefault()
    return results


def getSectionsDefault():
    return [
        Section("同人小说", "http://www.93haoshu.com/forum-2-1.html"),
        Section("全本小说", "http://www.93haoshu.com/forum-72-1.html"),
        Section("常规小说", "http://www.93haoshu.com/forum-56-1.html")
    ]


'''
##  获取要回复的内容
##  出错返回默认值
'''
def getMessages():
    results = []
    try:
        with open('Config/replies.txt', encoding='utf-8') as file:
            for line in file.readlines():
                results.append(line.strip('\n'))
    except:
        print('\n未检测到用户回复配置，启用默认设置！！！')
        return getMessagesDefault()
    return results


def getMessagesDefault():
    return [
            "[color=Red]楼主发贴辛苦了，谢谢楼主分享！[/color]我觉得[color=blue]好书友论坛[/color]是注册对了！",
            "楼主太厉害了！楼主，我觉得[color=blue]好书友[/color]真是个好地方！",
            "这个帖子不回对不起自己！我想我是一天也不能离开[color=blue]好书友[/color]。",
            "我看不错噢 谢谢楼主！[color=blue]好书友[/color]越来越好！",
            "论坛不能没有像楼主这样的人才啊！我会一直支持[color=blue]好书友[/color]。",
            "既然你诚信诚意的推荐了，那我就勉为其难的看看吧！[color=blue]好书友[/color]不走平凡路。",
            "感谢楼主分享~",
            "[color=blue]支持一下楼主[/color]",
            "进来看看，支持一下楼主"
        ]

'''
##  在cmd窗口上显示时间
'''
def showOnCmdTitle(username):
    global gTime, day
    _minute = _hour = _second = int(0)
    _second = gTime

    if gTime >= 60:
        _minute = int(gTime / 60)
        _second = gTime % 60

    if _minute >= 60:
        _hour = int(_minute / 60)
        _minute %= 60

    if _hour >= 24:
        day = day + 1
        _hour %= 24
        gTime %= 24 * 60 * 60

    timeFormat = str.format("title 好书友  [{0}]  已运行：{1} 天 {2}:{3}:{4}",
                            username, day.__str__().zfill(2), _hour.__str__().zfill(2),
                            _minute.__str__().zfill(2), _second.__str__().zfill(2))
    os.system(timeFormat)


global gTime, day


def doShowTime(username):
    global gTime, day
    while True:
        showOnCmdTitle(username)
        gTime = gTime + 1
        time.sleep(1)


'''
##  获取一个随机等待时间
'''
def getRandTime(Mode):
    if Mode == 0:
        otime = 30
    elif Mode == 1:
        otime = 170
    elif Mode == 2:
        otime = 140
    ext = random.randint(4, 6)
    return otime + ext


'''
##  获取操作系统信息
'''
def is_os_of(sysname):
    sysname = str.lower(sysname)
    splatform = platform.platform().lower()
    sversion = platform.version().lower()
    if splatform.__contains__(sysname) or sversion.__contains__(sysname):
        return True
    return False
