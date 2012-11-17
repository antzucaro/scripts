#!/usr/bin/python2

import datetime
import glob
import os
import shutil
import sys
from PIL import Image
from img_util import *

now = datetime.datetime.now()

C_L_SIZE = 1000
C_M_SIZE = 650
C_T_SIZE = 100
PANO_L_SIZE = 1600
PANO_M_SIZE = 650

# folder to place the images
directory = sys.argv[1]

MEDIA_ROOT='/home/ant/Documents/media.antzucaro.com/uploads'
MEDIA_DEST='{0}/{1}/{2}/'.format(MEDIA_ROOT, now.strftime('%Y/%m'), directory)
WEB_ROOT='http://media.antzucaro.com/uploads'
WEB_DEST='{0}/{1}/{2}/'.format(WEB_ROOT, now.strftime('%Y/%m'), directory)

# all of the images in the current directory
dir_images = glob("*.[jJ][pP][gG]")
dir_images.sort()

# open up a file for the output
of = open('gallery.html', 'w')

for image in dir_images:
    # open it up so we can get at the meta info
    img = Image.open(image)

    (width, height) = img.size
    if width > height:
        if width > 4000:
            l_option = "{0}x".format(PANO_L_SIZE)
            m_option = "{0}x".format(PANO_M_SIZE)
            #t_option = "{0}x".format(C_T_SIZE)
        else:
            l_option = "{0}x".format(C_L_SIZE)
            m_option = "{0}x".format(C_M_SIZE)
            #t_option = "{0}x".format(C_T_SIZE)
    else:
        if height > 4000:
            l_option = "x{0}".format(PANO_L_SIZE)
            m_option = "x{0}".format(PANO_M_SIZE)
            #t_option = "x{0}".format(C_T_SIZE)
        else:
            l_option = "x{0}".format(C_L_SIZE)
            m_option = "x{0}".format(C_M_SIZE)
            #t_option = "x{0}".format(C_T_SIZE)

    # split on the dot
    prefix = image[0:image.find('.')]
    suffix = image[image.find('.'):]

    # set up the image names
    l_fn = prefix + '_l' + suffix
    m_fn = prefix + '_m' + suffix
    #t_fn = prefix + '_t' + suffix

    # resize
    os.system("convert -resize {0} {1} {2}".format(l_option, image, l_fn))
    os.system("convert -resize {0} -quality 65 {1} {2}".format(m_option, l_fn, m_fn))
    #os.system("convert -resize {0} {1} {2}".format(t_option, l_fn, t_fn))

    # get the image sizes
    (l_width, l_height) = Image.open(l_fn).size
    (m_width, m_height) = Image.open(m_fn).size
    #(t_width, t_height) = Image.open(t_fn).size

    # grab captions
    m_img = Image.open(m_fn)
    m_img.show()
    caption = raw_input('Caption: ')
    #caption = get_caption(m_fn)

    os.system('mkdir -p {0}'.format(MEDIA_DEST))

    # move the files to their destination
    os.system('mv {0} {1}'.format(l_fn, MEDIA_DEST))
    os.system('mv {0} {1}'.format(m_fn, MEDIA_DEST))
    #os.system('mv {0} {1}'.format(t_fn, MEDIA_DEST))

    # urls
    l_url = '{0}{1}'.format(WEB_DEST, l_fn)
    m_url = '{0}{1}'.format(WEB_DEST, m_fn)
    #t_url = '{0}{1}'.format(WEB_DEST, t_fn)

    # print out the img tags and such
    # of.write("<div class='thumbnail'>\n")
    # of.write("  <a href='{0}' title='{1}'><img alt='{2}' src='{3}'></a>\n".format(l_url, caption, caption, m_url))
    # of.write("  <div class='thumbnail'>\n")
    # of.write("    <p>{0}</p>\n".format(caption))
    # of.write("  </div>")
    # of.write("</div>")

    of.write("<div class='wp-caption aligncenter' style='width: {0}px; margin-left: auto; margin-right: auto;'>\n".format(m_width+10))
    of.write("""  <a href="{0}" title="{1}">\n""".format(l_url, caption))
    of.write("""    <img width='{0}px' height='{1}px' alt="{2}" title="{3}" src='{4}'>\n""".format(m_width, m_height, caption, caption, m_url))
    of.write("""  </a>\n""")
    of.write("""    <p class='wp-caption-text'>{0}</p>\n""".format(caption))
    of.write("</div>\n\n")

of.close()
