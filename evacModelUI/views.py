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
    text_files_list = ['scorestats.txt']

    # Retrieving data for display
    inputs = input_collection.find()
    images = getImages(db, fs, images_list)
    txt_file_content = getTextFiles(db, fs, text_files_list)

    return render(request, "evacModelUI/results.html", {'inputs_list': inputs, 'images': images, 'text_list': txt_file_content})