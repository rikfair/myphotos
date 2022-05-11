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

import piexif
from PIL import Image

# -----------------------------------------------


def _get_dd_from_dms(dms, ref):
    """ Converts degrees, minutes, seconds to decimal degrees """

    if dms[0][1] and dms[1][1] and dms[2][1]:
        direction = 1 if ref.decode('ASCII') in ['N', 'E'] else -1

        degrees = dms[0][0] / dms[0][1] * direction
        minutes = dms[1][0] / dms[1][1] / 60 * direction
        seconds = dms[2][0] / dms[2][1] / 3600 * direction

        return round(degrees + minutes + seconds, 5)

    return None


# -----------------------------------------------


def _get_dms_from_dd(dd):
    """ Converts decimal degrees to degree, minute, second format"""

    split_deg = math.modf(abs(dd))
    degrees = int(split_deg[1])
    minutes = int(math.modf(split_deg[0] * 60)[1])
    seconds = int(round((math.modf(split_deg[0] * 60)[0] * 60) * 100, 0))

    return (degrees, 1), (minutes, 1), (seconds, 100)


# -----------------------------------------------


def get_data(source):
    """ Gets the latitude and longitude data from the images in the source directory """

    data = []

    for i in os.listdir(source):

        file_path = os.path.join(source, i)
        img_data = {
            'filename': i,
            'file_path': file_path,
            'coordinates': ''
        }

        if i.upper().endswith('.JPG') and os.path.isfile(file_path):
            print(f'Processing: {i}')
            img = Image.open(file_path)
            try:
                gps = piexif.load(img.info['exif'])['GPS']
                latitude = _get_dd_from_dms(gps[piexif.GPSIFD.GPSLatitude], gps[piexif.GPSIFD.GPSLatitudeRef])
                longitude = _get_dd_from_dms(gps[piexif.GPSIFD.GPSLongitude], gps[piexif.GPSIFD.GPSLongitudeRef])
                img_data['coordinates'] = f'{latitude}, {longitude}'

            except KeyError:
                pass

            img.close()
            data.append(img_data)

    return data


# -----------------------------------------------


def set_data(data):
    pass


# -----------------------------------------------
# End.
