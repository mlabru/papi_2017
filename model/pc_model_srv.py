#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_model

papi calibrate

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------
import logging
import Queue
#import threading
import time
#import serial
import sys

# PyQt library
from PyQt4 import QtCore

# model
import model.pc_data as gdata
import model.pc_live_data_feed as ldf
import model.tty_monitor as tmon

# control
import control.events.events_basic as events
import control.events.events_tty as evttty

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPAPICalModelSrv >-----------------------------------------------------------------------------

class CPAPICalModelSrv(object):
    """
    PAPI Calibra model
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        constructor
        """
        # check input
        assert f_control
         
        # event manager
        self.__event = f_control.event
        assert self.__event

        # register as event listener
        self.__event.register_listener(self)

        # tty default settings
        self.__s_port = f_control.config.dct_config["ser.port"]
        self.__i_baudrate = f_control.config.dct_config["ser.baud"]

        # on/off monitor state
        self.__v_monitor_active = False

        # live data feed
        self.__live_feed = ldf.CLiveDataFeed()
        assert self.__live_feed

        #self.com_data_q     = None
        #self.com_error_q    = None
        #self.csvdata        = []

        # data queue
        self.__queue_data = Queue.Queue()
        assert self.__queue_data

        # error queue
        self.__queue_error = Queue.Queue()
        assert self.__queue_error

        # monitor reception thread
        self.__thr_monitor = tmon.CTTYMonitor(self.__queue_data, self.__queue_error, self.__s_port, self.__i_baudrate)
        assert self.__thr_monitor

        # get error message
        ls_tty_error = self.get_item_from_queue(self.__queue_error)

        if ls_tty_error is not None:
            # reset thread
            self.__thr_monitor = None

            # logger
            M_LOG.critical("CPAPICalModelSrv::__init__: {}".format(ls_tty_error))

    # ---------------------------------------------------------------------------------------------
    def get_all_from_queue(self, fq_queue):
        """ 
        generator to yield one after the others all items currently in the queue fq_queue,
        without any waiting
        """
        try:
            while True:
                yield fq_queue.get_nowait()

        # em caso de erro...
        except Queue.Empty:
            # raise exception
            raise StopIteration

    # ---------------------------------------------------------------------------------------------
    def get_item_from_queue(self, fq_queue, ff_timeout=0.01):
        """ 
        attempts to retrieve an item from the queue fq_queue. If queue is empty, None is returned
            
        @note: don't use this method for speedy retrieval of multiple items
               (use get_all_from_queue for that)
        """
        try: 
            # blocks for 'ff_timeout' seconds in case the queue is empty
            l_item = fq_queue.get(True, ff_timeout)

        # em caso de erro...
        except Queue.Empty: 
            # return
            return None

        # return
        return l_item

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
            # wait all tasks terminate
            time.sleep(1)
            # ends application
            sys.exit()

        # received start event ?
        elif isinstance(f_evt, evttty.CTTYMonitorStart):
            # starts monitor
            self.__thr_monitor.start()
            # set flag
            self.__v_monitor_active = True

        # received update event ?
        elif isinstance(f_evt, evttty.CTTYMonitorUpdate):
            # read data
            self.read_serial_data()

    # ---------------------------------------------------------------------------------------------
    def read_serial_data(self):
        """ 
        called periodically by the update timer to read data from the serial port
        """
        # get all data from serial queue
        llst_data = list(self.get_all_from_queue(self.__queue_data))
        # M_LOG.debug("llst_data: {}".format(llst_data))

        # receive data ?
        if len(llst_data) > 0:
            # get just the most recent data, others are lost
            lt_msg = llst_data[-1]
            # M_LOG.debug("lt_msg: {}".format(lt_msg))
            
            # create dict
            ldct_data = self.trata_msg(lt_msg)
            M_LOG.debug("ldct_data: {}".format(ldct_data))

            # put available on livefeed
            self.__live_feed.add_data(ldct_data)

    # ---------------------------------------------------------------------------------------------
    def trata_msg(self, ft_msg):
        """
        trata input
        format: ('!ANG:-0.62,1.81,90.21,AN:34,39,-11,-159,-35,208,-0.00,-0.32,-0.04\r\n', 0.252393)
        """    
        # get message
        ls_msg = ft_msg[0]

        # valid message ?
        if ls_msg.startswith("!ANG:"):
            # split message
            llst_fields = ls_msg[5:-2].split(',')
            # M_LOG.debug(llst_fields)

            # 12 fields ?
            if 12 == len(llst_fields):
                # raw imu data ?                
                if llst_fields[3].startswith("AN:"):            
                    ls_gyro = llst_fields[3][3:]

                # senão,...
                else:
                    ls_gyro = llst_fields[3]

                # build dictionary 
                ldct_data = dict(roll = float(llst_fields[0]), 
                                 pitch = float(llst_fields[1]),
                                 yaw = float(llst_fields[2]),
                                 gyro_x = float(ls_gyro),
                                 gyro_y = float(llst_fields[4]),
                                 gyro_z = float(llst_fields[5]),
                                 accel_x = float(llst_fields[6]),
                                 accel_y = float(llst_fields[7]),
                                 accel_z = float(llst_fields[8]),
                                 magn_x = float(llst_fields[9]),
                                 magn_y = float(llst_fields[10]),
                                 magn_z = float(llst_fields[11]),
                                 timestamp = float(ft_msg[1]))

                # return
                return ldct_data 
            '''
            # use map(int) for simulation
            # data = map(ord, bytes)
            data = [10, 20, 30, 40, 50, 60]
            qdata = [0, 0, 0]
            
            if len(data) == 6:
                timestamp = time.time() - lf_time_ini
                # data = list(map(ord, list(ls_line)))

                # M_LOG.debug("ls_line.: {}".format(ls_line))
                # M_LOG.debug("bytes: {}".format(bytes))
                # M_LOG.debug("data.: {}".format(data))

                axes = self.getAxes(data)

                # M_LOG.debug("   x = %.3fG" % (axes['x']))
                # M_LOG.debug("   y = %.3fG" % (axes['y']))
                # M_LOG.debug("   z = %.3fG" % (axes['z']))

                qdata[0] = axes['x']
                qdata[1] = axes['y']
                qdata[2] = axes['z']
                # M_LOG.debug("qdata: {}".format(qdata))
            '''
        # return
        return None
            
    # ---------------------------------------------------------------------------------------------
    def getAxes(self, bytes, gforce=True):
        """
        constructor
        """
        x = bytes[0] | (bytes[1] << 8)

        if (x & (1 << 16 - 1)):
            x = x - (1 << 16)

        y = bytes[2] | (bytes[3] << 8)

        if (y & (1 << 16 - 1)):
            y = y - (1 << 16)

        z = bytes[4] | (bytes[5] << 8)

        if (z & (1 << 16 - 1)):
            z = z - (1 << 16)

        x = x * gdata.SCALE_MULTIPLIER
        y = y * gdata.SCALE_MULTIPLIER
        z = z * gdata.SCALE_MULTIPLIER

        if gforce == False:
            x = x * gdata.EARTH_GRAVITY_MS2
            y = y * gdata.EARTH_GRAVITY_MS2
            z = z * gdata.EARTH_GRAVITY_MS2

        x = round(x, 3)
        y = round(y, 3)
        z = round(z, 3)

        return {"x": x, "y": y, "z": z}

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
    def event(self):
        """
        get event
        """
        return self.__event

    # ---------------------------------------------------------------------------------------------
    @property
    def live_feed(self):
        """
        get live data feed
        """
        return self.__live_feed

# < the end >--------------------------------------------------------------------------------------
