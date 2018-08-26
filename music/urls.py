from django.conf.urls import url
from . import views
app_name  = 'music'
urlpatterns=[
	#/music/
#	url(r'^$',views.IndexView.as_view(),name ='index'),
	url(r'^$',views.index,name ='index'),

    url(r'^login_user/$', views.login_user, name='login_user'),
	url(r'^register/$',views.UserFormView.as_view(),name ='register'),
	url(r'^logout_user/$', views.logout_user, name='logout_user'),
	#music/album_id/
	#url(r'^(?P<album_id>[0-9]+)/$', views.details, name='details'),
	#music/album_id/favorite
	#url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),	
	url(r'^(?P<album_id>[0-9]+)/add-song/$',views.SongCreate,name='add-song'),
	url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='details'),
	
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
	#music/album/add/
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.del_song, name='delete_song'),
	url(r'album/add/$',views.AlbumCreate,name='album-add'),
	#music/album/2//
	url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'),
	#music/album/2/delete/
	url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),
]
