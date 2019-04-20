#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_defs

defines e constantes válidas globalmente

revision 0.1  2017/may  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < camera >---------------------------------------------------------------------------------------

# configuração da camera
D_CAM_WIDTH = 320
D_CAM_HEIGHT = 240

# número de frames para estatística
D_CAM_NFRAMES = 120

# < config >---------------------------------------------------------------------------------------

# arquivo de configuração
D_CFG_FILE = "papical.cfg"

# < diretórios >-----------------------------------------------------------------------------------

# diretório de dados
D_DIR_DAT = "data"
# diretório de imagens
D_DIR_IMG = "images"
# diretório de tabelas
D_DIR_TAB = "tabs"

# < mensagens >------------------------------------------------------------------------------------

# versão do conjunto de mensagens
D_MSG_VRS = 1202

# códigos das mensagens
D_MSG_ALT = 1923    # mensagens de altímetro
D_MSG_BAR = 1926    # mensagens de barômetro
D_MSG_GPS = 1929    # mensagens de GPS
D_MSG_THR = 1940    # mensagens de termômetro

D_MSG_IMG = 1961    # mensagens de imagens (frame)
D_MSG_SIZ = 1962    # mensagens de imagens (tamanho)
D_MSG_FPS = 1963    # mensagens de fps

D_MSG_FIM = 1970    # mensagem de fim de execução

# separador de campos na mensagem
D_MSG_SEP = '#'

# mensagens válidas
SET_MSG_VALIDAS = [D_MSG_ALT, D_MSG_BAR, D_MSG_GPS, D_MSG_THR, \
                   D_MSG_IMG, D_MSG_SIZ, D_MSG_FPS, D_MSG_FIM]

# < PAPI >-----------------------------------------------------------------------------------------

# ângulo de transição baixo (caixa 1)
D_ANG_A = 2.50
# ângulo de transição médio-baixo (caixa 2)
D_ANG_B = 2.83
# ângulo de transição médio-alto (caixa 3)
D_ANG_D = 3.17
# ângulo de transição alto (caixa 4)
D_ANG_E = 3.50

# ângulo normal da rampa
D_ANG_C = (D_ANG_B + D_ANG_D) / 2.
# ângulo de altura mínima do olho do piloto
D_ANG_M = D_ANG_B - 0.033
# superfície de proteção de obtáculo
D_ANG_OPS = D_ANG_A - 0.57

# ângulo máximo
D_ANG_MAX = D_ANG_E + 2.

# linhas de transição
D_LINES = ['A', 'B', 'D', 'E']

# distância default (mínima)
D_DFL_DIST = 60.
D_MAX_DIST = 5000.

# tamanho da amostra de calibração
D_SMP_CALIBRA = 120

# < rede >-----------------------------------------------------------------------------------------

# interface de rede
D_NET_IFC = (None, None)  # ("wlan0", "wlan0")

# endereço da ground station
D_NET_GCS = "192.168.0.2"
# endereço do servidor (raspi)
D_NET_SRV = "192.168.0.5"

# arbitrary non-privileged ports

# sensores
D_NET_PORT_ALT = 1923
D_NET_PORT_BAR = 1926
D_NET_PORT_GPS = 1929
D_NET_PORT_THR = 1940

# imagens
D_NET_PORT_IMG = 1961
# comnado/controle/configuração
D_NET_PORT_CCC = 1970

# < serial >---------------------------------------------------------------------------------------

# porta
D_SER_PORT = "/dev/ttyUSB0"
# velocidade
D_SER_BAUD = 57600

# < stylesheet >-----------------------------------------------------------------------------------

D_GBX_STYLE = """QGroupBox { color: white;
                             background-color: rgb(150, 150, 150);
                             border-style: solid;
                             border: 2px solid white;
                             border-radius: 5px;
                             margin-top: 4ex; }

                 QGroupBox::title { background-color: transparent;
                                    subcontrol-origin: margin;
                                    subcontrol-position: top left;
                                    padding: 3 13px;
                                    font-size: 18px;
                                    font-weight: bold; }

                 QGroupBox:focus { border: 2px solid 
                                   QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a); }
"""
# D_GBX_STYLE = ""

D_PTE_STYLE = """QPlainTextEdit { color: white;
                                  background-color: rgb(0, 0, 0);
                                  border: 1px solid rgb(200, 200, 200);
                                  border-style: solid;
                                  border-radius: 5px;}
"""
# D_PTE_STYLE = ""

D_XXX_STYLE = """
                                  margin-top: 4ex; }

                 QPlainTextEdit::title { background-color: transparent;
                                         subcontrol-origin: margin;
                                         subcontrol-position: top left;
                                         padding: 3 13px;
                                         font-size: 18px;
                                         font-weight: bold; }

                 QPlainTextEdit:focus { border: 2px solid 
                                        QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a); }
"""
# < tables >---------------------------------------------------------------------------------------

# tabela de aeródromos
D_TBL_AER = "tabAer"

# < temporização >---------------------------------------------------------------------------------

# tratador de eventos (10Hz) (float)
D_TIM_EVNT = .1
# round-robin (10Hz) (float)
D_TIM_RRBN = .1
# espera de eventos (2Hz) (float)
D_TIM_WAIT = .5

# < vídeo >----------------------------------------------------------------------------------------

# resolução do vídeo
D_VID_HORZ = 640
D_VID_VERT = 480

# < the end >--------------------------------------------------------------------------------------
