''' SETTINGS '''

# How many FOVs?
n = 19
m = 11

# How many frames?
n_frames = 1

# How many pixels does your FOV have?
n_pxl = 256

# What is the pixel size (nm)?
pxl_size = 156

# Overlap fraction
f = 0.0

# Which channels to take?
channels = [642]

''' SETTINGS END '''


# A few things to set up:

import sys
import os
import time
import numpy as np
sys.path.append('D:/Programs')
from Utilities import IO

channel_ids = {642: 0,
               561: 1,
               488: 2,
               405: 3,
               'LED': 4}

filenames = {}
for channel in channels:
    control.hal4000.toggleChannel(channel_ids[channel], False)
    filenames[channel] = []

ox0, oy0, oz = control.hal4000.getStagePosition()

d = (1.0-f) * float(pxl_size) * n_pxl / 1000.0

ox = ox0-d*n/2
oy = oy0-d*m/2

# Move stage and take images:

for i in range(n):
    x = ox + i*d

    if control.scripts.stop:
        break

    for j in range(m):
        y = oy + j*d

        if control.scripts.stop:
            break

        # Move stage
        control.hal4000.moveTo((x, y, oz))

        for channel in channels:
            movie_name = 'movie_{0:04d}_{1:04d}_{2}'.format(i+1, j+1, channel)
            control.hal4000.toggleChannel(channel_ids[channel], True)
            control.hal4000.movie(movie_name, 1)
            control.hal4000.toggleChannel(channel_ids[channel], False)
            #sleep.time(0.3)
            filenames[channel].append(movie_name)
            #sleep.time(0.5)

# Move back to original position
control.hal4000.moveTo((ox0, oy0, oz))


# Combining the individual dax images into one:

working_dir = control.hal4000.getWorkingDirectory()

for channel in channels:
    
    sequence = []

    for filename in filenames[channel]:
        success = False
        while success == False:
            if control.scripts.stop:
                break
            try:
                print 'Trying to open file {0}.dax'.format(filename)
                dax = IO.DAX(os.path.join(working_dir, filename))
                success = True
            except WindowsError as error:
                if error[0]==1006:
                    raise
                    #print 'error'
                    time.sleep(0.1)
                else:
                    raise
        sequence.append(dax[0])

    sequence = np.array(sequence)
    filename_mosaic = os.path.join(working_dir, 'mosaic_{0}'.format(channel))
    IO.writeDAX(filename_mosaic, sequence)

'''
# THIS IS BUGGY
# Deleting the original files
for channel in channels:
    for filename in filenames[channel]:
        os.remove(os.path.join(working_dir, filename+'.dax'))
'''


# Generating a table mosaic frame -> xyz stage position
table_file = open(os.path.join(working_dir, 'mosaic_table.txt'), 'w')
table_file.write('Frame\tX\tY\n')
counter = 1
for i in range(n):
    for j in range(m):
        table_file.write('{0}\t{1}\t{2}\n'.format(counter, ox+i*d, oy+j*d))
        counter += 1

