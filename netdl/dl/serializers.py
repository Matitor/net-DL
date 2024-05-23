from dl.models import *
from rest_framework import serializers
import base64
from collections import OrderedDict

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return value.decode('utf-8')

    def to_internal_value(self, value):
        return value.encode('utf-8')
class SegmentSer(serializers.ModelSerializer):
  class Meta:
    model = Segment
    fields = ('segment_data', 'time', 'segment_len', 'segment_num')
    def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 