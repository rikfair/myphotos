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

        return round(degrees + minutes + seconds, 7)

    return ''


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
    """
    Gets the latitude and longitude data from the images in the source directory
    :param source: String, the source directory
    :return: List, of {filename, file_path, coordinates, description}
    """

    data = []

    for i in os.listdir(source):

        file_path = os.path.join(source, i)
        img_data = {
            'filename': i,
            'file_path': file_path,
            'coordinates': '',
            'description': ''
        }

        if (i.upper().endswith('.JPG') or i.upper().endswith('.JPEG')) and os.path.isfile(file_path):
            print(f'Processing: {i}')
            img = Image.open(file_path)
            try:
                exif_dict = piexif.load(img.info['exif'])
                img_data['description'] = exif_dict.get(
                    '0th', {}).get(piexif.ImageIFD.ImageDescription, b'').decode('UTF-8')
                gps = exif_dict['GPS']
                latitude = _get_dd_from_dms(gps[piexif.GPSIFD.GPSLatitude], gps[piexif.GPSIFD.GPSLatitudeRef])
                longitude = _get_dd_from_dms(gps[piexif.GPSIFD.GPSLongitude], gps[piexif.GPSIFD.GPSLongitudeRef])
                img_data['coordinates'] = f'{latitude}, {longitude}' if latitude or longitude else ''

            except KeyError:
                pass

            img.close()
            data.append(img_data)

    return data


# -----------------------------------------------


def set_data(data):
    """
    Sets the geo for the files which are passed in the data list
    :param data: List, of {filename, file_path, coordinates, description}
    """

    # -------------------------------------------

    def progress_append(text):
        """ Prints and adds the progress string to the progress list """
        print(text)
        progress.append(text)

    # -------------------------------------------

    progress = ['Running Filename to Photo\n']

    for d in data:
        file_path = d['file_path']
        progress_append(f'Processing "{file_path}"...')

        if os.path.isfile(d['file_path']):

            img = Image.open(file_path)
            exif = img.info.get('exif')
            if exif:
                progress_append('... Exif found')
                exif_dict = piexif.load(exif)
                exif_dict['GPS'] = {}
            else:
                exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
            # ---
            if ',' in d['coordinates']:
                geos = d['coordinates'].replace(' ', '').split(',')
                progress_append(f'... Applying coordinates: {geos}')
                latitude_dd = float(geos[0])
                latitude_ref = 'S' if latitude_dd < 0 else 'N'
                latitude_dms = _get_dms_from_dd(latitude_dd)
                longitude_dd = float(geos[1])
                longitude_ref = 'W' if longitude_dd < 0 else 'E'
                longitude_dms = _get_dms_from_dd(longitude_dd)
                # ---
                try:
                    _dto = str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
                except KeyError:
                    progress_append('... Error! No date time original value found')
                    continue
                exif_dict['GPS'][piexif.GPSIFD.GPSDateStamp] = _dto[2:13]
                _smp = (int(_dto[13:15]), 1), (int(_dto[16:18]), 1), (int(_dto[19:21]), 1)
                # ---
                exif_dict['GPS'][piexif.GPSIFD.GPSTimeStamp] = _smp
                exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = latitude_ref
                exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = latitude_dms
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = longitude_ref
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = longitude_dms
                exif_dict['GPS'][piexif.GPSIFD.GPSAltitudeRef] = 1
                exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = (1, 1)
                exif_dict['GPS'][piexif.GPSIFD.GPSSpeedRef] = 'K'
                exif_dict['GPS'][piexif.GPSIFD.GPSSpeed] = (0, 1)
                exif_dict['GPS'][piexif.GPSIFD.GPSHPositioningError] = (1, 1)
                exif_dict['GPS'][piexif.GPSIFD.GPSImgDirectionRef] = 'M'
                exif_dict['GPS'][piexif.GPSIFD.GPSImgDirection] = (0, 1)
                exif_dict['GPS'][piexif.GPSIFD.GPSDestBearingRef] = 'M'
                exif_dict['GPS'][piexif.GPSIFD.GPSDestBearing] = (0, 1)
            else:
                progress_append('... Removing coordinates')

            if piexif.ImageIFD.Make not in exif_dict['0th']:
                exif_dict['0th'][piexif.ImageIFD.Make] = 'Unknown'

            exif_dict['0th'][piexif.ImageIFD.ImageDescription] = d['description'].encode('UTF-8')

            exif_bytes = piexif.dump(exif_dict)
            img.save(file_path, exif=exif_bytes)
            img.close()

        else:
            progress_append('...Unable to locate file')

        yield progress
        progress = []


# -----------------------------------------------
# End.
