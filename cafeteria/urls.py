
from django.contrib import admin
from django.urls import path, include
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

'''if we make url.py in the app
   then we dont need to write path('',views.SignupPage,name='signup')
   we can simply use from .views import * 
   and write path('',SignupPage,name='signup'),
'''
urlpatterns = [
    path('admin/', admin.site.urls),

    path("", include("app1.urls")),
    #path('',views.SignupPage,name='signup'),
    path('',views.index),
    path('login/',views.LoginPage,name='login'),
    path('signup/',views.SignupPage,name='signup'),
    path('logout/',views.LogoutPage,name='logout'),
    
    path('index/',views.index, name='index'),
    path('items/',views.items,name='items'),
    path('popular/',views.popular,name='popular'),
    path('category/',views.categorylist,name='category'),



    path('home/',views.HomePage,name='home'),
    path('token/',views.token_send,name='token_send'),
    path('success/',views.success,name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),

    path("ckeditor/",include("ckeditor_uploader.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)