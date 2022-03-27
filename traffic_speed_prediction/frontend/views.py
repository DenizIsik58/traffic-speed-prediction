from django.shortcuts import render, redirect

# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

def finmap(request, *args, **kwargs):
    mapbox_access_token = 'pk.eyJ1IjoidnNvbi1zb2xpdGEiLCJhIjoiY2wxNmlqcG5jMDdyMjNkcGt1N241bTV3eSJ9'

    

    return render(request, 'frontend/finmap.html', { 'mapbox_access_token': mapbox_access_token })

def apiSite(request, *args, **kwargs):
    return render(request, 'frontend/api.html')

def solita(request, *args, **kwargs):
    return render(request, 'frontend/solita.html')

def itu(request, *args, **kwargs):
    return render(request, 'frontend/itu.html')

def aboutUs(request, *args, **kwargs):
    return render(request, 'frontend/about_us.html')
