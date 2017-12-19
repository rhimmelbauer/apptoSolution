from django.shortcuts import render, redirect, get_object_or_404


def home(request):
	return render(request, 'dashboard.html')

def clients(request):
	return render(request, 'clients.html')

def zones(request):
	return render(request, 'zones.html')

def smart_atomizers(request):
	return render(request, 'smart_atomizers.html')