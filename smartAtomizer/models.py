from django.db import models
from django.db.models import Sum
from datetime import datetime

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

	def smart_atomizer_client_total_volume(self):
		zones = Zone.objects.filter(client=self)
		volume = 0
		numberOfAtomizers = 0
		for zone in zones:
			numberOfAtomizers = numberOfAtomizers + zone.count_smart_atomizers()
			if len(SmartAtomizer.objects.filter(zone=zone)) > 0:
				volume = volume + SmartAtomizer.objects.filter(zone=zone).aggregate(Sum('volume'))['volume__sum']

		return volume



class Zone(models.Model):
	client = models.ForeignKey(Client, related_name = 'z_client', on_delete = models.CASCADE)
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200, blank = True, null = True)

	def __str__(self):
		return self.name

	def count_smart_atomizers(self):
		return SmartAtomizer.objects.filter(zone=self).count()

	def sum_zone_volume(self):
		volume = SmartAtomizer.objects.filter(zone=self).aggregate(Sum('volume'))['volume__sum']
		numberOfAtomizers = SmartAtomizer.objects.filter(zone=self).count()
		if (volume == 0) | (numberOfAtomizers == 0) | (volume == None):
				return 0
		else:
			totalVolume = 100 * numberOfAtomizers
			volumePercent = (volume/totalVolume)*100
			return volumePercent

	def sum_zone_total_volume(self):
		volume = SmartAtomizer.objects.filter(zone=self).aggregate(Sum('volume'))['volume__sum']
		numberOfAtomizers = SmartAtomizer.objects.filter(zone=self).count()
		if (volume == 0) | (numberOfAtomizers == 0) | (volume == None):
				return 0
		else:
			return volume

class SmartAtomizer(models.Model):
	zone = models.ForeignKey(Zone, related_name = 'sa_zone', on_delete = models.SET_NULL, blank = True, null = True)
	serial = models.CharField(max_length = 150)
	state = models.BooleanField(default = False)
	sync_interval = models.CharField(max_length = 5, default = '0.04')
	volume = models.IntegerField(default = 0)
	activated = models.BooleanField(default = False)
	latitude = models.DecimalField(default=37.397987, max_digits=10, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(default=-121.983552, max_digits=10, decimal_places=6, blank=True, null=True)

	def __str__(self):
		return self.serial	

class SmartAtomizerSchedule(models.Model):
	VERY_LOW = 'Muy Bajo'
	LOW = 'Bajo'
	MEDIUM = 'Medio'
	HIGH = 'Alto'
	VERY_HIGH = 'Muy Alto'
	ATOMIZER_POWER = (
		(VERY_LOW, VERY_LOW),
		(LOW, LOW),
		(MEDIUM, MEDIUM),
		(HIGH, HIGH),
		(VERY_HIGH, VERY_HIGH)
	)

	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name='sa_schedule', on_delete = models.CASCADE)
	scheduled_start = models.TimeField(default='07:00')
	scheduled_finish = models.TimeField(default='12:00')
	atomizer_power = models.CharField(max_length=10,choices=ATOMIZER_POWER, default=LOW)

class Alert(models.Model):
	smart_atomizer = models.OneToOneField(SmartAtomizer, on_delete = models.CASCADE, primary_key=True)
	volume_warning = models.IntegerField(default = 45)
	sync_time_warning = models.CharField(max_length = 5, default = '0.25')

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
	comment = models.CharField(max_length=100, default='')
	log_time = models.DateTimeField(auto_now_add = True)

class AtomizerTriggerLog(models.Model):
	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name = 'atl_smart_atomizer', on_delete = models.CASCADE)
	log_time = models.DateTimeField(auto_now_add = True)
	atomizer_trigger_time = models.IntegerField()

class Representative(models.Model):
	first_name = models.TextField(max_length=50)
	last_name = models.TextField(max_length=50)

	def __str__(self):
		return self.first_name + " " + self.last_name	


class CheckUp(models.Model):
	client = models.ForeignKey(Client, related_name = 'cu_client', on_delete = models.CASCADE)
	representative = models.ForeignKey(Representative, related_name = 'cu_representative', on_delete = models.SET_NULL, blank = True, null = True)
	day = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	notes = models.TextField(max_length=250, blank=True, null=True)
	
	def __str__(self):
		return self.client.name + " - " + self.day.strftime('%Y-%m-%d')

	# def clean(self):
	# 	if self.end_time <= self.start_time:
	# 		raise ValidationError('Ending times must after starting times')

		# events = CheckUp.objects.filter(day=self.day).filter(client=self.client)
		# if events.exists():
		# 	for event in events:
		# 		if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
		# 			raise ValidationError('There is an overlap with another event: ' + str(event.day) + ', ' + str(event.start_time) + '-' + str(event.end_time))

class Report(models.Model):
	checkup = models.OneToOneField(CheckUp, on_delete = models.CASCADE, primary_key=True)
	visit_completed = models.BooleanField(default=False)
	log_time = models.DateTimeField(auto_now_add = True)
	notes = models.TextField(max_length=250, blank=True, null=True)



