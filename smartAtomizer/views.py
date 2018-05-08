
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .forms import *
from .models import *


############################## FBVs ########################################
@login_required
def dashboard(request):
	clients = Client.objects.all()
	clientsTotalVolume = []
	for client in clients:
		clientTotalVolume = {'name': client.name, 'volume': client.smart_atomizer_client_total_volume()}
		clientsTotalVolume.append(clientTotalVolume)

	activeDevice = {
		'active': SmartAtomizer.objects.filter(activated=True).count(),
		'inactive': SmartAtomizer.objects.filter(activated=False).count()
	}

	devices = SmartAtomizer.objects.all()
	deviceLocations = []
	for device in devices:
		deviceLocation = {'serial': device.serial, 'lat': device.latitude, 'long': device.longitude}
		deviceLocations.append(deviceLocation)

	return render(request, 'dashboard.html', {'clients': clientsTotalVolume, 'activeDevice': activeDevice, 'deviceLocations': deviceLocations})

@login_required
def new_client(request):
	if request.method == 'POST':
		form = NewClientForm(request.POST)
		if form.is_valid():
			newClient = form.save(commit=False)
			newClient.save()
			return redirect('clients')
	else:
		form = NewClientForm()
	return render(request, 'new_client.html', {'form': form})

@login_required
def new_representative(request):
	if request.method == 'POST':
		form = NewRepresentativeForm(request.POST)
		if form.is_valid():
			newRep = form.save(commit=False)
			newRep.save()
			return redirect('representatives')
	else:
		form = NewRepresentativeForm()
	return render(request, 'new_representative.html', {'form': form})

@login_required
def new_checkup(request):
	if request.method == 'POST':
		form = NewCheckUpForm(request.POST)
		print(form)
		if form.is_valid():
			newRep = form.save(commit=False)
			newRep.save()
			return redirect('schedule')
	else:
		form = NewCheckUpForm()
	return render(request, 'new_checkup.html', {'form': form})

@login_required
def report_checkup(request):
	if request.method == 'POST':
		form = NewReportCheckUpForm(request.POST)
		print(form)
		if form.is_valid():
			newRep = form.save(commit=False)
			newRep.save()
			return redirect('schedule')
	else:
		form = NewReportCheckUpForm()
	return render(request, 'report_checkup.html', {'form': form})

@login_required
def new_zone(request, client_pk):
	client = get_object_or_404(Client, pk=client_pk)
	if request.method == 'POST':
		form = NewZoneForm(request.POST)
		if form.is_valid():
			newZone = form.save(commit=False)
			newZone.client = client
			newZone.save()
			return redirect('zones', client_pk=client.pk)
	else:
		form = NewZoneForm()
	return render(request, 'new_zone.html', {'form': form, 'client': client})

@login_required
def smart_atomizers(request):
	return render(request, 'smart_atomizers.html')

@login_required
def schedule(request):
	today = datetime.now().date()
	checkups = CheckUp.objects.filter(day__gte=today).order_by('day', 'start_time','client')
	return render(request, 'schedule.html',{'checkups': checkups})

@login_required
def new_smart_atomizer(request):
	if request.method == 'POST':
		form = NewSmartAtomizerForm(request.POST)
		if form.is_valid():
			new_smart_atomizer = form.save(commit=False)
			new_smart_atomizer.save()
			return redirect('smart_atomizers')
	else:
		form = NewSmartAtomizerForm()
	return render(request, 'new_smart_atomizer_schedule.html', {'form': form})

def new_smart_atomizer_schedule(request, smart_atomizer_pk):
	smart_atomizer = get_object_or_404(SmartAtomizer, pk=smart_atomizer_pk)
	if request.method == 'POST':
		form = NewSmartAtomizerScheduleForm(request.POST)
		if form.is_valid():
			smart_atomizer_schedule = form.save(commit=False)
			smart_atomizer_schedule.smart_atomizer = smart_atomizer
			smart_atomizer_schedule.save()
			return redirect('smart_atomizer_schedule', smart_atomizer.pk)
	else:
		form = NewSmartAtomizerScheduleForm()
	return render(request, 'new_smart_atomizer_schedule.html', {'form': form, 'smart_atomizer': smart_atomizer})

@login_required
def assign_smart_atomizer(request):
	return render(request, 'assign_smart_atomizer.html')

