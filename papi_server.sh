#!/bin/bash

# nome do computador
HOST=`hostname`

# diretório de execução
cd ~/Public/mkr/papi/srce/papi_calibra
# diretório de sketchs
cd sketchbook
# carrega o sketch no arduino
./upino.sh papi_sensors

cd ..
# envia dados
/usr/bin/env python ./papi_senders.py 2> ./papi_senders.$HOST.log &
