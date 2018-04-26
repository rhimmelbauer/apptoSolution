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

class NewRepresentativeForm(forms.ModelForm):
	first_name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'First Name eg: Daniel'}
				),
				max_length=50,
				help_text='Max length is 50 characters'
			)
	last_name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Last Name eg: Perez Gonazales'}
				),
				max_length=100,
				help_text='Max length is 100 characters'
			)

	class Meta:
		model = Representative
		fields = ['first_name',
		          'last_name']

class NewReportCheckUpForm(forms.ModelForm):
	

	class Meta:
		model = Report
		fields = ['checkup',
		          'visit_completed',
		          'notes']

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
				  'scheduled_start',
				  'scheduled_finish',
				  'atomizer_power',
				  'sync_interval',
				  'volume',
				  'activated']

class NewCheckUpForm(forms.ModelForm):
	day = forms.DateField(
				widget = forms.DateInput(
					attrs={'id': 'datepicker'}
					),
					help_text='YYYY-MM-DD'
				)
	start_time = forms.TimeField(
					widget = forms.TimeInput(),
					help_text='HH:MM:SS eg: 14:30:00')
	end_time = forms.TimeField(
					widget = forms.TimeInput(),
					help_text='HH:MM:SS eg: 15:30:00')

	class Meta:
		model = CheckUp
		fields = ['client',
				  'representative',
				  'day',
				  'start_time',
				  'end_time',
				  'notes']


class ControlClientForm(forms.ModelForm):

	class Meta:
		model = SmartAtomizer
		fields = ['state',
				  'scheduled_start',
				  'scheduled_finish',
				  'atomizer_power',
				  'sync_interval']

class ControlZoneForm(forms.ModelForm):

	class Meta:
		model = SmartAtomizer
		fields = ['state',
				  'scheduled_start',
				  'scheduled_finish',
				  'atomizer_power',
				  'sync_interval']


class EditAlertsForm(forms.ModelForm):

	class Meta:
		model = Alert
		fields = ['volume_warning',
				  'sync_time_warning']