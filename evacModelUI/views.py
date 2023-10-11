from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse #may not need it if not used
from utils import get_db_handle
#from .models import test_collection


def home(request):
    return render(request, "evacModelUI/home.html")

def results(request):
    url = 'mongodb://localhost:27017/'
    db = get_db_handle("evacModelData", url)
    cities_collection = db['cities']
    #cities_collection.insertOne({'name' : 'Test'}) ## doesn't work because it is a GET request
    cities = cities_collection.find()
    #return HttpResponse(cities)
    return render(request, "evacModelUI/results.html")