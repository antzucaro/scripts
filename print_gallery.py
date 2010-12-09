#!/usr/bin/python

import sys
import glob

files = glob.glob('*.[jJ][pP][gG]')
files.sort()
prefix = sys.argv[1]

print '<html>'
print '<head></head>'
print '<body>'
print '<div class="imgblock">'

for file in files:
    print '    <a rel="cbimage" href="/%s/%s"><img src="/%s/thumb/%s"/></a>' % (prefix, file, prefix, file)

print '</div>'
print '</body>'
print '</html>'
