from django.shortcuts import render, redirect, get_object_or_404


def home(request):
	return render(request, 'dashboard.html')

def clients(request):
	return render(request, 'clients.html')

def new_client(request):
	return render(request, 'new_client.html')

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