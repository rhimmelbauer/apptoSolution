
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
	print(len(Client.objects.all()))
	clientsTotalVolume = []
	for client in clients:
		clientTotalVolume = {'name': client.name, 'volume': client.smart_atomizer_client_volume()}
		clientsTotalVolume.append(clientTotalVolume)

	return render(request, 'dashboard.html', {'clients': clientsTotalVolume})

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
def new_zone(request, client_pk):
	client = get_object_or_404(Client, pk=client_pk)
	if request.method == 'POST':
		form = NewZoneForm(request.POST)
		if form.is_valid():
			print("form is valid")
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
def new_smart_atomizer(request):
	if request.method == 'POST':
		form = NewSmartAtomizerForm(request.POST)
		if form.is_valid():
			newClient = form.save(commit=False)
			newClient.save()
			return redirect('smart_atomizers')
	else:
		form = NewSmartAtomizerForm()
	return render(request, 'new_smart_atomizer.html', {'form': form})

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
					smartAtomizer.timer_interval = smartAtomizerSettings.timer_interval
					smartAtomizer.scheduled_interval = smartAtomizerSettings.scheduled_interval
					smartAtomizer.atomizer_trigger_time = smartAtomizerSettings.atomizer_trigger_time
					smartAtomizer.sync_interval = smartAtomizerSettings.sync_interval
					smartAtomizer.log_information = smartAtomizerSettings.log_information
					smartAtomizer.save()
			return redirect('zones', client.pk)
	else:
		form = ControlClientForm()
	return render(request, 'control_client.html', {'client': client, 'form': form})

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
				smartAtomizer.timer_interval = smartAtomizerSettings.timer_interval
				smartAtomizer.scheduled_interval = smartAtomizerSettings.scheduled_interval
				smartAtomizer.atomizer_trigger_time = smartAtomizerSettings.atomizer_trigger_time
				smartAtomizer.sync_interval = smartAtomizerSettings.sync_interval
				smartAtomizer.log_information = smartAtomizerSettings.log_information
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
	print("Enterd class")
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
