#!/usr/bin/python3
# -----------------------------------------------
"""
    DESCRIPTION:
        Checks all files in a directory and sub-directories are as expected.

    ASSUMPTIONS:
        No assumptions to note

    ACCURACY:
        No accuracy issues to note
"""
# -----------------------------------------------

import os
import re

import piexif
from PIL import Image

# -----------------------------------------------


def main(source):
    """
    Sets the photo date exif value to that of the filename
    :param source: String, the source directory
    """

    # -------------------------------------------

    def progress_append(text):
        """ Prints and adds the progress string to the progress list """
        print(text)
        progress.append(text)

    # -------------------------------------------

    def add_issue(issue):
        """ Adds a message to the issues """
        issues.append(f'[{path}/{i}] {issue}')
        progress_append(f'.. {issue}')

    # -------------------------------------------

    issues = []

    progress = ['Running File Check\n']
    re_filename = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}#?\d*.([jpe?g]|mov|mp4)', re.IGNORECASE)

    for root, _, files in os.walk(source):
        path = root[len(source):].strip('\\').strip('/')
        progress_append(f'\nProcessing Directory: {path}')

        for i in files:
            progress_append(f'Processing File: {i}')

            # ---

            ext = i.upper().rsplit('.', 1)[1]
            if ext not in ['JPG', 'JPEG', 'MOV', 'MP4']:
                add_issue('Error with filename')
                continue

            # ---

            if not re.match(re_filename, i):
                add_issue('Invalid filename')
                continue

            # ---

            if ext in ['MOV', 'MP4']:
                continue  # End of the road for non-photos

            # ---

            source_file = os.path.join(root, i)
            img = Image.open(source_file)
            try:
                exif_dict = piexif.load(img.info['exif'])
                progress_append('.. Exif data found')
            except KeyError:
                add_issue('No exif data')
                continue

            # ---

            exif_date = str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
            exif_date = exif_date[2:21].replace(':', '-').replace(' ', 'T')

            if not i.startswith(exif_date):
                add_issue(f'Filename != date: {exif_date}')
                continue

            # ---

            try:
                if not exif_dict['0th'][piexif.ImageIFD.ImageDescription]:
                    add_issue('No image description')
                    continue
            except KeyError:
                add_issue('No image description element')
                continue

            # ---

            try:
                latitude = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]
                longitude = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]
                if latitude and longitude:
                    progress_append(f'.. Geo found: {latitude}, {longitude}')
                else:
                    add_issue('No latitude and longitude')
            except KeyError:
                add_issue('No geo data')
                continue

        yield progress
        progress = []

    yield ['-' * 50, 'Issues:', '', *issues] if issues else ['-' * 50, 'No issues']


# -----------------------------------------------

if __name__ == '__main__':
    _sd = input('Enter source directory:')
    for _i, _ in enumerate(main(_sd)):
        print(f'--- Loop {_i} ---')

# -----------------------------------------------
# End.
