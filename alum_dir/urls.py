from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),    
    # url(r'^(?P<alum_id>[0-100]+)/$', views.detail, name='detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/?$', views.search, name='search_view'),
    url(r'^profiles/$', views.user_profile, name='user_profile'),
]