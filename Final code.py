from watson_developer_cloud import VisualRecognitionV3
import json
import os
import shutil
from shutil import copyfile

# ** Configuration **

# Watson configuration
visual_recognition = VisualRecognitionV3(
	version = '2018-03-19',
    url = 'https://gateway.watsonplatform.net/visual-recognition/api',
	iam_apikey = 'x x x'
)

# Base directory
basedir = os.path.dirname(_file_) + "/images"

# Destination directory
destdir = os.path.dirname(_file_) + "/output"

# Remove direcory output if it exists
if os.path.isdir(destdir):
    shutil.rmtree(destdir)

# Create output directories
os.mkdir(destdir)
os.mkdir(destdir + "/FEMALE")
os.mkdir(destdir + "/MALE")

# For each jpg in directory 'images'
for file in os.listdir(basedir):
    if file.endswith(".JPG"):
        face_path = os.path.join(basedir, file)
        print("----> " + face_path)

        with open(face_path, 'rb') as image_file:
            face_result = visual_recognition.detect_faces(images_file=image_file).get_result()
            print(json.dumps(face_result, indent=2))

            # For each image
            for img in face_result["images"]:

                for face in img["faces"]:
                    print(face)

                    if face["gender"]["score"] > .5:
                        gender = face["gender"]["gender"]
                        destfile = destdir + "/" + gender + "/" + file
                        copyfile(face_path, destfile)
