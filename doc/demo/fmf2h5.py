#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2008, Rectorate of the University of Freiburg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the Freiburg Materials Research Center,
#   University of Freiburg nor the names of its contributors may be used to
#   endorse or promote products derived from this software without specific
#   prior written permission.
#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

u"""usage = "usage: %prog  FMF-archivename"

Load zipped FMF files and persist them in pyphant recipe.
"""

__id__ = "$Id$"
__author__ = "$Author$"
__version__ = "$Revision$"
# $Source$

import pkg_resources
pkg_resources.require("Pyphant")
import pyphant.core.PyTablesPersister
import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("pyphant")

from optparse import OptionParser

parser= OptionParser(__doc__)
(options, args) = parser.parse_args()
archiveName = args[0]
recipeName = args[0][:-3]+'h5'
_logger.info("Importing FMF archive %s into Pyphant recipe %s." % (archiveName,recipeName))

#Load template recipe from hdf file
recipe = pyphant.core.PyTablesPersister.loadRecipeFromHDF5File('fmf2h5.h5')
#Configure FMFLoader
inputWorker = recipe.getWorkers("Load FMF files")[0]
inputWorker.getParam('filename').value = archiveName

sample = inputWorker.plugLoadFMF.getResult()

#Save loaded Data
pyphant.core.PyTablesPersister.saveRecipeToHDF5File( recipe, recipeName )





