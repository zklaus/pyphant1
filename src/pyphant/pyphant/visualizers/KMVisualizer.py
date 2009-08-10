# -*- coding: utf-8 -*-

# Copyright (c) 2006-2008, Rectorate of the University of Freiburg
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

u"""
"""

__id__ = "$Id$"
__author__ = "$Author$"
__version__ = "$Revision$"
# $Source$


from pyphant.core.Connectors import (TYPE_IMAGE, TYPE_ARRAY)
from pyphant.wxgui2.DataVisReg import DataVisReg
from pyphant.core.KnowledgeManager import KnowledgeManager as KM
import webbrowser


class KMVisualizer(object):
    name='Register @ KnowledgeManager'
    def __init__(self, DataContainer, show=True):
        self.DataContainer = DataContainer
        self.show = show
        km = KM.getInstance()
        km.registerDataContainer(DataContainer)
        dc_id = DataContainer.id
        if km.isServerRunning():
            url = 'http://%s:%d/request_dc_details?dcid=%s' % (km._http_host,
                                                               km._http_port,
                                                               dc_id)
            webbrowser.open_new_tab(url)
        else:
            print "ID of registered DC is: " + dc_id


DataVisReg.getInstance().registerVisualizer(TYPE_IMAGE, KMVisualizer)
DataVisReg.getInstance().registerVisualizer(TYPE_ARRAY, KMVisualizer)