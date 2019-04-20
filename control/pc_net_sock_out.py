#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_net_sock_out

send socket

revision 0.1  2017/may  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import socket

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CNetSockOut >----------------------------------------------------------------------------

class CNetSockOut(socket.socket):
    """
    send socket
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ft_ifce, fs_addr, fi_port):
        """
        initializes network sender

        @param ft_ifce: tupla in/out de interfaces. ('eth0', 'eth0')
        @param fs_addr: endereço ('224.1.2.3')
        @param fi_port: porta (1970)
        """
        # check input
        assert fs_addr
        assert fi_port

        # init super class
        super(CNetSockOut, self).__init__(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # tupla endereço e porta
        self.__t_addr = (fs_addr, fi_port)

        # especificou uma interface ?
        if ft_ifce is not None:
            # especificou uma interface de saída ?
            if ft_ifce[1] is not None:
                # seleciona a interface (from socket.h, SO_BINDTODEVICE 25)
                self.setsockopt(socket.SOL_SOCKET, 25, ft_ifce[1] + '\0')

        # config sender socket
        self.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # non-blocking socket
        self.settimeout(0.0)
        self.setblocking(0)

    # ---------------------------------------------------------------------------------------------
    def send_data(self, fs_msg):
        """
        send message

        @param fs_msg: message
        """
        try:
            # send message
            self.sendto(fs_msg, self.__t_addr)
            # M_LOG.debug("fs_msg: {} to: {}".format(fs_msg, self.__t_addr))

        # em caso de não enviar a mensagen...
        except Exception, l_err:
            # logger
            l_log = logging.getLogger("CNetSockOut::send_data")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: socket send error: {}.".format(l_err))

# < the end >--------------------------------------------------------------------------------------
