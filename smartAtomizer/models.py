from django.db import models

class Client(models.Model):
	name = models.CharField(max_length = 50)
	contact_name = models.CharField(max_length = 100)
	contact_phone = models.CharField(max_length = 50)
	address = models.CharField(max_length = 150)
	description = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

class Zone(models.Model):
	client = models.ForeignKey(Client, related_name = 'z_client', on_delete = models.CASCADE)
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200, blank = True, null = True)

	def __str__(self):
		return self.name

class SmartAtomizer(models.Model):
	zone = models.ForeignKey(Zone, related_name = 'sa_zone', on_delete = models.CASCADE, blank = True, null = True)
	serial = models.CharField(max_length = 150)
	state = models.BooleanField(default = False)
	timer_interval = models.CharField(max_length = 5, default = '01:00')
	scheduled_interval = models.CharField(max_length = 200, default = '')
	atomizer_trigger_time = models.IntegerField(default = 1)
	sync_interval = models.CharField(max_length = 5, default = '01:00')
	log_information = models.IntegerField(default = 255)
	volume = models.IntegerField(default = 0)
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
