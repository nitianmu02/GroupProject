import django
import os
import json
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAPI.settings")
django.setup()
from React.models import Wallpaper, Users, Rating, Favorite


def getRandomItem(num):
    return [i.imagNAME for i in Wallpaper.objects.all().order_by('?')[:num]]

def getItemInfo(imgNAME):
    item_dict = {}
    searched_item = Wallpaper.objects.get(imagNAME = imgNAME)
    item_dict = {
        'img_name': searched_item.imagNAME,
        'src': searched_item.imagSRC,
        'img_tag': searched_item.imagTAGS,
    }
    # item_dict = json.dumps(item_dict)
    return item_dict

def signIn(Usr, Pwd):
    if not Usr:
        return {'code':0, 'msg': 'User name should not be empty!'}
    ifUserExists = len(Users.objects.filter(username = Usr)) 
    if not ifUserExists:
        return {'code':1, 'msg': 'User not exists!'}
    stat = 1 if Users.objects.get(username=Usr, password=Pwd) else 0
    if not stat:
        return {'code': stat, 'msg': 'pwd incorrect!'}
    return {'code': stat, 'msg': 'Success!'}

def signUp(Usr, Pwd):
    ifUserExists = len(Users.objects.filter(username = Usr)) 
    if ifUserExists:
        return {'code':0, 'msg': 'User exists!'}
    if not Usr:
        return {'code':0, 'msg': 'User name should not be empty!'}
    Users.objects.create(username=Usr, password=Pwd)
    return {'code': 1, 'msg': 'Success!'}

def like(userName, itemName, signal):
    ifUserExists = len(Users.objects.filter(username = userName)) 
    if not ifUserExists:
        return {'code':0, 'msg': 'User not exists!'}
    Rating.objects.get_or_create(username = userName, imagNAME = itemName)
    rating = Rating.objects.get(username = userName, imagNAME = itemName)
    if rating.like == signal:
        return {'code':0, 'msg': 'User has already liked or disliked this'}
    rating.like = signal
    if signal == True:
        rating.rating += 1
    elif signal == False:
        rating.rating -= 1
    rating.save()
    return {'code':1, 'msg': 'Success!'}

def favorite(userName, itemName, signal):
    ifUserExists = len(Users.objects.filter(username = userName)) 
    if not ifUserExists:
        return {'code':0, 'msg': 'User not exists!'}
    Rating.objects.get_or_create(username = userName, imagNAME = itemName)
    rating = Rating.objects.get(username = userName, imagNAME = itemName)
    if rating.fav == signal:
        return {'code':0, 'msg': 'User has already favorited or disfavorited this'}
    rating.fav = signal
    if signal == True:
        rating.rating += 1
    elif signal == False:
        rating.rating -= 1
    rating.save()
    stat = Favorite.objects.get_or_create(username = userName, imagname = itemName)
    if not stat[1]:
        Favorite.objects.get(username = userName, imagname = itemName).delete()
    return {'code':1, 'msg': 'Success!'}
    
def getRatingItem(userNAME):
    ifUserExists = len(Users.objects.filter(username = userNAME)) 
    if not ifUserExists:
        return {'code':0, 'msg': 'User not exists!'}
    rating_dict = {}
    ifRatingExists = len(Rating.objects.filter(username = userNAME))
    if not ifRatingExists:
        filter = getRandomItem(15)
        for img in filter:
            rating_dict[img] = 1
    else:
        filter = Rating.objects.filter(username = userNAME)
        for u_r in filter:
            rating_dict[u_r.imagNAME] = u_r.rating
            
    user_rating_dict = {userNAME: rating_dict}
    return user_rating_dict

def getItemRatingDetail(user, itemName):
    itemDetail = getItemInfo(itemName)
    itemDetail['liked'] = False
    itemDetail['favorited'] = False
    if not user:
        return itemDetail
    ifItemHasRate = len(Rating.objects.filter(username=user, imagNAME = itemName))
    if ifItemHasRate:
        liked = Rating.objects.get(username=user, imagNAME = itemName).like
        favorited = Rating.objects.get(username=user, imagNAME = itemName).fav
        itemDetail['liked'] = liked
        itemDetail['favorited'] = favorited
    elif not ifItemHasRate:
        Rating.objects.create(username=user, imagNAME = itemName)
        itemDetail['liked'] = False
        itemDetail['favorited'] = False

    return itemDetail

def search(label):
    search_query = Wallpaper.objects.filter(imagTAGS__icontains = label)
    if len(search_query) == 0:
        return None
    if not label:
        return None
    imgname_list = []
    for item in search_query:
        img_name = item.imagNAME
        imgname_list.append(getItemInfo(img_name))
    return imgname_list

def getFavorites(username):
    search_query = Favorite.objects.filter(username = username)
    favorited_list = []
    for item in search_query:
        favorited_list.append(getItemInfo(item.imagname))
    return favorited_list

# print(signUp('user1', '111'))
# print(getRatingItem('user3'))
# print(getItemRatingDetail('user1', 'wallhaven-01y1ew.jpg'))
# print(like('user1', 'wallhaven-01y1ew.jpg', True))
# print(favorite('user1', 'wallhaven-01y1ew.jpg', True))
# print(search('tree'))