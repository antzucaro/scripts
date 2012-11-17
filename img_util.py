import sys
from glob import glob
from os import stat, rename
from os.path import splitext
from PIL import Image
from PIL.ExifTags import TAGS
from time import strptime, mktime

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    exif = i._getexif()
    for key, value in exif.items():
        decoded = TAGS.get(key, key)
        ret[decoded] = value

    return ret


def get_ctime(fn):
    try:
        exif_info = get_exif(fn)
        time = mktime(strptime(exif_info['DateTime'], '%Y:%m:%d %H:%M:%S'))
    except:
        time = stat(fn).st_ctime

    return time


def get_caption(fn):
    try:
        exif_info = exif(fn)
        caption = exif_info['UserComment']
        if caption.startswith('ASCII\x00\x00\x00'):
            caption = caption.replace('ASCII\x00\x00\x00', '')
    except:
        caption = ""

    return caption


def get_image_filenames(get_jpgs=True, get_nefs=True):
    images =  []
    
    if get_jpgs:
        jpgs = glob('*.[jJ][pP][gG]')
        if len(jpgs) > 0:
            images += jpgs

    if get_nefs:
        nefs = glob('*.[nN][eE][fF]')
        if len(nefs) > 0:
            images += nefs

    return images


def get_images_sorted_by_ctime():
    images = []
    for fn in get_image_filenames():
        images.append({'filename':fn, 'ctime':get_ctime(fn)})

    images = sorted(images, key=lambda image: image['ctime'])

    return images


def rename_image(fn, prefix, suffix=0):
    basename, ext = splitext(fn)
    new_fn = "{0}_{1:03d}{2}".format(prefix, suffix, ext)
    print "Renaming {0} to {1}".format(fn, new_fn)
    rename(fn, new_fn)
