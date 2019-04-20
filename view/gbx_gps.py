#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
gbx_gps

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

# pyQT4
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import wid_chart_model as wplt

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# gps chart widget
M_ALT_YMAX = -20
M_ALT_YMIN = -50

# < CGPSWidget >-----------------------------------------------------------------------------------

class CGPSWidget(wplt.CChartModelWidget):
    """
    widget for gps
    """
    # signals
    C_SGN_DATA_GPS = QtCore.pyqtSignal(list)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_gps_feed, f_parent=None):
        """
        constructor

        @param f_gps_feed: gps data source
        @param f_parent: parent widget
        """
        # check input
        assert f_gps_feed

        # init super class
        super(CGPSWidget, self).__init__(f_gps_feed, f_parent)

        # actual frame
        self.__s_data = None

        # image source
        self.__gps_feed = f_gps_feed
        self.__gps_feed.C_SGN_DATA_GPS.connect(self.on_new_data)

        # create the chart and curves
        self._create_chart("Position (lat/lng)", M_ALT_YMIN, M_ALT_YMAX)

        # curves checkBoxes
        self.lst_checkboxes = [self._create_checkbox("Lat (G)", QtCore.Qt.green,  self._activate_curve, 0),
                               self._create_checkbox("Lng (R)", QtCore.Qt.red,    self._activate_curve, 1),
                               self._create_checkbox("Alt (Y)", QtCore.Qt.yellow, self._activate_curve, 2)]

        # clear chart button
        lbtn_clear = QtGui.QPushButton("clear chart")
        assert lbtn_clear

        # connect clear chart button
        lbtn_clear.clicked.connect(self._clear_chart)

        # create grid layout
        llay_wid = QtGui.QGridLayout()
        assert llay_wid is not None

        llay_wid.addWidget(self.chart, 0, 0, 8, 7)
        llay_wid.addWidget(self.lst_checkboxes[0], 0, 8)
        llay_wid.addWidget(self.lst_checkboxes[1], 1, 8)
        llay_wid.addWidget(self.lst_checkboxes[2], 2, 8)
        llay_wid.addWidget(lbtn_clear, 3, 8)
        # llay_wid.addStretch()

        # set layout
        self.setLayout(llay_wid)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def on_new_data(self, flst_data):
        """
        callback new frame arrived
        """
        # update chart
        self._update_chart(flst_data)

        # it emits a signal with the data
        # (to process the frame is not responsibility of the widget)
        self.C_SGN_DATA_GPS.emit(flst_data)

# < the end >--------------------------------------------------------------------------------------
        