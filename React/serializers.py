from rest_framework.serializers import ModelSerializer
from React.models import Users, Wallpaper

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class WallpaperSerializer(ModelSerializer):
    class Meta:
        model = Wallpaper
        fields = '__all__'