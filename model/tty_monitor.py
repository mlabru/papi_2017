#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
tty_monitor

a thread for monitoring a TTY port

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""

# < imports >--------------------------------------------------------------------------------------
import glob
import logging
import os
import Queue
import serial
import threading
import time

# model
# import pc_data as gdata

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CTTYMonitor >----------------------------------------------------------------------------------

class CTTYMonitor(threading.Thread):
    """
    a thread for monitoring a TTY port. The TTY port is opened when the thread is started
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fq_data, fq_error, fs_tty, fi_baud, fi_stopbits=serial.STOPBITS_ONE,
                       fi_parity=serial.PARITY_NONE, ff_timeout=0.01):
        """
        constructor
        """
        # init super class
        super(CTTYMonitor, self).__init__()

        # TTY port to open. Must be recognized by the system
        self.__tty_port = None

        # serial communication parameters
        # timeout used for reading the TTY port. If this value is low, the thread will return
        # data in finer grained chunks, with more accurate timestamps, but it will also consume more CPU.
        self.__dct_args = dict(port     = fs_tty,
                               baudrate = fi_baud,
                               stopbits = fi_stopbits,
                               parity   = fi_parity,
                               timeout  = ff_timeout)

        # queue for received data
        # items in the queue are (data, timestamp) pairs, where data is a binary string
        # representing the received data, and timestamp is the time elapsed from the thread's
        # start (in seconds).
        self.__queue_data = fq_data

        # queue for error messages
        # in particular, if the serial port fails to open for some reason, an error is placed into this queue
        self.__queue_error = fq_error

        # create mechanism for communication between threads
        self.__alive = threading.Event()
        assert self.__alive

        # set the internal flag to true
        self.__alive.set()

    # ---------------------------------------------------------------------------------------------
    def join(self, ff_timeout=None):
        """
        override join method
        """
        # reset the internal flag to false
        self.__alive.clear()

        # call super class
        threading.Thread.join(self, ff_timeout)

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        drive tty monitor
        """
        try:
            # serial already opened ?
            if self.__tty_port:
                # closes serial port
                self.__tty_port.close()

            # open serial port
            self.__tty_port = serial.Serial(**self.__dct_args)
            assert self.__tty_port

        # em caso de erro...
        except serial.SerialException, ls_msg:
            # put error message on queue
            self.__queue_error.put(ls_msg.message)

            # return
            return

        # restart the clock
        lf_time_ini = time.time()

        # while the internal flag is true
        while self.__alive.isSet():

            # read a line from serial
            ls_line = self.__tty_port.readline()

            # empty line ?
            if "" == ls_line:
                # try next one...
                continue

            # get time
            lf_timestamp = time.clock()

            # put message on queue
            self.__queue_data.put((ls_line, lf_timestamp))

        # serial opened ?
        if self.__tty_port:
            # close serial port
            self.__tty_port.close()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def alive(self):
        """
        get alive event
        """
        return self.__alive

    @alive.setter
    def alive(self, f_val):
        """
        set alive event
        """
        self.__alive = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def queue_data(self):
        """
        get data queue
        """
        return self.__queue_data

    @queue_data.setter
    def queue_data(self, f_val):
        """
        set data queue
        """
        self.__queue_data = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def queue_error(self):
        """
        get error queue
        """
        return self.__queue_error

    @queue_error.setter
    def queue_error(self, f_val):
        """
        set error queue
        """
        self.__queue_error = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def tty_port(self):
        """
        get tty port
        """
        return self.__tty_port

    @tty_port.setter
    def tty_port(self, f_val):
        """
        set tty port
        """
        self.__tty_port = f_val

# -------------------------------------------------------------------------------------------------
def enumerate_serial_ports():
    """ 
    scan for available serial ports

    @return a list of of the availables ports names
    """
    # wndows ?
    if 'nt' == os.name:
        # init answer list
        llst_available_ports = []

        # for all ports...
        for li_ndx in xrange(256):
            try:
                # try to open serial port
                l_tty = serial.Serial(li_ndx)

                # put port in list
                llst_available_ports.append(l_tty.portstr)

                # close port
                l_tty.close()   

            # em caso de erro...
            except serial.SerialException:
                # ok
                pass

        # return ports list
        return llst_available_ports

    # return ports list
    return glob.glob('/dev/tty*')

# < the end >--------------------------------------------------------------------------------------
