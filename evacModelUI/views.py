from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse #may not need it if not used
from utils import get_db_handle
import gridfs

def home(request):
    return render(request, "evacModelUI/home.html")

def results(request):
    # Loading in database and collections
    url = 'mongodb://localhost:27017/'
    db = get_db_handle("evacModelData", url)



    # Storing output files into database
    fs = gridfs.GridFS(db)  #used for large files
    output_files = ['modestats_stackedbar.png',
                    'modestats.png',
                    'modestats.txt',
                    'ph_modestats.png',
                    'ph_modestats.txt',
                    'pkm_modestats.png',
                    'pkm_modestats.txt',
                    'scorestats.png',
                    'scorestats.txt',
                    'stopwatch.png',
                    'stopwatch.txt',
                    'traveldistancestats.txt',
                    'traveldistancestatslegs.png',
                    'traveldistancestatstrips.png']
    
    # Writing in the database
    # for file in output_files:
    #     file_location = "evacModelUI/outputForTesting/" + file
    #     file_data = open(file_location, "rb")
    #     data = file_data.read()
    #     file_data.close()

    #     fs.put(data, filename = file)

    data = db.fs.files.find_one({'filename': 'stopwatch.png'})
    outputData = fs.get(data['_id']).read()
    decoded = open('evacModelUI/static/evacModelUI/test5.png', 'wb')
    decoded.write(outputData)
    decoded.close()



    # Retrieving information from POST request and updating database
    input_collection = db['input']
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