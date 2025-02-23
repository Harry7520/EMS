"""EMS_HR_PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include,re_path
from EMS_HR.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', to_login),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('ems/', include('EMS_HR.urls')),
    re_path(r'^.*/$', custom_404_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
