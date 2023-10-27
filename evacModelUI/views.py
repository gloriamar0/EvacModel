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
    inputs = input_collection.find()

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
    
    ## Writing in the database
    # for file in output_files:
    #     file_location = "evacModelUI/outputForTesting/" + file
    #     file_data = open(file_location, "rb")
    #     data = file_data.read()
    #     file_data.close()

    #     fs.put(data, filename = file)
    
    # Deciding which files to display in UI
    display_images = ['scorestats.png',
                      'stopwatch.png']
                     
    display_text = ['scorestats.txt']

    # Retrieving PNGs and saving in static folder
    for img_file_name in display_images:
        data = db.fs.files.find_one({'filename': img_file_name})
        file_content = fs.get(data['_id']).read()
        output_file = open("evacModelUI/static/evacModelUI/" + img_file_name, 'wb')
        output_file.write(file_content)
        output_file.close()

    # Retrieving TXT files
    txt_file_content = {}
    for txt_file_name in display_text:
        data = db.fs.files.find_one({'filename': txt_file_name})
        file_content = fs.get(data['_id']).readlines()

        headers = file_content.pop(0).decode().split("\t")
        content = []
        for line in file_content:
            content.append(line.decode().split("\t"))
            for i in range(1, len(headers)):
                content[-1][i] = content[-1][i][0:6]

        txt_file_content.update({'title': 'Score Statistics Table:',
                                 'headers': headers,
                                 'content': content})

    return render(request, "evacModelUI/results.html", {'inputs_list': inputs, 'text_list': txt_file_content})