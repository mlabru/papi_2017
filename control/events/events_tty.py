#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_tty

generic event superclass. What follows is a list of all events. None of these classes should
perform any tasks, as that could introduce vulnerabilities

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
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# control
import control.events.events_model as model

# < class CTTYMonitor >----------------------------------------------------------------------------

class CTTYMonitor(model.CEventsModel):
    """
    CTTYMonitor event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        contructor
        """
        # init super class
        super(CTTYMonitor, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        # save event id
        self.s_name = "TTYMonitor event"

# < class CTTYMonitorStart >-----------------------------------------------------------------------

class CTTYMonitorStart(CTTYMonitor):
    """
    CTTYMonitorStart event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_port, fi_baud):
        """
        contructor
        """
        # init super class
        super(CTTYMonitorStart, self).__init__()

        # herdados de CTTYMonitor
        # self.s_name        # event name

        # save event id
        self.s_name = "TTYMonitorStart event"

        # port
        self.__s_port = fs_port

        # baudrate
        self.__i_baud = fi_baud

    # ---------------------------------------------------------------------------------------------
    @property
    def i_baud(self):
        """
        get baudrate
        """
        return self.__i_baud

    # ---------------------------------------------------------------------------------------------
    @property
    def s_port(self):
        """
        get port
        """
        return self.__s_port

# < class CTTYMonitorStop >------------------------------------------------------------------------

class CTTYMonitorStop(CTTYMonitor):
    """
    CTTYMonitorStop event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        contructor
        """
        # init super class
        super(CTTYMonitorStop, self).__init__()

        # herdados de CTTYMonitor
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "TTYMonitorStop event"

# < class CTTYMonitorUpdate >----------------------------------------------------------------------

class CTTYMonitorUpdate(CTTYMonitor):
    """
    CTTYMonitorUpdate event class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        contructor
        """
        # init super class
        super(CTTYMonitorUpdate, self).__init__()

        # herdados de CTTYMonitor
        # self.s_name        # event name
        # self.s_callsign    # callsign

        # save event id
        self.s_name = "TTYMonitorUpdate event"

# < the end >--------------------------------------------------------------------------------------
