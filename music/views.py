from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
#from django.template import loader
#from django.http import Http404
#from django.http import HttpResponse
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.db.models import Q
from .forms import AlbumForm, UserForm,SongForm
from django.views import generic
from django.views.generic import View
from .models import Album ,Song
# Create your views here.
"""class IndexView(generic.ListView):
	template_name='music/index.html'
	context_object_name='all_albums'
	
	def get_queryset(self):
		return Album.objects.all()"""
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']

def index(request):
	if not request.user.is_authenticated():
		return render(request,'music/login.html')
	else:
		all_albums = Album.objects.filter(user=request.user)
		song_result=Song.objects.all()
		query = request.GET.get("q")
		if query:
			all_albums=all_albums.filter(
				Q(album_title__icontains =query)|Q(artist__icontains=query)).distinct()
			song_result=song_result.filter(
				Q(song_title__icontains=query)).distinct()
			return render(request,'music/index.html',{
				'all_albums':all_albums,
				'songs':song_result,
				})
		return render(request,'music/index.html',{'all_albums' : all_albums})

"""class DetailView(generic.DetailView):
	model= Album
	template_name='music/details.html' """

def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/details.html', {'album': album, 'user': user})

#class AlbumCreate(CreateView):
#	model=Album
#	fields=['artist','album_title','genre','logo']

class AlbumUpdate(UpdateView):
	model=Album
	fields=['artist','album_title','genre','logo']

class AlbumDelete(DeleteView):
	model=Album
	#fields=['artist','album_title','genre','logo']
	success_url=reverse_lazy('music:index')

def AlbumCreate(request):
	if not request.user.is_authenticated():
		return render(request,'music/login.html')
	else:
		form = AlbumForm(request.POST or None,request.FILES or None)
		if form.is_valid():
			album=form.save(commit=False)
			album.user = request.user
			album.logo = request.FILES['logo']
			album.save()
			return render(request,'music/details.html',{'album':album})
		context={
				"form":form,
		}
		return render(request,'music/album_form.html',context)

def SongCreate(request,album_id):
    form=SongForm(request.POST or None,request.FILES or None)
    album=get_object_or_404(Album,pk=album_id)
    if form.is_valid():
    	albums_song=album.song_set.all()
    	for k in albums_song:
    		if k.song_title == form.cleaned_data.get("song_title"):
    			context = {
    				'album': album,
    				'form' : form,
    				'error_message': 'You already add that song',
    			}
    			return render(request,'music/add-song.html',context)
    	song=form.save(commit=False)
    	song.album = album
    	song.audio_file=request.FILES['audio_file']
    	file_type=song.audio_file.url.split('.')[-1]
    	file_type=file_type.lower()
    	if file_type not in AUDIO_FILE_TYPES:
    		context={
    			'album': album,
    			'form' : form,
    			'error_message': 'Not supported format',
    		}
    		return render(request,'music/add-song.html',context)
    	song.save()
    	return render(request,'music/details.html',{'album' :album})
    context={
    	'album' : album,
    	'form' : form,
    }
    return render(request,'music/add-song.html',context)

class UserFormView(View):
	form_class= UserForm
	template_name = 'music/registration_form.html'
	#display bank form
	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})
	#process form data
	def post(self,request):
		form=self.form_class(request.POST)
	 	
	 	if form.is_valid():
	 		user=form.save(commit=False)
	 		# cleaned(normalize data)
	 		username=form.cleaned_data['username']
	 		password=form.cleaned_data['password']
	 		user.set_password(password)
	 		user.save()
	 		#return user object if its correct
	 		user = authenticate(username=username,password=password)

	 		if user is not None:
	 			if user.is_active:
	 				login(request,user)
	 				return redirect('music:index')

		return render(request,self.template_name,{'form':form})

def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
	"form":form,
	}
	return render(request,'music/login.html',context)
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username ,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				albums=Album.objects.filter(user=request.user)
				return render(request,'music/index.html',{'albums' : albums})
			else:
				return render(request,'music/login.html',{'error_message' : 'Account disabled'})
		else:
			return render(request,'music/login.html',{'error_message' : 'Invalid login'})
	return render(request,'music/login.html')
def songs(request,filter_by):
	if not request.user.is_authenticated():
		return render(request,'music/login.html')
	else:
		try:
			song_id=[]
			for album in Album.objects.filter(user=request.user):
				for song in album.song_set.all():
					song_id.append(song.pk)
			users_songs=Song.objects.filter(pk__in=song_id)
		except Album.DoesNotExist:
			users_songs=[]
		return render(request,'music/songs.html' ,{'song_list' : users_songs})

def del_song(request,album_id,song_id):
	album =get_object_or_404(Album,pk=album_id)
	song=Song.objects.get(pk=song_id)
	song.delete()
	return render(request,'music/details.html',{'album':album})
"""def index(request):
	#return render(request,"music/temp/Hello.html",{})
	all_albums=Album.objects.all()
	#html=''
#	template=loader.get_template('music/index.html')
	context ={
		'all_albums' : all_albums,
	}
#	return HttpResponse(template.render(context,request))
	return render(request,'music/index.html',context)
	#for album in all_album:
	#	url = '/music/' + str(album.id)+'/'
	#	html+='<a href =" '+url+'"> '+ album.album_title +'</a><br>'
	#return HttpResponse(html)
	#return HttpResponse("<h1>This is music homepage</h1>")
def details(request,album_id):
	try:
		album=Album.objects.get(pk=album_id)
	except Album.DoesNotExist:
		raise Http404("Album DoesNotExist")
	album=get_object_or_404(Album,pk=album_id)
	#return HttpResponse("<h2>Details for Album id is :" + str(album_id) + "</h2>")
	return render(request,'music/details.html',{'album':album})
def favorite(request,album_id):
	album=get_object_or_404(Album,pk=album_id)
	try:
		selected_song=album.song_set.get(pk=request.POST['song'])
	except (KeyError,Song.DoesNotExist):
		return render(request,'music/detail.html',{
			'album':album,
			'error_message':"You did no select valid song",
			})
	else:
		selected_song.is_fav=True
		selected_song.save()
		return render(request,'music/details.html',{'album':album})"""