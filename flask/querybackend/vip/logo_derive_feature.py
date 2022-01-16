from array import array
import cv2
import numpy as np
import os
MAX_PHOTO_NUM=14
INTERNAL_DIR=os.path.dirname(__file__)
BRAND=["安踏","特步","阿迪达斯","李宁","匹克","鸿星尔克","耐克"]
def Search_for_logo(Search_photo):
    sift=cv2.xfeatures2d.SIFT_create()
    img=Search_photo
    img=cv2.GaussianBlur(img,ksize=(3,3),sigmaX=0)
    _,feature_search=sift.detectAndCompute(img,None)
    final=dict()
    for i in range(MAX_PHOTO_NUM):
        img=cv2.imread(os.path.join(INTERNAL_DIR,'./logoset/%d.jpg'%(i+1)),cv2.IMREAD_COLOR)
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img=cv2.GaussianBlur(img,ksize=(3,3),sigmaX=0)
        _,des=sift.detectAndCompute(img,None)
        match=cv2.BFMatcher()
        result=match.knnMatch(des,feature_search,k=2)
        count=0
        for a,b in result:
            if a.distance<0.8*b.distance:
                count+=1
        final[i]=count
    print(final)
    final=sorted(final.items(),key=lambda x:(x[1],x[0]),reverse=True)
    print(BRAND[final[0][0]%7])
    return BRAND[final[0][0]%7]

if __name__=="__main__":
    img=cv2.imread("test.jpg",cv2.IMREAD_COLOR)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    Search_for_logo(img)
    