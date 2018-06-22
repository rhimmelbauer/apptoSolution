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
	sync_interval = models.CharField(max_length = 5, default = '7')
	volume = models.DecimalField(default = 0, max_digits=8, decimal_places=4)
	activated = models.BooleanField(default = False)
	latitude = models.DecimalField(default=37.397987, max_digits=10, decimal_places=6, blank=True, null=True)
	longitude = models.DecimalField(default=-121.983552, max_digits=10, decimal_places=6, blank=True, null=True)
	version = models.CharField(max_length=8, default='00.00.00')

	def __str__(self):
		return self.serial	

class SmartAtomizerSchedule(models.Model):
	NIVEL_1 = 'N1: 120s, 90s'
	NIVEL_2 = 'N2: 120s, 120s'
	NIVEL_3 = 'N3: 90s, 120s'
	NIVEL_4 = 'N4: 60s, 120s'
	NIVEL_5 = 'N5: 90s, 210s'
	NIVEL_6 = 'N6: 100s, 300s'
	NIVEL_7 = 'N7: 60s, 300s'
	NIVEL_8 = 'N8: 30s, 300s'
	NIVEL_9 = 'N9: 10s, 300s'
	ATOMIZER_POWER = (
		(NIVEL_1, NIVEL_1),
		(NIVEL_2, NIVEL_2),
		(NIVEL_3, NIVEL_3),
		(NIVEL_4, NIVEL_4),
		(NIVEL_5, NIVEL_5),
		(NIVEL_6, NIVEL_6),
		(NIVEL_7, NIVEL_7),
		(NIVEL_8, NIVEL_8),
		(NIVEL_9, NIVEL_9),
	)

	smart_atomizer = models.ForeignKey(SmartAtomizer, related_name='sa_schedule', on_delete = models.CASCADE)
	scheduled_start = models.CharField(default='07:00', max_length=5)
	scheduled_finish = models.CharField(default='12:00', max_length=5)
	atomizer_power = models.CharField(max_length=15, choices=ATOMIZER_POWER, default=NIVEL_3)

	def __str__(self):
		return '%d' % self.pk

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
	volume = models.DecimalField(default = 0, max_digits=8, decimal_places=4)

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



