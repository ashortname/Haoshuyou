import json
from PageModel.SectionModel import Section


def getSections():
    results = []
    with open('Config/sections.json', encoding='utf-8') as file:
        sections = file.read()
        secs = json.loads(sections)
        for temp in secs:
            t = Section(temp['secName'], temp['secUrl'])
            results.append(t)
    return results

def getMessages():
    results = []
    with open('Config/replies.txt', encoding='utf-8') as file:
        for line in file.readlines():
            results.append(line.strip('\n'))
    return results