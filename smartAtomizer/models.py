from django.db import models
from django.db.models import Sum

class Client(models.Model):
	name = models.CharField(max_length = 50)
	contact_name = models.CharField(max_length = 100)
	contact_phone = models.CharField(max_length = 50)
	address = models.CharField(max_length = 150)
	description = models.CharField(max_length = 200)

	def __str__(self):
		return self.name


	def smart_atomizer_client_volume(self):
		zones = Zone.objects.filter(client=self)
		volume = 0
		numberOfAtomizers = 0
		print("num of zones")
		print(len(zones))
		for zone in zones:
			numberOfAtomizers = numberOfAtomizers + zone.count_smart_atomizers()
			if len(SmartAtomizer.objects.filter(zone=zone)) > 0:
				volume = volume + SmartAtomizer.objects.filter(zone=zone).aggregate(Sum('volume'))['volume__sum']

		if len(zones) > 0:
			if volume == 0:
				return 0
			else:
				totalVolume = 100 * numberOfAtomizers
				volumePercent = int((volume/totalVolume)*100)
				return volumePercent
		else:
			return 0


class Zone(models.Model):
	client = models.ForeignKey(Client, related_name = 'z_client', on_delete = models.CASCADE)
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200, blank = True, null = True)

	def __str__(self):
		return self.name

	def count_smart_atomizers(self):
		return SmartAtomizer.objects.filter(zone=self).count()

class SmartAtomizer(models.Model):
	zone = models.ForeignKey(Zone, related_name = 'sa_zone', on_delete = models.SET_NULL, blank = True, null = True)
	serial = models.CharField(max_length = 150)
	state = models.BooleanField(default = False)
	timer_interval = models.CharField(max_length = 5, default = '0.5')
	scheduled_interval = models.CharField(max_length = 200, default = '07:00,23:00')
	atomizer_trigger_time = models.IntegerField(default = 1)
	sync_interval = models.CharField(max_length = 5, default = '0.25')
	log_information = models.IntegerField(default = 255)
	volume = models.IntegerField(default = 0)
	activated = models.BooleanField(default = False)
	latitude = models.DecimalField(default=37.397987, max_digits=10, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(default=-121.983552, max_digits=10, decimal_places=6, blank=True, null=True)

	def __str__(self):
		return self.serial	


class ErrorLog(models.Model):
	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name = 'el_smart_atomizer', on_delete = models.CASCADE)
	log_time = models.DateTimeField(auto_now_add = True)
	zone = models.ForeignKey(Zone, related_name = 'el_zone', blank = True, null = True, on_delete = models.CASCADE)
	client = models.ForeignKey(Client, related_name = 'el_client', blank = True, null = True, on_delete = models.CASCADE)
	stack_trace = models.CharField(max_length = 500)

class MovementLog(models.Model):
	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name = 'ml_smart_atomizer', on_delete = models.CASCADE)
	log_time = models.DateTimeField(auto_now_add = True)

class VolumeLog(models.Model):
	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name = 'vl_smart_atomizer', on_delete = models.CASCADE)
	log_time = models.DateTimeField(auto_now_add = True)
	volume = models.IntegerField()

class SyncLog(models.Model):
	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name = 'sl_smart_atomizer', on_delete = models.CASCADE)
	log_time = models.DateTimeField(auto_now_add = True
)
class AtomizerTriggerLog(models.Model):
	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name = 'atl_smart_atomizer', on_delete = models.CASCADE)
	log_time = models.DateTimeField(auto_now_add = True)
	atomizer_trigger_time = models.IntegerField()
