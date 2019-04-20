#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_light

papi calibrate

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

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CLightWidget >---------------------------------------------------------------------------------

class CLightWidget(QtGui.QWidget):
    """
    light widget
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_colour):
        """
        constructor
        """
        # init super class
        super(CLightWidget, self).__init__()

        # light colour
        self.__colour = f_colour

        # flag on
        self.__v_on = False

    # ---------------------------------------------------------------------------------------------
    def isOn(self):
        """
        return if light is on
        """
        return self.__v_on

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtGui.QPaintEvent)
    def paintEvent(self, f_evt):
        """
        paint event callback
        """
        # create painter
        painter = QtGui.QPainter(self)
        assert painter
        
        # setup
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(self.__colour if self.__v_on else QtCore.Qt.black)
        painter.drawEllipse(0, 0, self.width(), self.height())

    # ---------------------------------------------------------------------------------------------
    def __set_on(self, fv_on):
        """
        set widget on/off
        """
        # unchange state ?
        if self.__v_on == fv_on:
            # return
            return

        # save new state
        self.__v_on = fv_on

        # update widget
        self.update()

    # ---------------------------------------------------------------------------------------------
    def turnOff(self):
        """
        turns light off
        """
        self.__set_on(False)

    # ---------------------------------------------------------------------------------------------
    def turnOn(self):
        """
        turns light on
        """
        self.__set_on(True)

# < the end >--------------------------------------------------------------------------------------
