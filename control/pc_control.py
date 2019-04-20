#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
papi calibrate

revision 0.1  2017/abr  mlabru
initial version (Linux/Python)
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import sys
import time

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_data as gdata
import model.pc_model_gcs as mdgcs
import model.pc_model_srv as mdsrv

# view
import view.pc_view_gcs as vgcs
import view.pc_view_srv as vsrv

# control
import control.pc_config as gcfg
import control.pc_net_sender as sender
import control.pc_net_listener as listener
import control.pc_net_sock_in as sockin

# events
import control.events.events_manager as evtmgr
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPAPICalControl >------------------------------------------------------------------------------

class CPAPICalControl(object):
    """
    PAPI Calibra control
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CPAPICalControl, self).__init__()

        # instancia o event manager
        self.__event = evtmgr.CEventsManager()
        assert self.__event

        # registra a sí próprio como recebedor de eventos
        self.__event.register_listener(self)

        # load config
        gcfg.load_config("papical.cfg")

        # create application
        self.create_app("papi_calibra")

        # interface e endereço de rede
        lt_ifc = gdata.G_DCT_CONFIG["net.ifc"]
        ls_adr = gdata.G_DCT_CONFIG["net.adr"]

        # portas
        li_ccc = int(gdata.G_DCT_CONFIG["net.ccc"])

        # create connections
        self.create_connections_gcs(lt_ifc, ls_adr, li_ccc)        
    
        # instancia o modelo
        self.__model = mdgcs.CPAPICalModelGCS(self)
        assert self.__model

        # create view
        self.__view = vgcs.CPAPICalViewGCS(self, self.__model)
        assert self.__view

        # inicia
        gdata.G_KEEP_RUN = True

    # ---------------------------------------------------------------------------------------------
    def create_app(self, fs_name):
        """
        create application
        """
        # create application
        self.__app = QtGui.QApplication(sys.argv)
        assert self.__app

        # setup application parameters
        self.__app.setOrganizationName("sophosoft")
        self.__app.setOrganizationDomain("sophosoft.com.br")
        self.__app.setApplicationName(fs_name)
        
        # load logo
        l_pix_logo = QtGui.QPixmap(":/images/logo_python.png")
        assert l_pix_logo
        
        # create splash screen
        self.__splash = QtGui.QSplashScreen(l_pix_logo, QtCore.Qt.WindowStaysOnTopHint)
        assert self.__splash

        self.__splash.setMask(l_pix_logo.mask())
        
        # show splash screen
        self.__splash.show()

        # process events (before main loop)
        self.__app.processEvents()

    # ---------------------------------------------------------------------------------------------
    def create_connections_gcs(self, ft_ifc, fs_adr, fi_ccc):
        """
        create connections
        """
        # cria a queue de envio de comando/controle/configuração
        self.__q_snd_ccc = multiprocessing.Queue()
        assert self.__q_snd_ccc

        # cria o socket de envio de comando/controle/configuração
        self.__sck_snd_ccc = sender.CNetSender(ft_ifc, fs_adr, fi_ccc, self.__q_snd_ccc)
        assert self.__sck_snd_ccc

        # cria a queue de recebimento de comando/controle/configuração
        self.__q_rcv_ccc = multiprocessing.Queue()
        assert self.__q_rcv_ccc

        # cria o socket de recebimento de comando/controle/configuração
        self.__sck_rcv_ccc = listener.CNetListener(ft_ifc, fs_adr, fi_ccc, self.__q_rcv_ccc)
        assert self.__sck_rcv_ccc

    # ---------------------------------------------------------------------------------------------
    # @staticmethod
    def notify(self, f_evt):
        """
        event handling callback

        @param f_event: received event
        """
        # check input
        assert f_evt
        
        # received quit event ?
        if isinstance(f_evt, events.CQuit):
            # para todos os processos
            gdata.G_KEEP_RUN = False

            # wait all tasks terminate
            time.sleep(1)

            # ends application
            sys.exit()

    # =============================================================================================
    # dados     
    # =============================================================================================
        
    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        return self.__app

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        return self.__event
        
    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self.__model

    # ---------------------------------------------------------------------------------------------
    @property
    def q_rcv_ccc(self):
        return self.__q_rcv_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_ccc(self):
        return self.__sck_rcv_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def q_snd_ccc(self):
        return self.__q_snd_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_snd_ccc(self):
        return self.__sck_snd_ccc

    # ---------------------------------------------------------------------------------------------
    @property
    def splash(self):
        return self.__splash

    # ---------------------------------------------------------------------------------------------
    @property
    def view(self):
        return self.__view

# < the end >--------------------------------------------------------------------------------------
