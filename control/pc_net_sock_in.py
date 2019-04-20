#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_net_sock_in

DOCUMENT ME!

revision 0.1  2017/may  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < imports >--------------------------------------------------------------------------------------

# python library
import errno
import logging
import socket

# model 
import model.pc_data as gdata

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CNetSockIn >-----------------------------------------------------------------------------------

class CNetSockIn(socket.socket):
    """
    communication socket to receive messages
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ft_ifce, fs_addr, fi_port):
        """
        constructor

        @param ft_ifce: tupla in/out de interfaces. ('eth0', 'eth0')
        @param fs_addr: endereço multicast. ('225.12.2')
        @param fi_port: porta. (1970)
        """
        # check input
        assert fs_addr
        assert fi_port

        # init super class
        super(CNetSockIn, self).__init__(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # logger
        # M_LOG.debug("socket: {}:{} on {}".format(fs_addr, fi_port, ft_ifce))

        # especificou uma interface ?
        if ft_ifce[0] is not None:
            # seleciona a interface (from socket.h, SO_BINDTODEVICE 25)
            self.setsockopt(socket.SOL_SOCKET, 25, ft_ifce[0] + '\0')

        # set some options to make it multicast-friendly
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # set some options to make it multicast-friendly
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # em caso de erro...
        except AttributeError as l_err:
            # logger
            l_log = logging.getLogger("CNetSockIn::__init__")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: some systems don't support SO_REUSEPORT: {}".format(l_err))

        try:
            # bind socket to local host and port
            self.bind((fs_addr, fi_port))

            # instead of: self.bind(('', fi_port))
            # ...because if you want to listen to multiple mcast groups on the same port, you'll get
            # all messages on all listeners

        # em caso de erro...
        except socket.error, l_err:
            # logger
            l_log = logging.getLogger("CNetSockIn::__init__")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E02: bind failed: {} - {}".format(l_err[0], l_err[1]))

            # termina
            sys.exit()

            # logger
            # M_LOG.debug("socket bind complete")

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive application
        """
        # clear to go
        assert self.__fd_recv

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1)

        # non-blocking socket
        self.__fd_recv.settimeout(0.)
        self.__fd_recv.setblocking(0)

        # application loop
        while gdata.G_KEEP_RUN:
            try:
                # recebe uma mensagem (de até 512 bytes)
                l_data, l_addr = self.__fd_recv.recvfrom(512)
                # M_LOG.debug("data: {} received from: {}".format(l_data, l_addr))

                # divide a mensagem em seus componentes
                llst_data = l_data.split(gdefs.D_MSG_SEP)
                # M_LOG.debug("llst_data: {}".format(llst_data))

                # versão da mensagem não reconhecida ?
                if gdefs.D_MSG_VRS != int(llst_data[0]):
                    # próxima mensagem
                    continue

                # mensagem válida ?
                if int(llst_data[1]) in gdefs.SET_MSG_VALIDAS:
                    # coloca a mensagem na queue
                    self.__q_queue.put(llst_data[1:])

                # senão, mensagem não reconhecida ou inválida
                else:
                    # logger
                    l_log = logging.getLogger("CNetSockIn::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E01: unknow: {}.".format(llst_data[2:]))

            # em caso de erro...
            except socket.timeout, l_err:
                pass

            # em caso de erro...    
            except socket.error, l_err:
                # get error code
                li_err = l_err.args[0]

                # data unavailable ?
                if (errno.EAGAIN == li_err) or (errno.EWOULDBLOCK == li_err):
                    continue

                # senão, a "real" error occurred
                else:
                    # logger
                    l_log = logging.getLogger("CNetSockIn::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E02: socket receive error: {}.".format(l_err))

# < the end >--------------------------------------------------------------------------------------
