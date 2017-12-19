from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

def home(request):
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

def zones(request):
	return render(request, 'zones.html')

def new_zone(request):
	return render(request, 'new_zone.html')

def smart_atomizers(request):
	return render(request, 'smart_atomizers.html')

def new_smart_atomizer(request):
	return render(request, 'new_smart_atomizer.html')

def assign_smart_atomizer(request):
	return render(request, 'assign_smart_atomizer.html')