#!/usr/bin/python

import sys
import glob

files = glob.glob('*.[jJ][pP][gG]')
files.sort()
prefix = sys.argv[1]

print '<html>'
print '<head></head>'
print '<body>'
print '<div class="gallery">'

for file in files:
    print '    <a href="http://media.antzucaro.com/galleries/%s/%s"><img src="http://media.antzucaro.com/galleries/%s/thumb/%s"/></a>' % (prefix, file, prefix, file)

print '</div>'
print '</body>'
print '</html>'
