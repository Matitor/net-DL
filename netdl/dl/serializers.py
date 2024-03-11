from dl.models import *
from rest_framework import serializers
import base64

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return value.decode('utf-8')

    def to_internal_value(self, value):
        return value.encode('utf-8')
class SegmentSer(serializers.ModelSerializer):
  class Meta:
    model = Segment
    fields = ('segment_data', 'time', 'segment_len', 'segment_num')
  segment_data = BinaryField()