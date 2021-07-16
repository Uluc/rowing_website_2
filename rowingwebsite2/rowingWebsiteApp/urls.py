from django.urls import path
from . import views
from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='website-home'),
    path('roster/', views.roster, name='website-roster'),
    path('schedule/', views.schedule, name='website-schedule'),
    path('sponsor/', views.sponsor, name='website-sponsor'),
    path('recruitment/', views.recruitment, name='website-recruitment'),
    path('leadership/', views.leadership, name='website-leadership'),
    path('photogallery/', views.photogallery, name='website-photogallery'),
    path('aboutus/',views.aboutus, name='website-aboutus'),
    path('confirmed/', views.confirmed, name='website-confirmed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)