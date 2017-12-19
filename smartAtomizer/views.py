from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

def dashboard(request):
	return render(request, 'dashboard.html')

def clients(request):
	return render(request, 'clients.html')

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

def zones(request, pk):
	client = get_object_or_404(Client, pk=pk)
	return render(request, 'zones.html', {'client': client})

def new_zone(request, pk):
	client = get_object_or_404(Client, pk=pk)
	if request.method == 'POST':
		form = NewZoneForm(request.POST)
		if form.is_valid():
			newZone = form.save(commit=False)
			newZone.cliente = client
			newZone.save()
			return redirect('zones', pk=client.pk)
	else:
		form = NewZoneForm
	return render(request, 'new_zone.html', {'form': form, 'client': client})

def smart_atomizers(request):
	return render(request, 'smart_atomizers.html')

def new_smart_atomizer(request):
	return render(request, 'new_smart_atomizer.html')

def assign_smart_atomizer(request):
	return render(request, 'assign_smart_atomizer.html')