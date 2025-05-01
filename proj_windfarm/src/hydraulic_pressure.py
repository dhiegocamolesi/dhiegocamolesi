
import boto3
import json
from random import uniform
import time
from datetime import datetime


cliente = boto3.client('kinesis',aws_access_key_id='MEU ACESSO', aws_secret_access_key='MINHA SENHA',
                       region_name='us-east-1')

id = 0
while True:
  dados = uniform(70,80)
  id += 1;
  registro = {'idtemp' : str(id), 'data' : str(dados), 'type': 'hydraulicpressure', 'timestamp' : str(datetime.now()) }
  cliente.put_record(StreamName='windfarm', Data = json.dumps(registro), PartitionKey='02')
  time.sleep(10)