@login_required
def control_client(request, client_pk):
	client = get_object_or_404(Client, pk=client_pk)
	if request.method == 'POST':
		form = ControlClientForm(request.POST)
		if form.is_valid():
			smartAtomizerSettings = form.save(commit=False)
			clientZones = Zone.objects.filter(client=client)
			for zone in clientZones:
				zoneSmartAtomizers = SmartAtomizer.objects.filter(zone=zone)
				for smartAtomizer in zoneSmartAtomizers:
					smartAtomizer.state = smartAtomizerSettings.state
					smartAtomizer.scheduled_start = smartAtomizerSettings.scheduled_start
					smartAtomizer.scheduled_finish = smartAtomizerSettings.scheduled_finish
					smartAtomizer.atomizer_power = smartAtomizerSettings.atomizer_power
					smartAtomizer.sync_interval = smartAtomizerSettings.sync_interval
					smartAtomizer.save()
			return redirect('zones', client.pk)
	else:
		form = ControlClientForm()
	return render(request, 'control_client.html', {'client': client, 'form': form})

@login_required
def edit_alerts_client(request, client_pk):
	client = get_object_or_404(Client, pk=client_pk)
	if request.method == 'POST':
		form = EditAlertsForm(request.POST)
		if form.is_valid():
			alerts = form.save(commit=False)
			clientZones = Zone.objects.filter(client=client)
			for zone in clientZones:
				zoneSmartAtomizers = SmartAtomizer.objects.filter(zone=zone)
				for smartAtomizer in zoneSmartAtomizers:
					alert = Alert.objects.get(smart_atomizer=smartAtomizer)
					alert.volume_warning = alerts.volume_warning
					alert.sync_time_warning = alerts.sync_time_warning
					alert.save()
			return redirect('zones', client.pk)
	else:
		form = EditAlertsForm()
	return render(request, 'edit_alerts_client.html', {'client': client, 'form': form})

@login_required
def edit_alerts_zone(request, client_pk, zone_pk):
	client = get_object_or_404(Client, pk=client_pk)
	zone = get_object_or_404(Zone, pk=zone_pk)
	if request.method == 'POST':
		form = EditAlertsForm(request.POST)
		if form.is_valid():
			alerts = form.save(commit=False)
			zoneSmartAtomizers = SmartAtomizer.objects.filter(zone=zone)
			for smartAtomizer in zoneSmartAtomizers:
				alert = Alert.objects.get(smart_atomizer=smartAtomizer)
				alert.volume_warning = alerts.volume_warning
				alert.sync_time_warning = alerts.sync_time_warning
				alert.save()
			return redirect('smart_atomizers_assigned_zone', client.pk, zone.pk)
	else:
		form = EditAlertsForm()
	return render(request, 'edit_alerts_zone.html', {'client': client, 'zone': zone, 'form': form})

@login_required
def edit_alerts_smart_atomizer_zone(request, client_pk, zone_pk, smart_atomizer_pk):
	smart_atomizer = get_object_or_404(SmartAtomizer, pk=smart_atomizer_pk)
	if request.method == 'POST':
		form = EditAlertsForm(request.POST)
		if form.is_valid():
			alerts = form.save(commit=False)
			alert = Alert.objects.get(smart_atomizer=smart_atomizer)
			alert.volume_warning = alerts.volume_warning
			alert.sync_time_warning = alerts.sync_time_warning
			alert.save()
			return redirect('edit_smart_atomizer_zone', smart_atomizer.zone.client.pk, smart_atomizer.zone.pk, smart_atomizer.pk)
	else:
		form = EditAlertsForm()
	return render(request, 'edit_alerts_smart_atomizer_zone.html', {'client': smart_atomizer.zone.client, 'zone': smart_atomizer.zone, 'smart_atomizer': smart_atomizer, 'form': form})

@login_required
def control_zone(request, client_pk, zone_pk):
	client = get_object_or_404(Client, pk=client_pk)
	zone = get_object_or_404(Zone, pk=zone_pk)
	if request.method == 'POST':
		form = ControlZoneForm(request.POST)
		if form.is_valid():
			smartAtomizerSettings = form.save(commit=False)
			zoneSmartAtomizers = SmartAtomizer.objects.filter(zone=zone)
			for smartAtomizer in zoneSmartAtomizers:
				smartAtomizer.state = smartAtomizerSettings.state
				smartAtomizer.scheduled_start = smartAtomizerSettings.scheduled_start
				smartAtomizer.scheduled_interval = smartAtomizerSettings.scheduled_finish
				smartAtomizer.atomizer_power = smartAtomizerSettings.atomizer_power
				smartAtomizer.sync_interval = smartAtomizerSettings.sync_interval
				smartAtomizer.save()
			return redirect('smart_atomizers_assigned_zone', client.pk, zone.pk)
	else:
		form = ControlZoneForm()
	return render(request, 'control_zone.html', {'client':client, 'zone': zone, 'form': form})

