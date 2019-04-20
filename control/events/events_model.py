#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_model

generic event super class

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

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < class CEventsModel >---------------------------------------------------------------------------

class CEventsModel(object):
    """
    generic event super class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CEventsModel, self).__init__()

        # event name
        self.__s_name = "Generic Event"

    # ---------------------------------------------------------------------------------------------
    def __str__(self):
        """
        DOCUMENT ME!
        """
        return "<%s %s>" % (self.__class__.__name__, id(self))

    # ---------------------------------------------------------------------------------------------
    @property
    def s_name(self):
        """
        get event name
        """
        return self.__s_name

    @s_name.setter
    def s_name(self, f_val):
        """
        set event name
        """
        self.__s_name = f_val

# < the end >--------------------------------------------------------------------------------------
