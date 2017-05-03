import logging
from zipfile import ZipFile
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from holoview.scripting import Script
from holoview.imageutils import rgbarray2bytes, bytes2rgbarray

logger = logging.getLogger('HoloView')

class Project:
    """Datastructure for a basic HoloView Project.

    A Project consists of the following components:
      - title
      - author: creator of the project -- Firstname Lastname <email@server.com>
      - description: descriptive text explaining the content/purpose of the project
      - image: a two-dimensional ndarray representing the captured image
      - script: script-object containing the script source code

    Project files have a special file structure:
        project_ab.zip
            └─ script.py
            └─ image.png
            └─ METADATA.txt

    METADATA.txt is a plain text file with the following content:
        <Title>
        created by <author>
        <description>

    """
    def __init__(self, title="", author="", description="", script=Script(), 
                 image=np.empty((0, 0))):
        """Initialize the project
        
        By default, empty values are used"""
        self.title = title
        self.author = author
        self.description = description
        self.script = script
        self.image = image

    def set_title(self, title):
        self.title = title

    def set_author(self, author):
        self.author = author

    def set_description(self, desc):
        self.description = desc

    def set_image(self, image):
        self.image = image

    def set_script(self, script):
        self.script = script

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_description(self):
        return self.description

    def get_script(self):
        return self.script

    def get_image(self):
        return self.image

    def save(self, path):
        """Save the project to a file specified by path."""
        # Prepare the content of METADATA.txt
        metadata = "{}\ncreated by {}\n{}".format(self.title,
                                                  self.author,
                                                  self.description)
        with ZipFile(path, 'w') as zipfile:
            zipfile.writestr('METADATA.txt', metadata)
            sourcecode = self.script.get_source()
            logger.debug('Source of code is {}'.format(sourcecode))
            zipfile.writestr('script.py', self.script.get_source())
            imgData = rgbarray2bytes(self.image, 'PNG')
            zipfile.writestr('image.png', imgData)

    def load(self, path):
        """Load the project from the file specified by path."""
        with ZipFile(path, 'r') as zipfile:
            metadata = zipfile.read('METADATA.txt').decode().split("\n")
            logger.info("metadata: "+str(metadata))
            logger.info("metadata: "+str(len(metadata)))
            if len(metadata) != 3:
                logger.error("Invalid METADATA.txt in project file {}" \
                             .format(path))
                return
            title = metadata[0]
            author = metadata[1][11:]
            desc = metadata[2]
            script_source = zipfile.read('script.py').decode()
            image = bytes2rgbarray(zipfile.read('image.png'))
            
        self.author = author
        self.title = title
        self.description = desc
        self.script.set_source(script_source)
        self.image = image
