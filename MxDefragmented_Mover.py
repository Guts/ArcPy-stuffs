# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        MXDefragmented_Mover
# Purpose:     Move all MXD files whch have been defragmented with the ArcGIS
#              tool
#
# Author:      Julien
#
# Created:     01/04/2013
#-------------------------------------------------------------------------------

from os import path, walk, mkdir, rename
from shutil import move

orig = 'D:/'
dest = path.join(orig, 'MXD_Defragmented')
mkdir(dest)


for root, dirs, files in walk(orig):
    for fic in files:
        if '.mxd.old' in path.basename(fic) and not 'MXD_Defragmented' in root:
            try:
                move(path.join(root, fic), dest)
            except:
                old = path.join(root, fic)
                new = path.join(root, path.basename(root) + '_' + fic)
                rename(old, new)
                move(new, dest)



