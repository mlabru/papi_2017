#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_light_box

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

# view
import view.wid_light as wl

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CLightBoxWidget >------------------------------------------------------------------------------

class CLightBoxWidget(QtGui.QWidget):
    """
    light box widget
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CLightBoxWidget, self).__init__()

        # create white light
        self.__white_light = wl.CLightWidget(QtCore.Qt.white)
        assert self.__white_light

        # create red light
        self.__red_light = wl.CLightWidget(QtCore.Qt.red)
        assert self.__red_light

        # create palette
        l_pal = QtGui.QPalette()
        assert l_pal
        
        # set background color
        l_pal.setColor(QtGui.QPalette.Background, QtCore.Qt.black)

        # set widget palette
        self.setPalette(l_pal)
        self.setAutoFillBackground(True)

        # create widget layout
        l_vbox = QtGui.QVBoxLayout(self)
        assert l_vbox is not None

        # put lights on layout
        l_vbox.addWidget(self.__white_light)
        l_vbox.addWidget(self.__red_light)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def red_light(self):
        return self.__red_light

    # ---------------------------------------------------------------------------------------------
    @property
    def white_light(self):
        return self.__white_light

# < the end >--------------------------------------------------------------------------------------
