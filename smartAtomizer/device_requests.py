from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from datetime import datetime
from .forms import *
from .models import *

def test_volume_log(request, pk, volume):
	print("logging volume")
	print(volume)
	smartAtomizer = get_object_or_404(SmartAtomizer, pk=pk)
	smartAtomizer.volume = volume
	print(smartAtomizer.volume)
	smartAtomizer.save()
	volumeLog = VolumeLog()
	volumeLog.smart_atomizer = smartAtomizer
	volumeLog.log_time = datetime.now()
	volumeLog.volume = volume
	volumeLog.save()
	response = JsonResponse({'smart_atomizer': 'testing callback'})
	return response

def test_activation(request, serial):
	try:
		smartAtomizerDevice = SmartAtomizer.objects.filter(serial=serial)
		print("Found Device")
		smartAtomizerDB = SmartAtomizer.objects.get(serial=serial)


		syncLog = SyncLog()
		syncLog.smart_atomizer = smartAtomizerDB
		syncLog.comment = "Device Synced Correctly"
		syncLog.save();
		data = serializers.serialize('json', [smartAtomizerDB,])

		return HttpResponse(data, content_type="application/json")
	except SmartAtomizer.DoesNotExist:
		print("Entered Create Device")
		smartAtomizerDevice = SmartAtomizer()
		smartAtomizerDevice.serial = serial
		smartAtomizerDevice.save()
		alert = Alert()
		alert.smart_atomizer = smartAtomizerDevice
		alert.save()

		syncLog = SyncLog()
		syncLog.smart_atomizer = smartAtomizerDevice
		syncLog.comment = "Enrolled new Device"
		syncLog.save();
		data = serializers.serialize('json', [smartAtomizerDevice,])
		return HttpResponse(data, content_type="application/json")


