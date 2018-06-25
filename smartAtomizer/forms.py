from django import forms
from .models import *

class NewZoneForm(forms.ModelForm):
	name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Escriba un nombre representativo de la zona. Ejemplo: Lobby'}
				),
				label='Nombre de la Zona',
				max_length=50,
				help_text='Máximo 50 carácteres.'
			)
	description = forms.CharField(
				widget = forms.Textarea(
					attrs={'rows': 5, 'placeholder': 'Agregue una descriptción, Ejemplo: El atomizador fue instalado al final del pasillo.'}
				),
				label='Descripción',
				max_length=200,
				help_text='Máximo 2000 carácteres.'
			)
	class Meta:
		model = Zone
		fields = ['name', 'description']

class NewClientForm(forms.ModelForm):
	name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Ejemplo: Camino Real Santa Fe'}
				),
				label='Nombre de la Empresa',
				max_length=50,
				help_text='Máximo 50 carácteres.'
			)
	contact_name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Ejemplo: Pedro Paramo'}
				),
				label='Nombre del Contacto',
				max_length=100,
				help_text='Máximo 100 carácteres.'
			)
	contact_phone = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Ejemplo: +52 55 1234 5678'}
				),
				label='Télefono del Contacto',
				max_length=50,
				help_text='Máximo 50 carácteres.'
			)
	address = forms.CharField(
				widget = forms.Textarea(
					attrs={'rows': 5, 'placeholder': 'Ejemplo: Alcanfores 23, San Jose de los Cedros, Cuajimalpa, CDMX'}
				),
				label='Dirección',
				max_length=150,
				help_text='Máximo 150 carácteres.'
			)
	description = forms.CharField(
				widget = forms.Textarea(
					attrs={'rows': 5, 'placeholder': 'Ejemplo: El cliente cuenta con 5 atomizadores'}
				),
				label='Descripción',
				max_length=200,
				help_text='Máximo 200 carácteres.'
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
					attrs={'placeholder': 'Ejemplo: Daniel'}
				),
				label='Nombre',
				max_length=50,
				help_text='Máximo 50 carácteres.'
			)
	last_name = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Ejemplo: Perez Gonazales'}
				),
				label='Apellidos',
				max_length=100,
				help_text='Máximo 100 carácteres.'
			)

	class Meta:
		model = Representative
		fields = ['first_name',
		          'last_name']

class NewReportCheckUpForm(forms.ModelForm):

	visit_completed = forms.CharField(
				widget = forms.BooleanField(),
				label='Visita Completada',
			)
	notes = forms.CharField(
				widget = forms.TextInput(
					attrs={'placeholder': 'Ejemplo: Se cambio el líquido.'}
				),
				label='Notas de la Visita',
				max_length=100,
				help_text='Máximo 250 carácteres.'
			)
	

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
				help_text='Máximo 50 carácteres.'
			)	

	state = forms.BooleanField(
				required=False,
				label='Estado',
				help_text='Encendido/Apagado'

			)

	sync_interval = forms.CharField(
				widget = forms.TextInput(
					attrs={ 'placeholder': '7'}
				),
				label='Interval de Sincronización',
				max_length=5,
				help_text=""
			)

	volume = forms.DecimalField(
				label='Volumen del Líquido Restante mL',
				help_text='Ingresar el Volumen del aromatizador'
			)

	activated = forms.BooleanField(
				required=False,
				label='Ativado',
				help_text='Activado/Desactivado'
			)

	class Meta:
		print('inside form')
		model = SmartAtomizer
		fields = ['serial',
				  'state',
				  'sync_interval',
				  'volume',
				  'activated']

class NewSmartAtomizerScheduleForm(forms.ModelForm):	

	scheduled_start = forms.CharField(
				label='Hora de Comienzo',
				help_text="Ejemplo 07:00"
				)

	scheduled_finish = forms.CharField(
				label='Hora de Fin',
				help_text='Ejemplo 13:00'
				)

	

	class Meta:
		model = SmartAtomizerSchedule
		fields = ['scheduled_start',
				  'scheduled_finish',
				  'atomizer_power',]

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
				  'sync_interval']

class ControlZoneForm(forms.ModelForm):

	class Meta:
		model = SmartAtomizer
		fields = ['state',
				  'sync_interval']


class EditAlertsForm(forms.ModelForm):

	class Meta:
		model = Alert
		fields = ['volume_warning',
				  'sync_time_warning']
