from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse #may not need it if not used
from utils import get_db_handle
from evacModelUI.db_functions import *
import gridfs

def home(request):
    return render(request, "evacModelUI/home.html")

def results(request):
    # Loading in database and collections
    url = 'mongodb+srv://gloriamar0:V6mSlQAbfbaSzzj1@cluster0.c0et8hr.mongodb.net/'
    db = get_db_handle("evacModelData", url)
    input_collection = db['input']

    fs = gridfs.GridFS(db)  #used for large files

    # Retrieving information from POST request and updating database
    if request.method == "POST":
        inputForm = request.POST
        updateInputs(input_collection, inputForm)


    # Storing output files into database
    # output_files = ['modestats_stackedbar.png',
    #                 'modestats.png',
    #                 'modestats.txt',
    #                 'ph_modestats.png',
    #                 'ph_modestats.txt',
    #                 'pkm_modestats.png',
    #                 'pkm_modestats.txt',
    #                 'scorestats.png',
    #                 'scorestats.txt',
    #                 'stopwatch.png',
    #                 'stopwatch.txt',
    #                 'traveldistancestats.txt',
    #                 'traveldistancestatslegs.png',
    #                 'traveldistancestatstrips.png']
    
    # Deciding which files to display in UI
    images_list = ['scorestats.png','stopwatch.png']
    display_text = ['scorestats.txt']

    # Retrieving PNGs and saving in static folder
    # for img_file_name in images_list:
    #     data = db.fs.files.find_one({'filename': img_file_name})
    #     file_content = fs.get(data['_id']).read()
    #     output_file = open("evacModelUI/static/evacModelUI/" + img_file_name, 'wb')
    #     output_file.write(file_content)
    #     output_file.close()

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
        
    # Retrieving data for display
    inputs = input_collection.find()
    images = getImages(db, fs, images_list)

    return render(request, "evacModelUI/results.html", {'inputs_list': inputs, 'images': images, 'text_list': txt_file_content})