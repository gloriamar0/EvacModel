from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse #may not need it if not used
from utils import get_db_handle

def home(request):
    return render(request, "evacModelUI/home.html")

def results(request):
    return render(request, "evacModelUI/results.html")