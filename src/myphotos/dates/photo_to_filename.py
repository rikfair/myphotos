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
    mov_files = []
    non_photos = os.path.join(target, f'{myphotos.NON_PHOTOS}{now}')
    progress = ['Running Photo to Filename\n']
    files = sorted(os.listdir(source))  # Ensures jpg comes before mov, for the iOS live files.

    for i in files:
        progress_append(f'Processing: {i}')
        source_file = os.path.join(source, i)

        if i.upper().endswith('.JPG') or i.upper().endswith('.JPEG'):
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
                if not os.path.isdir(target_path):
                    os.makedirs(target_path)
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
                # ---
                # Check for iOS live mov file
                mov_file = i.rsplit('.', 1)[0] + '.MOV'  # Assumes uppercase if not Windows
                if mov_file in files:
                    progress_append('.. Mov file found')
                    shutil.copy(os.path.join(source, mov_file), os.path.join(target_path, f'{exif_date}.mov'))
                    mov_files.append(mov_file)
                # ---

            except KeyError:
                progress_append('.. Exif not found')
                if not os.path.isdir(errors):
                    os.makedirs(errors)
                shutil.copy(source_file, os.path.join(errors, i))
                progress_append('.. Copied to errors')

            finally:
                img.close()
                del img

        elif i in mov_files:
            progress_append('.. Mov file already processed')

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
