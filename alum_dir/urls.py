from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),        
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/?$', views.search, name='search_view'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
]