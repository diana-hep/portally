# automatically generated by the FlatBuffers compiler, do not modify

# namespace: aghast_generated

import flatbuffers


class Quantiles(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsQuantiles(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Quantiles()
        x.Init(buf, n + offset)
        return x

    # Quantiles
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Quantiles
    def ValuesType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Quantiles
    def Values(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            from flatbuffers.table import Table

            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

    # Quantiles
    def P(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(
                flatbuffers.number_types.Float64Flags, o + self._tab.Pos
            )
        return 0.5

    # Quantiles
    def Weightpower(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # Quantiles
    def Filter(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = o + self._tab.Pos
            from .StatisticFilter import StatisticFilter

            obj = StatisticFilter()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None


def QuantilesStart(builder):
    builder.StartObject(5)


def QuantilesAddValuesType(builder, valuesType):
    builder.PrependUint8Slot(0, valuesType, 0)


def QuantilesAddValues(builder, values):
    builder.PrependUOffsetTRelativeSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(values), 0
    )


def QuantilesAddP(builder, p):
    builder.PrependFloat64Slot(2, p, 0.5)


def QuantilesAddWeightpower(builder, weightpower):
    builder.PrependInt8Slot(3, weightpower, 0)


def QuantilesAddFilter(builder, filter):
    builder.PrependStructSlot(
        4, flatbuffers.number_types.UOffsetTFlags.py_type(filter), 0
    )


def QuantilesEnd(builder):
    return builder.EndObject()
