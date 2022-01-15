from collections import Counter
from itertools import count

def resultsCounter(results):
    '''
    results should be a list of tuples, each tuple containing
     a string(productId) and a dict (detailized infomation)
    return (brands,categories,mostFrequentAttrs(top5),attrDict)
    '''
    attrs=[]
    brands=[]
    categories=[]
    attrDict=dict()
    for pid,detail in results:
        if detail['brandShowName'] not in brands:
            brands.append(detail['brandShowName'])
        if detail['category'] not in categories:
            categories.append(detail['category'])
        for _d in detail['attrs']:
            name=_d['name']
            value=_d['value']
            attrs.append(name)
            if name not in attrDict :attrDict[name]=[]
            if value not in attrDict[name]: attrDict[name].append(value)

    counter=Counter(attrs)
    most_occur=[x[0] for x in counter.most_common(5)]
    return (brands,categories,most_occur,attrDict)

