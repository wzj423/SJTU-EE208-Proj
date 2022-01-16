import json,os
from sys import builtin_module_names
INTERNAL_DIR=os.path.dirname(__file__)

print(INTERNAL_DIR)
itemDatas=None

def getCategory(filename):
    builtin_category=("衣服","鞋","裤","袜","帽")
    for cate in builtin_category:
        if filename.find(cate)!=-1:
            return cate
    if filename.find('服')!=-1: return "衣服 "

def commentSatisFactor(item):
    satisScore={'VERY_SATISFIED':2.5,'SATISFIED':1,'DISSATISFIED':-3,'VERY_DISSATISFIED':-8,'GENERAL':0.5}
    tot=len(item[1]['comments'])
    score=0
    if tot==0 : return 2.5
    for comment in item[1]['comments']:
        score+=comment['nlpScore']*satisScore[comment['satisfiedStatus']]
        tot+=comment['nlpScore']
    score/=tot
    score+=2.5
    if score<0 :score=0
    return score


def loadDatabase() :
    #templist=[]
    global itemDatas
    for dirpath, dirnames, filenames in os.walk(INTERNAL_DIR):
        for filename in filenames:
            if not filename.endswith('.json'): continue
            with open(os.path.join(INTERNAL_DIR, filename),encoding='utf-8') as f:
                json_file=json.load(f)
            cate=getCategory(filename)
            for item in json_file.items():
                item[1]['category']=cate
                item[1]['url']=f"https://detail.vip.com/detail-{item[1]['brandId']}-{item[1]['productId']}.html"
                item[1]['commentScore']=commentSatisFactor(item)
                #if len(templist)<20: templist.append(item[0]) 
            itemDatas={**json_file,**(itemDatas if itemDatas else dict())}
    #print(templist)

loadDatabase()
def queryItems(itemList):
    itemDetails=[]
    for itemId in itemList:
        if itemId in itemDatas:
            itemDetails.append((itemId,itemDatas[itemId]))
    return itemDetails

def filterItems(itemDetails,brands,cates,attrs):
    def attr2set(attr):
        t=attr
        ret=set(t.split(','))
        return ret
    def isSubAttr(subattr,attr):
        subset=attr2set(subattr)
        aset=attr2set(attr)
        return subset.issubset(aset)

    filteredItemDetails=[]
    for pid,detail in itemDetails:
        if brands and detail['brandShowName'] not in brands: continue
        if cates and detail['category'] not in cates: continue
        legal=True
        if attrs:#默认无
            for attr,value in attrs.items():
                if value=='all':continue#无要求
                for _d in detail['attrs']:
                    if attr in _d['name'] and not isSubAttr(value,_d['value']):
                        legal=False
                        break
        if legal: filteredItemDetails.append((pid,detail))
        pass
    return filteredItemDetails



def sortItems(itemDetails,sortway):
    if not sortway or sortway=='similarity': return itemDetails
    ret=itemDetails
    if sortway=='priceup':
        ret.sort(key=lambda x:str(x[1]['vipshopPrice']))
    elif sortway=='pricedown':
        ret.sort(key=lambda x:str(x[1]['vipshopPrice']) ,reverse=True)
    elif sortway=='comment':
        ret.sort(key=lambda x:x[1]['commentScore'] ,reverse=True)
    return ret