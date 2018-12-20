#!/usr/bin/env python

# Copyright (c) 2018, DIANA-HEP
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

import sys
import numbers
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

import numpy

class Check(object):
    def __init__(self, classname, paramname, required):
        self.classname = classname
        self.paramname = paramname
        self.required = required

    def __repr__(self):
        return "<{0} {1}.{2} at 0x{3:012x}>".format(type(self).__name__, self.classname, self.paramname, id(self))

    def __call__(self, obj):
        if obj is None and self.required:
            raise TypeError("{0}.{1} is required, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
        else:
            return obj

    def fromflatbuffers(self, obj):
        return obj

class CheckBool(Check):
    def __call__(self, obj):
        super(CheckBool, self).__call__(obj)
        if obj is None:
            return obj
        elif not isinstance(obj, (bool, numpy.bool_, numpy.bool)):
            raise TypeError("{0}.{1} must be boolean, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
        return bool(obj)

class CheckString(Check):
    def __call__(self, obj):
        super(CheckString, self).__call__(obj)
        if obj is None:
            return obj
        elif not ((sys.version_info[0] >= 3 and isinstance(obj, str)) or (sys.version_info[0] < 3 and isinstance(obj, basestring))):
            raise TypeError("{0}.{1} must be a string, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
        else:
            return obj

class CheckNumber(Check):
    def __init__(self, classname, paramname, required, min=float("-inf"), max=float("inf"), min_inclusive=True, max_inclusive=True):
        super(CheckNumber, self).__init__(classname, paramname, required)
        self.min = min
        self.max = max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def __call__(self, obj):
        super(CheckNumber, self).__call__(obj)
        if obj is None:
            return obj
        elif not isinstance(obj, (numbers.Real, numpy.floating, numpy.integer)) or numpy.isnan(obj):
            raise TypeError("{0}.{1} must be a number, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
        elif self.min_inclusive and not self.min <= obj:
            raise TypeError("{0}.{1} must not be below {2} (inclusive), cannot pass {3}".format(self.classname, self.paramname, self.min, repr(obj)))
        elif not self.min_inclusive and not self.min < obj:
            raise TypeError("{0}.{1} must not be below {2} (exclusive), cannot pass {3}".format(self.classname, self.paramname, self.min, repr(obj)))
        elif self.max_inclusive and not obj <= self.max:
            raise TypeError("{0}.{1} must not be above {2} (inclusive), cannot pass {3}".format(self.classname, self.paramname, self.max, repr(obj)))
        elif not self.max_inclusive and not obj < self.max:
            raise TypeError("{0}.{1} must not be above {2} (exclusive), cannot pass {3}".format(self.classname, self.paramname, self.max, repr(obj)))
        else:
            return float(obj)

class CheckInteger(Check):
    def __init__(self, classname, paramname, required, min=float("-inf"), max=float("inf")):
        super(CheckInteger, self).__init__(classname, paramname, required)
        self.min = min
        self.max = max

    def __call__(self, obj):
        super(CheckInteger, self).__call__(obj)
        if obj is None:
            return obj
        elif not isinstance(obj, (numbers.Integral, numpy.integer)):
            raise TypeError("{0}.{1} must be an integer, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
        elif not self.min <= obj:
            raise TypeError("{0}.{1} must not be below {2} (inclusive), cannot pass {3}".format(self.classname, self.paramname, self.min, repr(obj)))
        elif not obj <= self.max:
            raise TypeError("{0}.{1} must not be above {2} (inclusive), cannot pass {3}".format(self.classname, self.paramname, self.max, repr(obj)))
        else:
            return int(obj)

class CheckEnum(Check):
    def __init__(self, classname, paramname, required, choices):
        super(CheckEnum, self).__init__(classname, paramname, required)
        self.choices = choices

    def __call__(self, obj):
        super(CheckEnum, self).__call__(obj)
        if obj is None:
            return obj
        elif obj not in self.choices:
            raise TypeError("{0}.{1} must be one of {2}, cannot pass {3}".format(self.classname, self.paramname, self.choices, repr(obj)))
        else:
            return self.choices[self.choices.index(obj)]

    def fromflatbuffers(self, obj):
        return self.choices[obj]

class CheckClass(Check):
    def __init__(self, classname, paramname, required, type):
        super(CheckClass, self).__init__(classname, paramname, required)
        self.type = type

    def __call__(self, obj):
        super(CheckClass, self).__call__(obj)
        if obj is None:
            return obj
        elif not isinstance(obj, self.type):
            raise TypeError("{0}.{1} must be a {2} object, cannot pass {3}".format(self.classname, self.paramname, self.type, repr(obj)))
        return obj

    def fromflatbuffers(self, obj):
        return self.type._fromflatbuffers(obj)

class CheckKey(Check):
    def __init__(self, classname, paramname, required, type):
        super(CheckKey, self).__init__(classname, paramname, required)
        self.type = type

    def __call__(self, obj):
        super(CheckKey, self).__call__(obj)
        if obj is None:
            return obj
        elif self.type is str:
            if not ((sys.version_info[0] >= 3 and isinstance(obj, str)) or (sys.version_info[0] < 3 and isinstance(obj, basestring))):
                raise TypeError("{0}.{1} must be a string, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
            return obj
        elif self.type is float:
            if not isinstance(obj, (numbers.Real, numpy.floating, numpy.integer)):
                raise TypeError("{0}.{1} must be a number, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
            return float(obj)
        elif self.type is int:
            if not isinstance(obj, (numbers.Integral, numpy.integer)):
                raise TypeError("{0}.{1} must be an integer, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
            return int(obj)
        else:
            if not isinstance(obj, self.type):
                raise TypeError("{0}.{1} must be a {2} object, cannot pass {3}".format(self.classname, self.paramname, self.type, repr(obj)))
            return obj

    def fromflatbuffers(self, obj):
        if self.type is str or self.type is float or self.type is int:
            return obj
        else:
            return self.type._fromflatbuffers(obj)

class CheckVector(Check):
    def __init__(self, classname, paramname, required, type, minlen=0, maxlen=float("inf")):
        super(CheckVector, self).__init__(classname, paramname, required)
        self.type = type
        self.minlen = minlen
        self.maxlen = maxlen

    def __call__(self, obj):
        super(CheckVector, self).__call__(obj)
        if obj is None:
            return obj
        elif not isinstance(obj, Iterable):
            raise TypeError("{0}.{1} must be iterable, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))

        if not self.minlen <= len(obj) <= self.maxlen:
            raise TypeError("{0}.{1} length must be between {2} and {3} (inclusive), cannot pass {4}".format(self.classname, self.paramname, self.minlen, self.maxlen, repr(obj)))

        if self.type is str:
            for x in obj:
                if not ((sys.version_info[0] >= 3 and isinstance(x, str)) or (sys.version_info[0] < 3 and isinstance(x, basestring))):
                    raise TypeError("{0}.{1} elements must be strings, cannot pass {2}".format(self.classname, self.paramname, repr(x)))
            return list(obj)
        elif isinstance(self.type, list):
            for x in obj:
                if not x in self.type:
                    raise TypeError("{0}.{1} elements must be one of {2}, cannot pass {3}".format(self.classname, self.paramname, self.type, repr(x)))
            return [self.type[self.type.index(x)] for x in obj]
        else:
            for x in obj:
                if not isinstance(x, self.type):
                    raise TypeError("{0}.{1} elements must be {2} objects, cannot pass {3}".format(self.classname, self.paramname, self.type, repr(x)))
            return list(obj)

    def fromflatbuffers(self, obj):
        if self.type is str or self.type is float or self.type is int:
            return list(obj)
        else:
            return [self.type._fromflatbuffers(x) for x in obj]

class CheckBuffer(Check):
    def __call__(self, obj):
        super(CheckBuffer, self).__call__(obj)
        if obj is None:
            return obj
        try:
            return numpy.frombuffer(obj, dtype=numpy.uint8)
        except AttributeError:
            raise TypeError("{0}.{1} must be a buffer, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))

class CheckSlice(Check):
    def __call__(self, obj):
        super(CheckSlice, self).__call__(obj)
        if obj is None:
            return obj
        elif not isinstance(obj, slice):
            raise TypeError("{0}.{1} must be a slice, cannot pass {2}".format(self.classname, self.paramname, repr(obj)))
        return out

    def fromflatbuffers(self, obj):
        return slice(obj.Start() if obj.HasStart() else None, obj.Stop() if obj.HasStop() else None, obj.Step() if obj.HasStep() else None)
