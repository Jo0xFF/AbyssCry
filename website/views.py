from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from pytube import YouTube
from wsgiref.util import FileWrapper
import os
import time

def yt_download(yt_obj):
	stream = yt_obj.streams.get_highest_resolution()
	return stream


def yt_title(yt_obj):
	return yt_obj.title

def yt_thumb(yt_obj):
	return yt_obj.thumbnail_url


def getAudio(yt_obj):

	med_bit = 0
	low_bit = 0
	bits = {"low_url": "", "med_url": ""}
	for x in yt_obj.vid_info['streamingData']['adaptiveFormats']:
	    if x.get('audioQuality'):
	        if x.get('mimeType').split(';')[0] == "audio/webm":
	            if x.get('audioQuality') == 'AUDIO_QUALITY_MEDIUM':
	                if x['bitrate'] > med_bit:
	                    med_bit = x['bitrate']
	                    bits['med_url'] = x['url']
	            if x.get('audioQuality') == 'AUDIO_QUALITY_LOW':
	                if x['bitrate'] > low_bit:
	                    low_bit = x['bitrate']
	                    bits['low_url'] = x['url']
	return bits



def vod_del(request):
	print("hello im here")
	file = FileWrapper(open('website/downloads/vod.mp4', 'rb'))
	response = HttpResponse(file, content_type='video/mp4')
	path = os.listdir('website/downloads')[0]
	dir_path = 'website/downloads'
	full_path = os.path.join(dir_path, path)


	response['X-Sendfile'] = path
	response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
	response['Content-Length'] = os.stat(full_path).st_size

	# os.remove('website/downloads/vod.mp4')
	return response
	# return render(request, 'index.html', {})




def home(request):
	context = {}
	if os.path.isfile('website/downloads/vod.mp4'):
		os.remove('website/downloads/vod.mp4')

	print("IM AFTER REMOVED......")
	if request.method == 'POST' and 'social_url' in request.POST.keys():
		# print("im in POST")
		# print(request.POST)
		social_url = request.POST.get('social_url')

		# initial Youtube (pytube) obj
		yt_obj = YouTube(social_url)

		# Get the Vod obj
		vod = yt_download(yt_obj)
		vod.download('website/downloads', filename='vod.mp4')
		

		# get the thumbnail of Vod
		thumbnail = yt_thumb(yt_obj)

		# Get the Audio of Vod
		audio_obj = getAudio(yt_obj)


		
		# context['vod_down'] = response
		context['thumbnail_url'] = thumbnail
		context['low_q'] = audio_obj.get('low_url')
		context['med_q'] = audio_obj.get('med_url')

	elif request.method == 'POST':
		print("The Another POST: ", request.POST)
		print("im in GET")
		return vod_del(request)
		 


	return render(request, 'index.html', context)
