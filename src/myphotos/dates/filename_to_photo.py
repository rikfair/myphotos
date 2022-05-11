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
    non_images = os.path.join(target, f'_non_images_{now}')

    for i in os.listdir(source):
        progress = []
        progress_append(f'Processing: {i}')
        source_file = os.path.join(source, i)
        target_file = os.path.join(target, i[2:10], i)

        if (i.upper().endswith('.JPG')) or (i.upper().endswith('.JPEG')):
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
            if not os.path.isdir(non_images):
                os.makedirs(non_images)
            shutil.copy(source_file, os.path.join(non_images, i))

        yield progress


# -----------------------------------------------

if __name__ == '__main__':
    main(input('Enter source directory:'), input('Enter target directory:'))

# -----------------------------------------------
# End.
