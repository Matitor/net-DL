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
def strxor(a,b):
    res=''
    for i,j in zip(a,b):
        if i==j:
            res+='0'
        else:
            res+='1'
    return res
def coder4(segment):
  #/////////////////////////////////
  gen='1011'  
  percent_error=11
  #////////////////////////////////
  segment_bin=text_to_bits(segment)
  segment_bin_after=''
  for i in range(0,len(segment_bin),4):
      error_code=random.choices([True,False],weights=[percent_error,100-percent_error]) #шанс на битый бит
      code=segment_bin[i:i+4]
      code4=code+'000'
      for i in range(4):
        if code4[i]=='1':
          code4=code4[:i]+strxor(code4[i:i+4],gen)+code4[i+4:]
      if error_code[0]:
         randint=random.randint(0,6)
         randbit='0'*7
         randbit=randbit[:randint]+'1'+randbit[randint+1:]
         segment_bin_after+=strxor(code+code4[4:7],randbit)
        # print('in')
      else:   
        segment_bin_after+=code+code4[4:7]
  return segment_bin_after
def encode4(segment):
  gen='1011'  
  sindrom=['001','010','100','011','110','111','101']
  segment_bin_after=''
  for i in range(0,len(segment),7):
    code=segment[i:i+7]
    code7=code
    for i in range(4):
      if code7[i]=='1':
        code7=code7[:i]+strxor(code7[i:i+4],gen)+code7[i+4:]
    #print(code7[4:7])
    if code7[4:7] in sindrom:
      error=sindrom.index(code7[4:7])
      fixbit='0'*7
      fixbit=fixbit[:6-error]+'1'+fixbit[6-error+1:]
      code=strxor(code,fixbit)
      #print('fix in ', error)
    segment_bin_after+=code[0:4]
  return text_from_bits(segment_bin_after)

@csrf_exempt
@api_view(['Get'])
def get(request):
  #/////////////////////////////////////////////////////
  second_service_url = "http://192.168.95.9:8000/transfer/"
  percent_drop_segment=2
  #/////////////////////////////////////////////////////
  print(request.data.get('time'),request.data.get('segment_num'),'!!!!принял')
  drop_segment=random.choices([True,False],weights=[percent_drop_segment,100-percent_drop_segment]) 
  if not drop_segment[0]:
    segment_data=request.data.get('segment_data')
    segment_data_after=encode4(coder4(segment_data))
    data = {
        'segment_data': segment_data_after, #ПОМЕНЯТЬ
        'time': request.data.get('time'),
        'segment_len':request.data.get('segment_len'),
        'segment_num':request.data.get('segment_num')
    }
    
    answ = requests.post(second_service_url, data=data) # ПРОВЕРИТЬ ТИП МЕТОДА
    if answ.status_code == 200:
      print(request.data.get('time'),request.data.get('segment_num'),'отправлен!!!!!')
    else:
       print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Не доходит!!!!!!!!!!!!!!!')
    if segment_data==segment_data_after:
       print('целый')
    else:
       print('битый')
    if segment_data==segment_data_after:
       print('целый')
    else:
       print('битый')
    return Response(status=status.HTTP_200_OK)
  print(request.data.get('time'),request.data.get('segment_num'),'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!дроп!!!!!!!!!!!!!!!!!!!!!!!!')
  return Response(status=status.HTTP_200_OK)