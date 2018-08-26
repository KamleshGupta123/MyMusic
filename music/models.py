# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse
class Album(models.Model):
	user = models.ForeignKey(User, default=1)
	artist=models.CharField(max_length=250)
	album_title=models.CharField(max_length=250)
	genre=models.CharField(max_length=250)
	logo=models.FileField()
	
	def get_absolute_url(self):
		return reverse('music:details',kwargs={'pk': self.pk})

	def __str__(self):
		return self.album_title + ' - '	+ self.artist

class Song(models.Model):
	album=models.ForeignKey(Album,on_delete=models.CASCADE)
	#file_type=models.CharField(max_length=250)
	song_title=models.CharField(max_length=250)
	audio_file=models.FileField(default='')
	#is_fav=models.BooleanField(default=False)
	def __str__(self):
		return self.song_title
