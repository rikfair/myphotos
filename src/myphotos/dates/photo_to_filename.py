#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Takes the filename and sets the photos date

    ASSUMPTIONS:
        No assumptions to note

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

# -----------------------------


def main(source, target):
    """
    Sets the photo filename to that of the exif date
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
    errors = os.path.join(target, f'{myphotos.ERRORS}{now}')
    non_photos = os.path.join(target, f'{myphotos.NON_PHOTOS}{now}')

    for i in os.listdir(source):
        progress = []
        progress_append(f'Processing: {i}')
        source_file = os.path.join(source, i)

        if (i.upper().endswith('.JPG')) or (i.upper().endswith('.JPEG')):
            img = Image.open(source_file)
            try:
                exif_dict = piexif.load(img.info['exif'])
                progress_append('.. Exif data found')
                # ---
                exif_date = str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
                exif_date = exif_date[2:21].replace(':', '-').replace(' ', 'T')
                # ---
                photo_no = 0
                target_path = os.path.join(target, exif_date[2:10])
                target_file = os.path.join(target_path, f'{exif_date}.jpg')
                while os.path.isfile(target_file):
                    photo_no += 1
                    target_file = os.path.join(target_path, f'{exif_date}#{photo_no}.jpg')
                progress_append(f'.. Creating "{target_file}"')
                # ---
                try:
                    make_value = exif_dict['0th'][piexif.ImageIFD.Make]
                    progress_append(f'.. Found make data: {make_value}')
                except KeyError:
                    progress_append('.. Creating make data')
                    exif_dict['0th'][piexif.ImageIFD.Make] = 'Unknown'
                # ---
                exif_bytes = piexif.dump(exif_dict)
                img.save(target_file, exif=exif_bytes)

            except KeyError:
                progress_append('.. Exif not found')
                if not os.path.isdir(errors):
                    os.makedirs(errors)
                shutil.copy(source_file, os.path.join(errors, i))
                progress_append('.. Copied to errors')

            finally:
                img.close()
                del img

        else:
            progress_append('.. Non image file')
            if not os.path.isdir(non_photos):
                os.makedirs(non_photos)
            shutil.copy(source_file, os.path.join(non_photos, i))
            progress_append('.. Copied')

        yield progress


# -----------------------------------------------

if __name__ == '__main__':
    main(input('Enter source directory:'), input('Enter target directory:'))

# -----------------------------------------------
# End.
