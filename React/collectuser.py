
import os
import sys
sys.path.append('../')
sys.path.append('../wrec')
from wrec import api
import pickle
from .models import Users

rating_dict = api.getUserRating('user1', api.test_input['table'])
def niu(user):
    
    targetuser = Users.obejects.filter(username = user)
    retval = os.getcwd()
    cf = api.rec_init(os.path.join(retval, './objects'), os.path.join(retval, './filelist/filelist.csv'), os.path.join(retval, './imgs'), os.path.join(retval, './features/features.json'))
    output = cf.recommend(top=20, rating_dict=rating_dict, shuffle=True)
    return output