
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import *
from .models import *

def dashboard(request):
	return render(request, 'dashboard.html')

class ClientsListView(ListView):
	model = Client
	context_object_name = 'clients'
	template_name = 'clients.html'
	paginate_by = 10


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

class ZonesListView(ListView):
	model = Zone
	context_object_name = 'zones'
	template_name = 'zones.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		kwargs['client'] = self.client
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
		queryset = Zone.objects.filter(client = self.client)
		return queryset

class SmartAtomizerAssignedZoneView(ListView):
	print("Enterd class")
	model = SmartAtomizer
	context_object_name = 'smart_atomizers'
	template_name = 'smart_atomizers_assigned_zone.html'
	paginate_by = 10


	def get_context_data(self, **kwargs):
		print("Enterd get get_context_data")
		kwargs['client'] = self.client
		kwargs['zone'] = self.zone
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		print("Enterd get get_queryset")
		self.client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
		print(self.client)
		self.zone = get_object_or_404(Zone, pk=self.kwargs.get('zone_pk'))
		print(self.zone)
		queryset = SmartAtomizer.objects.filter(zone=self.zone)
		return queryset


def new_zone(request, pk):
	client = get_object_or_404(Client, pk=pk)
	if request.method == 'POST':
		form = NewZoneForm(request.POST)
		if form.is_valid():
			print("form is valid")
			newZone = form.save(commit=False)
			newZone.client = client
			newZone.save()
			return redirect('zones', pk=client.pk)
	else:
		form = NewZoneForm()
	return render(request, 'new_zone.html', {'form': form, 'client': client})

def smart_atomizers(request):
	return render(request, 'smart_atomizers.html')

def new_smart_atomizer(request):
	if request.method == 'POST':
		form = NewSmartAtomizerForm(request.POST)
		if form.is_valid():
			newClient = form.save(commit=False)
			newClient.save()
			return redirect('clients')
	else:
		form = NewSmartAtomizerForm()
	return render(request, 'new_client.html', {'form': form})

def assign_smart_atomizer(request):
	return render(request, 'assign_smart_atomizer.html')

def control_client(request, pk):
	client = get_object_or_404(Client, pk=pk)
	if request.method == 'POST':
		return redirect('dashboard')
	else:
		form = ControlClientForm()
	return render(request, 'control_client.html', {'client': client, 'form': form})


def control_zone(request, pk):
	zone = get_object_or_404(Zone, pk=pk)
	if request.method == 'POST':
		return redirect('dashboard')
	else:
		form = ControlZoneForm()
	return render(request, 'control_zone.html', {'zone': zone, 'form': form})