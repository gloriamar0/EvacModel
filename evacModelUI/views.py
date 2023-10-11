from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse #may not need it if not used
from utils import get_db_handle
from .models import test_collection


def home(request):
    return render(request, "evacModelUI/home.html")

def results(request):
    cities = test_collection.find()
    return HttpResponse(cities)
    return render(request, "evacModelUI/results.html")