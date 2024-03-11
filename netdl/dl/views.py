from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import random
import requests

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

@csrf_exempt
@api_view(['Get'])
def get(request):
  #/////////////////////////////////////////////////////
  second_service_url = "http://localhost:8088/async_task"
  percent_drop_segment=2
  percent_error=11
  #/////////////////////////////////////////////////////
  print(request.data.get('time'),request.data.get('segment_num'),'!!!!принял')
  drop_segment=random.choices([True,False],weights=[percent_drop_segment,100-percent_drop_segment]) 
  if not drop_segment[0]:
    segment_data=request.data.get('segment_data')
    print(segment_data)
    segment_bin=text_to_bits(segment_data)
    segment_bin_after=''
    for i in range(0,len(segment_bin),4):
      error_code=random.choices([True,False],weights=[percent_error,100-percent_error])
      code4=segment_bin[i:i+4]
    segment_data_after=''
    data = {
        'segment_data': segment_data_after,
        'time': request.data.get('time'),
        'segment_len':request.data.get('segment_len'),
        'segment_num':request.data.get('segment_num')
    }
    '''
    answ = requests.post(second_service_url, data=data) # ПРОВЕРИТЬ ТИП МЕТОДА
    if answ.status_code == 200:
      print(request.data.get('time'),request.data.get('segment_num'),'отправлен!!!!!')
    else:
       print('!!!!!!!!!!!!!!!!Не доходит!!!!!!!!!!!!!!!')
    '''

    if segment_data==segment_data_after:
       print('целый')
    else:
       print('битый')
    return Response(status=status.HTTP_200_OK)
  print(request.data.get('time'),request.data.get('segment_num'),'дроп!!!!!')
  return Response(status=status.HTTP_200_OK)