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

import os, os.path

def getPyphantPath(subdir = '/'):
    """
    returns full pyphant path with optional subdirectory
    subdir -- subdirectory that is created if it does not exist already,
              recursive creation of directories is supported also.
    """
    homedir = os.path.expanduser('~')
    if not subdir.startswith('/'):
        subdir = '/' + subdir
    if not subdir.endswith('/'):
        subdir = subdir + '/'
    if homedir == '~':
        homedir = os.getcwdu()
    plist = ('/.pyphant' + subdir).split('/')
    makedir = homedir
    path = homedir + '/.pyphant' + subdir
    for p in plist:
        if p != '':
            makedir += "/%s" % (p, )
            if not os.path.isdir(makedir):
                os.mkdir(makedir)
    return path

def getUsername():
    enc = lambda s: unicode(s, "utf-8")
    import platform
    pltform = platform.system()
    if pltform == 'Linux' or pltform == 'Darwin':
        user = enc(os.environ['LOGNAME'])
    elif pltform == 'Windows':
        try:
            user = enc(os.environ['USERNAME'])
        except:
            user = u"Unidentified User"
    else:
        raise NotImplementedError, "Unsupported Platform %s" %pltform
    return user

def getMachine():
    import socket
    return unicode(socket.getfqdn(), 'utf-8')

def enableLogging():
    """
    Enables logging to stdout for debug purposes.
    """
    l = logging.getLogger("pyphant")
    l.setLevel(logging.DEBUG)
    f = logging.Formatter('%(asctime)s [%(name)s|%(levelname)s] %(message)s')
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(f)
    l.addHandler(h)
    l.info("Logger 'pyphant' has been configured for debug purposes.")
