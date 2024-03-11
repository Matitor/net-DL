from django.db import models

class Segment(models.Model):
  segment_data=models.BinaryField(editable = True)
  time=models.DateTimeField()
  segment_len=models.PositiveIntegerField()
  segment_num=models.PositiveIntegerField()
