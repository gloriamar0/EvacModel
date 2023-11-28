from base64 import b64encode

# Only to use if want to save more than one input forms
def insertInputs(input_collection, inputForm):
    # Retrieving each input
    inputCity = inputForm['cities']
    inputEvent = inputForm['event']
    inputPopulation = inputForm['population']

    input_collection.insert_one({'id': 0, 'city': inputCity, 'event': inputEvent, 'population': inputPopulation} )

# Updates inputs from exisiting database entry
def updateInputs(input_collection, inputForm):
    # Retrieving each input
    inputCity = inputForm['cities']
    inputEvent = inputForm['event']
    inputPopulation = inputForm['population']

    input_collection.update_one({'id': 0},
                                {'$set': {'city': inputCity,
                                          'event': inputEvent,
                                          'population': inputPopulation} })

def storeLargeFileDatabase(fs, file_name, file_location):
    file_data = open(file_location, "rb")
    data = file_data.read()
    file_data.close()
    fs.put(data, filename = file_name)

# Retrives images in an encoded Base64 format
def getImages(db, fs, img_name_list):
    images = []
    for img_name in img_name_list:
        data = db.fs.files.find_one({'filename': img_name})
        file_content = b64encode(fs.get(data['_id']).read())
        images.append(str(file_content, 'utf-8'))
    return images

# Retrives text files formatted ready for implementation in a table
def getTextFiles(db, fs, txt_name_list):
    txt_files = {}  #empty dictionary
    for txt_name in txt_name_list:
        data = db.fs.files.find_one({'filename': txt_name})
        file_content = fs.get(data['_id']).readlines()

        headers = file_content.pop(0).decode().split("\t")
        content = []
        for line in file_content:
            content.append(line.decode().split("\t"))
            for i in range(1, len(headers)):
                content[-1][i] = content[-1][i][0:6]

        txt_files.update({'title': 'Score Statistics Table:', 'headers': headers, 'content': content})
        
    return txt_files