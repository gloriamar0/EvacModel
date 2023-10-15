from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse #may not need it if not used
from utils import get_db_handle

def home(request):
    return render(request, "evacModelUI/home.html")

def results(request):
    # Loading in database and collections
    url = 'mongodb://localhost:27017/'
    db = get_db_handle("evacModelData", url)
    input_collection = db['input']

    # Retrieving information from POST request and updating database
    if request.method == "POST":
        inputForm = request.POST
        inputCity = inputForm['cities']
        inputEvent = inputForm['event']
        inputPopulation = inputForm['population']
        input_collection.update_one(
            {'id': 0},
            {'$set': {'city': inputCity,
                      'event': inputEvent,
                      'population': inputPopulation} })
        
        """ input_collection.insert_one(
            {'id': 0,
             'city': inputCity,
             'event': inputEvent,
             'population': inputPopulation} ) """

    # Displaying results
    inputs = input_collection.find()
    return render(request, "evacModelUI/results.html", {'inputs_list': inputs })