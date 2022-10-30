import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAPI.settings")
import sys
sys.path.append('./wrec')
import django

django.setup()

def makeItemTable():
    from React.models import Wallpaper
    label_list = []
    with open('./wrec/filelist/filelist.csv', 'r') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            line = line.strip().split(',')
            imgNAME = line[0]
            imgSRC = line[1]
            imgTAGS = ','.join(line[2:])
            label_list.append(Wallpaper(imgId=idx, imagNAME=imgNAME, imagSRC=imgSRC, imagTAGS=imgTAGS))
    Wallpaper.objects.bulk_create(label_list)
    
makeItemTable()