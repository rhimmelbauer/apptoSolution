from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from datetime import datetime
from pytz import timezone
from .forms import *
from .models import *
from django.forms.models import model_to_dict
import requests, json


ENROLLED_NEW_DEVICE = "Enrolled new Device"
DEVICE_SYNC_OK = "Device Synced Correctly"

def ping_home(request, pk):
	print("Ping home")
	response = JsonResponse({'smart_atomizer': 'OK'})
	return response
	

def test_volume_log(request, pk, volume):
	print("logging volume")
	smartAtomizer = get_object_or_404(SmartAtomizer, pk=pk)
	smartAtomizer.volume = volume
	smartAtomizer.save()

	volumeLog = VolumeLog()
	volumeLog.smart_atomizer = smartAtomizer
	volumeLog.log_time = datetime.now().astimezone(timezone('America/Mexico_City'))
	volumeLog.volume = volume
	volumeLog.save()

	response = JsonResponse({'smart_atomizer': 'OK'})
	return response

def set_location(request, pk, lat, lng):
	print("Setting Location")
	smartAtomizer = get_object_or_404(SmartAtomizer, pk=pk)
	smartAtomizer.latitude = lat
	smartAtomizer.longitude = lng
	smartAtomizer.save()

	response = JsonResponse({'smart_atomizer': 'OK'})
	return response
	
def get_location(request, pk, cid, lac, mcc, mnc):
	smartAtomizer = get_object_or_404(SmartAtomizer, pk=pk)
	payload = {'considerIp':'false','cellTowers':[{'cellId': cid,'locationAreaCode': lac,'mobileCountryCode': mcc,'mobileNetworkCode':mnc}]}
	jsonPayload = json.dumps(payload)
	headers = {'content-type': 'application/json'}
	privateKey = "AIzaSyC_p5U3kzT2N1N2UCHu80h54eXLJqa34Mg"
	url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + privateKey
	r = requests.post(url,data=jsonPayload,headers = headers)
	response = JsonResponse({'smart_atomizer': r.text})
	return response
	response = json.loads(r.text)
	lat = response['location']['lat']
	lng = response['location']['lng']
	#smartAtomizer.latitude = lat
	#smartAtomizer.longitude = lng
	#smartAtomizer.save()

	response = JsonResponse({'smart_atomizer': 'OK'})
	return response

def test_activation(request, serial):
	try:
		smartAtomizerDevice = SmartAtomizer.objects.filter(serial=serial)
		print("Found Device")
		smartAtomizerDB = SmartAtomizer.objects.get(serial=serial)

		log_sync(smartAtomizerDB, DEVICE_SYNC_OK)

		data = serializers.serialize('json', [smartAtomizerDB,])

		return HttpResponse(data, content_type="application/json")
	except SmartAtomizer.DoesNotExist:
		print("Entered Create Device")
		smartAtomizerDevice = SmartAtomizer()
		smartAtomizerDevice.serial = serial
		smartAtomizerDevice.save()
		
		init_alerts(smartAtomizerDevice)

		log_sync(smartAtomizerDevice, ENROLLED_NEW_DEVICE)

		init_schedule(smartAtomizerDevice)

		data = serializers.serialize('json', [smartAtomizerDevice,])
		return HttpResponse(data, content_type="application/json")

def init_alerts(smartAtomizer):
	alert = Alert()
	alert.smart_atomizer = smartAtomizer
	alert.save()

def init_schedule(smartAtomizer):
	smartAtomizerSchedule = SmartAtomizerSchedule()
	smartAtomizerSchedule.smart_atomizer = smartAtomizer
	smartAtomizerSchedule.save()

def log_sync(smartAtomizer, msg):
	syncLog = SyncLog()
	syncLog.smart_atomizer = smartAtomizer
	syncLog.comment = msg
	syncLog.log_time = datetime.now().astimezone(timezone('America/Mexico_City'))
	syncLog.save();

def get_schedule(request, pk):
	print("Getting Schedule Count")
	smartAtomizer = get_object_or_404(SmartAtomizer, pk=pk)
	scheduleIDs = SmartAtomizerSchedule.objects.filter(smart_atomizer=smartAtomizer)
	
	data = serialize_querySet(scheduleIDs)
	
	return HttpResponse(data, content_type="application/json")

def serialize_querySet(querySet):
	data = "["
	for item in querySet:
		temp = serializers.serialize('json', [item,])
		temp = temp.replace("[", "")
		temp = temp.replace("]","")
		data += temp
		data += ","

	data = data[:-1]
	data += "]"
	return data