@login_required
def add_smart_atomizer_zone(request, client_pk, zone_pk):
	client = get_object_or_404(Client, pk=client_pk)
	zone = get_object_or_404(Zone, pk=zone_pk)
	if request.method == 'POST':
		print(request.POST)
		atomizersInTable = request.POST.getlist('atomizersTable')
		print("-----------------------------Atomizers itn table______________________")
		
		for at in atomizersInTable:
			smartAtomizer = SmartAtomizer.objects.get(pk=at)
			smartAtomizer.zone = zone
			smartAtomizer.save()
		
		return redirect('smart_atomizers_assigned_zone', zone.client.pk, zone.pk)
	else:
		queryset = SmartAtomizer.objects.filter(zone__isnull=True)
		page = request.GET.get('page', 1)
		paginator = Paginator(queryset, 20)

		try:
			smart_atomizers = paginator.page(page)
		except PageNotAnInteger:
			# fallback to the first page
			smart_atomizers = paginator.page(1)
		except EmptyPage:
			# probably the user tried to add a page number
			# in the url, so we fallback to the last page
			smart_atomizers = paginator.page(paginator.num_pages)
	return render(request, 'add_smart_atomizer_zone.html',{'client': client, 'zone': zone, 'smart_atomizers': smart_atomizers})


@login_required
def delete_client(request, client_pk):
	client = get_object_or_404(Client, pk=client_pk)
	zones = Zone.objects.filter(client=client)
	for zone in zones:
		smartAtomizers = SmartAtomizer.objects.filter(zone=zone)
		for smartAtomizer in smartAtomizers:
			smartAtomizer.zone = None
			smartAtomizer.state = False
			smartAtomizer.activated = False
			smartAtomizer.save()
		zone.delete()
	client.delete()
	return redirect('clients')

def delete_zone(request, zone_pk):
	zone = get_object_or_404(Zone, pk=zone_pk)
	client_pk = zone.client.pk
	smartAtomizers = SmartAtomizer.objects.filter(zone=zone)
	for smartAtomizer in smartAtomizers:
		smartAtomizer.zone = None
		smartAtomizer.state = False
		smartAtomizer.activated = False
		smartAtomizer.save()

	zone.delete()
	return redirect('zones', client_pk)

def delete_smart_atomizer(request, smart_atomizer_pk):
	zone = get_object_or_404(SmartAtomizer, pk=smart_atomizer_pk)
	zone.delete()
	return redirect('smart_atomizers')

def delete_smart_atomizer_schedule(request, smart_atomizer_pk, smart_atomizer_schedule_pk):
	smart_atomizer = get_object_or_404(SmartAtomizer, pk=smart_atomizer_pk)
	smart_atomizer_schedule = get_object_or_404(SmartAtomizerSchedule, pk=smart_atomizer_schedule_pk)
	smart_atomizer_schedule.delete()
	return redirect('smart_atomizer_schedule', smart_atomizer.pk)

def remove_from_zone(request, smart_atomizer_pk):
	smartAtomizer = get_object_or_404(SmartAtomizer, pk=smart_atomizer_pk)
	client_pk = smartAtomizer.zone.client.pk
	zone_pk = smartAtomizer.zone.pk
	smartAtomizer.zone = None
	smartAtomizer.save()
	return redirect('smart_atomizers_assigned_zone', client_pk, zone_pk)

def alerts(request):
	queryset = []
	alerts = Alert.objects.all()
	for alert in alerts:
		if alert.smart_atomizer.volume < alert.volume_warning:
			queryset.append(alert)

	syncLogs = SyncLog.objects.all()
	volumeLogs = VolumeLog.objects.all()

	return render(request, 'alerts.html', {'alerts': queryset, 'syncLogs': syncLogs, 'volumeLogs': volumeLogs})

############################## GCBVs ########################################

############################## ListViews ########################################
@method_decorator(login_required, name="dispatch")
class ClientsListView(ListView):
	model = Client
	context_object_name = 'clients'
	template_name = 'clients.html'
	paginate_by = 10

@method_decorator(login_required, name="dispatch")
class ZonesListView(ListView):
	model = Zone
	context_object_name = 'zones'
	template_name = 'zones.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		kwargs['client'] = self.client
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.client = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
		queryset = Zone.objects.filter(client = self.client)
		return queryset

@method_decorator(login_required, name="dispatch")
class SmartAtomizerScheduleListView(ListView):
	model = SmartAtomizerSchedule
	context_object_name = 'schedules'
	template_name = 'smart_atomizer_schedule.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		kwargs['smart_atomizer'] = self.smart_atomizer
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.smart_atomizer = get_object_or_404(SmartAtomizer, pk=self.kwargs.get('smart_atomizer_pk'))
		queryset = SmartAtomizerSchedule.objects.filter(smart_atomizer = self.smart_atomizer)
		return queryset

