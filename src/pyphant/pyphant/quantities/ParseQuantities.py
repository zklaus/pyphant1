# -*- coding: utf-8 -*-

# Copyright (c) 2008-2009, Rectorate of the University of Freiburg
# Copyright (c) 2009-2011, Andreas W. Liehr (liehr@users.sourceforge.net)
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

import mx.DateTime.ISO
from pyphant.quantities import Quantity
from pyphant.quantities.PhysicalQuantities import PhysicalQuantity

import logging
_logger = logging.getLogger("pyphant")

#Estimate floating point accuracy
ACCURACY = 1.0 -0.1 -0.1 -0.1 -0.1 -0.1 -0.1 -0.1 -0.1 -0.1 -0.1

def str2unit(unitStr,FMFversion='1.1'):
    """The function str2unit returns either a quantity or a float from a given string."""
    # Prepare conversion to quantity
    if unitStr.startswith('.'):
        unitStr = '0'+unitStr
    elif unitStr.endswith('%'):
        try:
            unit = float(unitStr[:-1])/100.0
        except: 
            unit = 0.01
    elif unitStr.endswith('a.u.'):
        try:
            unit = float(unitStr[:-4])
        except:
            unit = 1.0
    elif not (unitStr[0].isdigit() or unitStr[0]=='-'):
        unitStr = '1'+unitStr
    # Convert input to quantity or float
    if FMFversion not in ['1.0','1.1']:
        raise ValueError, 'FMFversion %s not supported.' % FMFversion
    else:
        unitStr = unitStr.replace('^', '**')
        try: #FMFversion=='1.1'
            unit = Quantity(unitStr.encode('utf-8'))
        except:
            unit = None
        if FMFversion=='1.0':
            try:
                unit1_0 = PhysicalQuantity(unitStr.encode('utf-8'))
                unit1_1 = Quantity(str(unit1_0.inBaseUnits()))
            except:
                unit1_1 = None
            
            if (isinstance(unit,Quantity) and
                isinstance(unit1_1,Quantity) and
                not unit.inBaseUnits() == unit1_1):
                try: 
                    diff = unit - unit1_1
                    if diff > ACCURACY:
                        unit = Quantity(str(unit1_0))
                except: 
                    unit = unit1_1
                    _logger.warn('Usage of old unit "%s" required '
                                 'conversion to base units.' % unit1_0)

        if unit == None:
            try:
                unit = float(unit)
            except e:
                raise ValueError, "Unit %s cannot be interpreted." % unit
    return unit

def parseQuantity(value,FMFversion='1.1'):
    import re
    pm = re.compile(ur"(?:\\pm|\+-|\+/-)")
    try:
        value, error = [s.strip() for s in pm.split(value)]
    except:
        error = None
    if value.startswith('('):
        value = float(value[1:])
        error, unit = [s.strip() for s in error.split(')')]
        unit = str2unit(unit,FMFversion)
        value *= unit
    else:
        value = str2unit(value,FMFversion)
    if error != None:
        if error.endswith('%'):
            error = value*float(error[:-1])/100.0
        else:
            try:
                error = float(error)*unit
            except:
                error = str2unit(error,FMFversion)
    return value, error

def parseVariable(oldVal,FMFversion='1.1'):
    shortname, value = tuple([s.strip() for s in oldVal.split('=')])
    value, error = parseQuantity(value,FMFversion)
    return (shortname, value, error)

def parseDateTime(value,FMFversion='1.1'):
    """
    >>>parseDateTime('2004-08-21 12:00:00+-12hr')
    (Quantity(731814.5,'d'), Quantity(0.5,'d'))
    >>>parseDateTime('2004-08-21 12:00:00')
    (Quantity(731814.5,'d'), None)
    """
    datetimeWithError = value.split('+-')
    if len(datetimeWithError)==2:
        datetime = mx.DateTime.ISO.ParseAny(datetimeWithError[0])
        uncertainty = parseQuantity(datetimeWithError[1],FMFversion)[0]
        if uncertainty.isCompatible('h'):
            _logger.warning("The uncertainty of timestamp %s has the unit 'h', which is deprecated. The correct abbreviation for hour is 'hr'." % value)
            uncertainty = uncertainty*Quantity('1hr/h')
        error = uncertainty.inUnitsOf('d')
    else:
        datetime = mx.DateTime.ISO.ParseAny(value)
        error = None
    days,seconds = datetime.absvalues()
    return (Quantity(days,'d')+Quantity(seconds,'s'),error)
