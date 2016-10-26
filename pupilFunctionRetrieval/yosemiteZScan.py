#!/usr/bin/python
#
## @file
#
# Stage control for Yosemite.
#
# Hazen 04/12
# RJM: 1/15 -- switch from Marzhauser to ASI
#

from PyQt4 import QtCore

# stage.
import asi.asi as asi


# scan control
import pupilFunctionRetrieval.zscan as zscan

#
# Stage control dialog specialized for Storm4
# with RS232 Marzhauser motorized stage.
#
class AZScan(zscan.ZScan):
    def __init__(self, hardware, parameters, parent = None):
        #stage = asi.ASI_RS232("COM29", wait_time = 0.05)
        zscan.ZScan.__init__(self, hardware, parameters, parent)
