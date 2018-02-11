from django import forms
from .models import *

class NewZoneForm(forms.ModelForm):
	name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Write a name for the zone. Eg: Main Hall'}
				),
				max_length=50,
				help_text='Max length is 50 characters'
			)
	description = forms.CharField(
				widget = forms.Textarea(
					attrs={'rows': 5, 'placeholder': 'Additinal Notes, eg: Atomizer placed left corner.'}
				),
				max_length=200,
				help_text='Max length is 200 characters'
			)
	class Meta:
		model = Zone
		fields = ['name', 'description']

class NewClientForm(forms.ModelForm):
	name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Clients Name eg: Appto'}
				),
				max_length=50,
				help_text='Max length is 50 characters'
			)
	contact_name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Contacts full name eg: Pedro Paramo'}
				),
				max_length=100,
				help_text='Max length is 100 characters'
			)
	contact_phone = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Contacts phone number eg: +52 55 1234 5678'}
				),
				max_length=50,
				help_text='Max length is 50 characters'
			)
	address = forms.CharField(
				widget = forms.Textarea(
					attrs={'rows': 5, 'placeholder': 'Clients Address. eg: Alcanfores 23, San Jose de los Cedros, Cuajimalpa, CDMX'}
				),
				max_length=150,
				help_text='Max length is 150 characters'
			)
	description = forms.CharField(
				widget = forms.Textarea(
					attrs={'rows': 5, 'placeholder': 'Additinal Notes, eg: starting with 5 smart atomizers in the main hall'}
				),
				max_length=200,
				help_text='Max length is 200 characters'
			)	

	class Meta:
		model = Client
		fields = ['name',
		          'contact_name',
		          'contact_phone',
		          'address',
		          'description']

class NewSmartAtomizerForm(forms.ModelForm):
	serial = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'PixieBoard Serial'}
				),
				max_length=50,
				help_text='Max length is 50 characters'
			)	

	class Meta:
		model = SmartAtomizer
		fields = ['serial',
				  'state',
				  'timer_interval',
				  'scheduled_interval',
				  'atomizer_trigger_time',
				  'sync_interval',
				  'volume',
				  'activated']


class ControlClientForm(forms.ModelForm):

	class Meta:
		model = SmartAtomizer
		fields = ['state',
				  'timer_interval',
				  'scheduled_interval',
				  'atomizer_trigger_time',
				  'sync_interval',
				  'log_information']

class ControlZoneForm(forms.ModelForm):

	class Meta:
		model = SmartAtomizer
		fields = ['state',
				  'timer_interval',
				  'scheduled_interval',
				  'atomizer_trigger_time',
				  'sync_interval',
				  'log_information']