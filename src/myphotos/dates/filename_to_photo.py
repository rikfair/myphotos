#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Takes the filename and sets the photos date

    ASSUMPTIONS:
        The filename is in the format %Y-%m-%sT%H-%M-%S

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import datetime
import os
import shutil

import piexif
from PIL import Image

import myphotos

# -----------------------------------------------


def main(source, target):
    """
    Sets the photo date exif value to that of the filename
    :param source: String, the source directory
    :param target: String, the target directory
    """

    # -------------------------------------------

    def progress_append(text):
        """ Prints and adds the progress string to the progress list """
        print(text)
        progress.append(text)

    # -------------------------------------------

    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    non_photos = os.path.join(target, f'{myphotos.NON_PHOTOS}{now}')
    progress = ['Running Filename to Photo\n']

    for i in os.listdir(source):
        progress_append(f'Processing: {i}')
        source_file = os.path.join(source, i)
        target_file = os.path.join(target, i[2:10], i)

        if i.upper().endswith('.JPG') or i.upper().endswith('.JPEG'):
            img = Image.open(source_file)
            try:
                exif = piexif.load(img.info['exif'])
            except KeyError:
                progress_append('.. No exif found')
                exif = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
            try:
                progress_append(f".. Old date: {exif['Exif'][piexif.ExifIFD.DateTimeOriginal]}")
            except KeyError:
                progress_append('.. Old date not found')
            new_date = i[0:19].replace('-', ':').replace('T', ' ')
            progress_append(f'.. New date: {new_date}')
            exif['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
            exif_bytes = piexif.dump(exif)
            if not os.path.isdir(os.path.dirname(target_file)):
                os.makedirs(os.path.dirname(target_file))
            img.save(target_file, exif=exif_bytes)
            img.close()
            progress_append('.. Saved')
        else:
            progress_append('.. Non image file')
            if not os.path.isdir(non_photos):
                os.makedirs(non_photos)
            shutil.copy(source_file, os.path.join(non_photos, i))
            progress_append('.. Copied')

        yield progress
        progress = []


# -----------------------------------------------

if __name__ == '__main__':
    _sd = input('Enter source directory:')
    _td = input('Enter target directory:')
    for _i, _ in enumerate(main(_sd, _td)):
        print(f'--- Loop {_i} ---')

# -----------------------------------------------
# End.
