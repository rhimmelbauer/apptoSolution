
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
	return render(request, 'dashboard.html')

def helloReq(request, pk, volume):
	smartAtomizer = get_object_or_404(SmartAtomizer, pk=pk)
	volumeLog = VolumeLog()
	volumeLog.smart_atomizer = smartAtomizer
	volumeLog.log_time = datetime.now()
	volumeLog.volume = volume
	volumeLog.save()
	response = JsonResponse({'smart_atomizer': 'testing callback'})
	return response

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
def control_client(request, pk):
	client = get_object_or_404(Client, pk=pk)
	if request.method == 'POST':
		return redirect('dashboard')
	else:
		form = ControlClientForm()
	return render(request, 'control_client.html', {'client': client, 'form': form})

@login_required
def control_zone(request, pk):
	zone = get_object_or_404(Zone, pk=pk)
	if request.method == 'POST':
		return redirect('dashboard')
	else:
		form = ControlZoneForm()
	return render(request, 'control_zone.html', {'zone': zone, 'form': form})

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
		
		return redirect('clients')
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
		self.client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
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
		queryset = SmartAtomizer.objects.all().order_by('zone')
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

@method_decorator(login_required, name="dispatch")
class UpdateClientView(UpdateView):
	model = Client
	form_class = NewClientForm
	template_name = 'edit_client.html'
	pk_url_kwarg = 'pk'
	context_object_name = 'client'

	def form_valid(self, form):
		client = form.save(commit=False)
		client.save()
		return redirect('clients')

@method_decorator(login_required, name="dispatch")
class UpdateZoneView(UpdateView):
	model = Zone
	form_class = NewZoneForm
	template_name = 'edit_zone.html'
	pk_url_kwarg = 'pk'
	context_object_name = 'zone'

	def form_valid(self, form):
		zone = form.save(commit=False)
		zone.save()
		return redirect('clients')
