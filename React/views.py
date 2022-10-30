from copyreg import pickle
from json import dump, dumps
from operator import is_, truediv
# from tkinter import image_names
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
from React.models import Rating, Users, Wallpaper
from React.serializers import UserSerializer, WallpaperSerializer
from django.http import request
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import login, authenticate
from django.core import serializers
from django.core.paginator import Paginator
import sys
import os
sys.path.append('..')
sys.path.append('../wrec')
from wrec import api
import json
import React.db
serializer_class = UserSerializer
queryset = Users.objects.all()

@api_view(['POST'])
def log_in(request):
    username = request.data.get('username')
    password = request.data.get('password')

    res = {
            'code': 1,
            'msg': '',
            'data': {}
        }
    
    if not all([username, password]):
        res['msg'] = '参数异常。'
        return Response(res)
    print(request.data)
    try:
        Users.objects.get(username=username, password=password)
    except:
        res['msg'] = 'Wrong Username or Password!'
        return Response(res)

    res['msg'] = 'Login Successful!'
    res['code'] = 0
    res['data'] = {'username': username}
    return Response(res)

@api_view(['POST'])
def register(request):
        password = request.data.get('password')
        username = request.data.get('username')
        res = {
            'code': 0,
            'msg': '',
            'data': {}
        }

        if not all([password, username]):
            res['msg'] = '参数异常。'
            return Response(res)

        print([password, username])
        if Users.objects.filter(username=username):
            res['msg'] = 'This username is already exist!'
            return Response(res)

        Users.objects.create(password=password, username=username)
        res['code'] = 1
        res['data'] = {'username': username}
        return Response(res)

@api_view(['POST'])
def recommend(request):
    username = request.data.get('username')
    if not username:
        return HttpResponse('?')
    rating_dict = React.db.getRatingItem(username)
    rating_dict = rating_dict[username]
    cf = api.rec_init()
    rec = cf.recommend(45, rating_dict, True)
    outputs = []
    for item in rec:
        img_src = convertImage(item)
        itemInfo = React.db.getItemInfo(item)
        itemInfo.update({'img_src': img_src})
        # outputs[itemInfo['img_name']] = itemInfo
        outputs.append(itemInfo)

    # outputs = json.dumps(outputs)
    return Response(outputs)

@api_view(['POST','GET'])
def paging(request):
    object_list = Wallpaper.objects.all()
    serializers = WallpaperSerializer(object_list, many = True)
    photos = serializers.data
     # 获取所有的img
    # paginator = Paginator(object_list, 15)
    #   #每页的数目为15个
    # page = request.GET.get('page',1)
    # #   #得到第几页
    # limit = request.GET.get('limit',15)
    # all_count = outputs.Article.objects.all()
    # posts = paginator.page(page)
      #正常显示第几页
    # return render(request, 'index.html', {'page': page, 'posts': posts})
    return Response(photos)
      #将数据传入那个网页

def convertImage(imagename, img_dir='wrec\imgs'):
    img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, img_dir, imagename)
    with open(img_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream

@api_view (["POST"])
def search(request):
    tag_name = request.data.get("tag_name")
    item_list = React.db.search(tag_name)
    if not item_list:
        return Response([])
    outputs = []

    for item in item_list:
        imgname = item['img_name']
        itemInfo = React.db.getItemInfo(imgname)
        img_src = convertImage(itemInfo['img_name'])
        itemInfo.update({'img_src': img_src})
        outputs.append(itemInfo)
    return Response(outputs)

@api_view (["POST"])
def getItemRatingDetail(request):
    user = request.data.get("username")
    item_name = request.data.get("image_name")
    status = React.db.getItemRatingDetail(user, item_name)
    # status = json.dumps(status)
    return Response([status])

@api_view (["POST"])
def like(request):
    user = request.data.get("username")
    image = request.data.get('image_name')
    rating = request.data.get("like")
    status = React.db.like(user, image, rating)
    return Response([status])

@api_view (["POST"])
def favorite(request):
    user = request.data.get("username")
    image = request.data.get('image_name')
    rating = request.data.get("collect")
    status = React.db.favorite(user, image, rating)
    return Response([status])


@api_view (["POST"])
def getFavorite(request):
    user = request.data.get("username")
    favorited_list = React.db.getFavorites(user)
    for item in favorited_list:
        img_src = convertImage(item['img_name'])
        item.update({'img_src': img_src})
    return Response(favorited_list)



# @api_view(['POST','GET'])
# def search(request):
#     serializer_class = UserSerializer
#     q = request.data.get('username')
#     error_msg = ''
#     if not q:
#         error_msg = 'please input a tag name'
#         return Response(error_msg)
#     # search_list = serializers.serialize("json", Users.objects.filter(username__icontains = q))
#     search_list1 = Users.objects.filter(username__icontains = q)
#     serializers1 = UserSerializer(search_list1, many = True)

#     search_list2 = Users.objects.filter(password__icontains = q)
#     serializers2 = UserSerializer(search_list2, many = True)

#     serializers = serializers1.data+serializers2.data
#     return Response(serializers)
 



