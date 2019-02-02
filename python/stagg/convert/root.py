#!/usr/bin/env python

# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy
try:
    import ROOT
except ImportError:
    raise ImportError("\n\nInstall ROOT package with:\n\n    conda install -c conda-forge root")

from stagg import *

def toroot(obj):
    pass

def tostagg(obj, collection=False):
    if isinstance(obj, ROOT.TH1):
        if isinstance(obj, ROOT.TProfile):
            raise NotImplementedError

        elif isinstance(obj, ROOT.TProfile2D):
            raise NotImplementedError

        elif isinstance(obj, ROOT.TProfile3D):
            raise NotImplementedError

        if not isinstance(obj, (ROOT.TH2, ROOT.TH3):

# >>> numpy.frombuffer(h.fArray, count=102, dtype=numpy.float32)
# array([0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
#        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0.],
#       dtype=float32)
# >>> h.GetNbinsX()

# h = Histogram([Axis(RegularBinning(10, RealInterval(0.1, 10.1)))], UnweightedCounts(InterpretedInlineBuffer.fromarray(numpy.arange(10))))


            if isinstance(obj, ROOT.TH1C):
                array = numpy.frombuffer(obj.fArray, count=obj.fN, dtype=numpy.int8)

            elif isinstance(obj, ROOT.TH1S):
                array = numpy.frombuffer(obj.fArray, count=obj.fN, dtype=numpy.int16)

            elif isinstance(obj, ROOT.TH1I):
                array = numpy.frombuffer(obj.fArray, count=obj.fN, dtype=numpy.int32)

            elif isinstance(obj, ROOT.TH1F):
                array = numpy.frombuffer(obj.fArray, count=obj.fN, dtype=numpy.float32)

            elif isinstance(obj, ROOT.TH1D):
                array = numpy.frombuffer(obj.fArray, count=obj.fN, dtype=numpy.float64)

# h.GetSumw2N()
# sumw2 = h.GetSumw2()
# numpy.frombuffer(sumw2.fArray, count=sumw2.fN, dtype=numpy.float64)



        elif isinstance(obj, ROOT.TH2):
            if isinstance(obj, ROOT.TH2C):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH2S):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH2I):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH2F):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH2D):
                raise NotImplementedError

        elif isinstance(obj, ROOT.TH3):
            if isinstance(obj, ROOT.TH3C):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH3S):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH3I):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH3F):
                raise NotImplementedError

            elif isinstance(obj, ROOT.TH3D):
                raise NotImplementedError

        else:
            raise TypeError("cannot convert {0}".format(type(obj).__name__))

    elif isinstance(obj, ROOT.TTree):
        raise NotImplementedError

    else:
        raise TypeError("cannot convert {0}".format(type(obj).__name__))