@method_decorator(login_required, name="dispatch")
class SmartAtomizersListView(ListView):
	model = SmartAtomizer
	context_object_name = 'smart_atomizers'
	template_name = 'smart_atomizers.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		queryset = SmartAtomizer.objects.order_by('zone')
		return queryset

@method_decorator(login_required, name="dispatch")
class PendingActivationsListView(ListView):
	model = SmartAtomizer
	context_object_name = 'smart_atomizers'
	template_name = 'pending_activations.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		queryset = SmartAtomizer.objects.filter(activated = False)
		return queryset

@method_decorator(login_required, name="dispatch")
class SmartAtomizerAssignedZoneView(ListView):
	model = SmartAtomizer
	context_object_name = 'smart_atomizers'
	template_name = 'smart_atomizers_assigned_zone.html'
	paginate_by = 10


	def get_context_data(self, **kwargs):
		kwargs['client'] = self.client
		kwargs['zone'] = self.zone
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.client = get_object_or_404(Client, pk=self.kwargs.get('client_pk'))
		self.zone = get_object_or_404(Zone, pk=self.kwargs.get('zone_pk'))
		queryset = SmartAtomizer.objects.filter(zone=self.zone)
		return queryset

@method_decorator(login_required, name="dispatch")
class AlertsView(ListView):
	model = Alert
	context_object_name = 'alerts'
	template_name = 'alerts.html'
	paginate_by = 10


	def get_context_data(self, **kwargs):
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		queryset = []
		alerts = Alert.objects.all()
		for alert in alerts:
			if alert.smart_atomizer.volume < alert.volume_warning:
				queryset.append(alert)

		return queryset

@method_decorator(login_required, name="dispatch")
class RepresentativesListView(ListView):
	model = Representative
	context_object_name = 'reps'
	template_name = 'representatives.html'
	paginate_by = 10

@method_decorator(login_required, name="dispatch")
class ReportsListView(ListView):
	model = Report
	context_object_name = 'reports'
	template_name = 'reports.html'
	paginate_by = 10

############################## UpdateViews ########################################

@method_decorator(login_required, name="dispatch")
class UpdateClientView(UpdateView):
	model = Client
	form_class = NewClientForm
	template_name = 'edit_client.html'
	pk_url_kwarg = 'client_pk'
	context_object_name = 'client'

	def form_valid(self, form):
		client = form.save(commit=False)
		client.save()
		return redirect('zones', client_pk=client.pk)

@method_decorator(login_required, name="dispatch")
class UpdateSmartAtomizerView(UpdateView):
	model = SmartAtomizer
	form_class = NewSmartAtomizerForm
	template_name = 'edit_smart_atomizer.html'
	pk_url_kwarg = 'smart_atomizer_pk'
	context_object_name = 'smart_atomizer'

	def form_valid(self, form):
		print('inside val')
		smartAtomizer = form.save(commit=False)
		smartAtomizer.save()
		return redirect('smart_atomizers')

@method_decorator(login_required, name="dispatch")
class UpdateSmartAtomizerZoneView(UpdateView):
	model = SmartAtomizer
	form_class = NewSmartAtomizerForm
	template_name = 'edit_smart_atomizer_zone.html'
	pk_url_kwarg = 'smart_atomizer_pk'
	context_object_name = 'smart_atomizer'

	def form_valid(self, form):
		smartAtomizer = form.save(commit=False)
		smartAtomizer.save()
		return redirect('smart_atomizers_assigned_zone', client_pk=smartAtomizer.zone.client.pk, zone_pk=smartAtomizer.zone.pk)


@method_decorator(login_required, name="dispatch")
class UpdateSmartAtomizerScheduleView(UpdateView):
	model = SmartAtomizerSchedule
	form_class = NewSmartAtomizerScheduleForm
	template_name = 'edit_smart_atomizer_schedule.html'
	pk_url_kwarg = 'smart_atomizer_schedule_pk'
	context_object_name = 'smart_atomizer_schedule'

	def form_valid(self, form):
		smartAtomizer = form.save(commit=False)
		smartAtomizer.save()
		return redirect('smart_atomizer_schedule', smart_atomizer_pk=smartAtomizer.smart_atomizer.pk)

@method_decorator(login_required, name="dispatch")
class UpdateZoneView(UpdateView):
	model = Zone
	form_class = NewZoneForm
	template_name = 'edit_zone.html'
	pk_url_kwarg = 'zone_pk'
	context_object_name = 'zone'


	def form_valid(self, form):
		zone = form.save(commit=False)
		zone.save()
		return redirect('smart_atomizers_assigned_zone', client_pk=zone.client.pk, zone_pk=zone.pk)


########################## CALENDAR ########################################
