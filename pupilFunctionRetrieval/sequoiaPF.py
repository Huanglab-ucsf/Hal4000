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


# scan control
import pupilFunctionRetrieval.PFRetrieval as PFRetrieval

#
# Stage control dialog specialized for Storm4
# with RS232 Marzhauser motorized stage.
#
class APupilRetrieval(PFRetrieval.PFRetrieval):
    def __init__(self, hardware, parameters, parent = None):
        
        PFRetrieval.PFRetrieval.__init__(self, hardware, parameters, parent)
