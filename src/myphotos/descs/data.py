#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Gets and sets the latitude and longitude data

    ASSUMPTIONS:
        No assumptions to note

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import math
import os
import re

import piexif
from PIL import Image

# -----------------------------------------------


def main(source):
    """
    Sets the photo filename to that of the exif date
    :param source: String, the source directory
    """

    # -------------------------------------------

    def progress_append(text):
        """ Prints and adds the progress string to the progress list """
        print(text)
        progress.append(text)

    # -------------------------------------------

    progress = ['Running Descriptions\n']

    # ---

    for root, _, files in os.walk(source):
        path = root[len(source):].strip('\\').strip('/')
        progress_append(f'\nProcessing Directory: {path}')

        description = os.path.basename(root)
        if re.match(r'^[\d|\-\~]* ', description):
            description = description.split(' ', 1)[1]
        progress_append(f'Description: {description}')
        description = description.encode('UTF-8')

        for i in [img for img in files if img.upper().endswith('.JPG') or img.upper().endswith('.JPEG')]:

            progress_append(f'Processing: {i}')
            file_path = os.path.join(root, i)

            if i.upper().endswith('.JPG') or i.upper().endswith('.JPEG'):
                img = Image.open(file_path)
                try:
                    exif_dict = piexif.load(img.info['exif'])
                    progress_append('.. Exif data found')
                except KeyError:
                    progress_append('.. Exif not found')
                    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
                # ---
                if '0th' not in exif_dict:
                    progress_append('.. Creating 0th')
                    exif_dict['0th'] = {piexif.ImageIFD.ImageDescription: description}
                elif (piexif.ImageIFD.ImageDescription not in exif_dict['0th']
                      or not exif_dict['0th'][piexif.ImageIFD.ImageDescription]):
                    exif_dict['0th'][piexif.ImageIFD.ImageDescription] = description
                else:
                    progress_append('.. Description exists')
                    continue

                exif_bytes = piexif.dump(exif_dict)
                img.save(file_path, exif=exif_bytes)
                img.close()
                progress_append('.. Updated description')

            yield progress
            progress = []

    yield progress


# -----------------------------------------------

if __name__ == '__main__':
    _sd = input('Enter source directory:')
    for _i, _ in enumerate(main(_sd)):
        print(f'--- Loop {_i} ---')

# -----------------------------------------------
# End.
