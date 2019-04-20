#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sp_live_data_feed

a serial port packet monitor that plots live data

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CLiveDataFeed >--------------------------------------------------------------------------------

class CLiveDataFeed(object):
    """ 
    a simple 'live data feed' abstraction that allows a reader to read the most recent data and
    find out whether it was updated since the last read. 
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # pointer to current data  
        self.__cur_data = None

        # a boolean attribute telling the reader whether the data was updated since the last read
        self.__v_has_new_data = False
    
    # ---------------------------------------------------------------------------------------------
    def add_data(self, f_data):
        """
        add new data to the feed (interface to writer)
        """
        # save data
        self.__cur_data = f_data

        # set flag
        self.__v_has_new_data = True
    
    # ---------------------------------------------------------------------------------------------
    def read_data(self):
        """
        returns the most recent data. (interface to reader)
        """
        # set flag
        self.__v_has_new_data = False

        # return 
        return self.__cur_data

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def v_has_new_data(self):
        """
        get v_has_new_data
        """
        return self.__v_has_new_data
        
# < the end >--------------------------------------------------------------------------------------
