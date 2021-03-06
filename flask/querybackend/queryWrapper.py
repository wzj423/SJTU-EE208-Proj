import json,os
from querybackend.vip.Search import keywordQueryWrapped as keywordQuery
from querybackend.vip.logo_derive_feature import Search_for_logo as logoQuery
from querybackend.vip.search_for_product import Find_Similiarity as imageQuery
INTERNAL_DIR=os.path.dirname(__file__)

print(INTERNAL_DIR)
itemDatas=None

debugOutput=['6919654910762287749', '6919654911604462238', '6919495701707184450', '6919163322931147603', '6919114716577338309', '6919645140414211153', '6918895347464727070', '6919580789552072467', '6919654911604351646', '6919043337308051038', '6919442009418135426', '6919459526233007630', '6919502526182146882', '6919654742033381007', '6919605733754244037', '6919563717228623443', '6919644914970350534', '6919656195083113414', '6919219774913262914', '6919508309708260367']

def keywordQueryWrapped(keyword):
    if not keyword or keyword=='': return []
    return keywordQuery(keyword)
    return debugOutput

def imageQueryWrapped(image):
    return imageQuery(image)
    return debugOutput 
def logoQueryWrapped(logo):
    return logoQuery(logo)
