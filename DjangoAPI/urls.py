
import imp
from django.contrib import admin
from django.urls import path, include
from React import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('React.urls')),
]
