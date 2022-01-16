from array import array
from io import BytesIO
from re import search
import cv2
from PIL import Image
import numpy as np
import urllib.request
import requests
import json
import torchvision
import torch.nn.functional as func
import torchvision.transforms as transforms
import os
import torch
DATA_NUM=1
INTERNAL_DIR=os.path.dirname(__file__)
modelAlex=torchvision.models.alexnet(pretrained=True)

transform=transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

Data=list()
for root, dirnames, filenames in os.walk(INTERNAL_DIR):
    for filename in filenames :
        if filename.endswith('.json') and not filename.startswith('.'):
            with open(os.path.join(INTERNAL_DIR, filename),'r',encoding='utf8') as data_json:
                Data+=json.load(data_json)
'''
for i in range(DATA_NUM):
    #open内为json_data保存路径，格式见内
    with open(os.path.join(INTERNAL_DIR, "data%d.json"%i),'r',encoding='utf8') as data_json:
        Data+=json.load(data_json)
'''

def feature_model(img):
    img=transform(img)
    img=torch.unsqueeze(img,0)
    img_feature=modelAlex.features(img).detach().numpy()
    img_feature=np.squeeze(img_feature)
    img_feature=np.ravel(img_feature)
    img_feature/=np.linalg.norm(img_feature)
    return img_feature

def similarity(a,b):
    return np.dot(a,b)

def Find_Similiarity(search_img,data=Data):
    feature_img=list()
    feature_search=feature_model(search_img)
    sort_list=list()
    print("Start to compare")
    count=0
    if not os.path.exists(os.path.join(INTERNAL_DIR,"features_of_product_all.npy")):
        for item in data:
            count+=1
            img_src=item["squareImage"]
            response=requests.get(img_src)
            img=Image.open(BytesIO(response.content))
            #print(img.size[0],img.size[1])
            print("save process:%d/%d"%(count,len(data)))
            feature_img.append([feature_model(img),item["productId"]])
        np.save(os.path.join(INTERNAL_DIR,f"./features_of_product_all.npy"),feature_img)
        return None
    else:
        feature_img=np.load(os.path.join(INTERNAL_DIR,f"./features_of_product_all.npy"),allow_pickle=True)
        for feature in feature_img:
            sort_list.append((similarity(feature[0],feature_search),feature[1]))
        print("compare finished")
        sort_list=sorted(sort_list,key=lambda tup:tup[0],reverse=True)
        id_final=list()
        for i in range(min(len(sort_list,400))):
            id_final.append(sort_list[i][1])
        print(id_final[0:10])
        return id_final
    

if __name__=="__main__":
    '''
    Data=list()
    for i in range(DATA_NUM):
        with open("./data%d.json"%i,'r',encoding='utf8') as data_json:
            Data+=json.load(data_json)
    '''
    search_img=Image.open(os.path.join(INTERNAL_DIR, "test.jpg"))
    Find_Similiarity(search_img,Data)
    