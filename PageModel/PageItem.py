class PageItem:
    def __init__(self, url, tid, creator, createTime, visitor, visitTime, watchNum):
        self.pageUrl = url
        self.creator = creator
        self.createTime = createTime
        self.num = watchNum
        self.lastVisitor = visitor
        self.lastVisitTime = visitTime
        self.tid = tid


