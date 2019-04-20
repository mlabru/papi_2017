#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_image_camera

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

# numPy
import numpy as np

# openCV
import cv2.cv as cv

# pyQT4
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.img_opencv as imocv

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CImageCameraWidget >---------------------------------------------------------------------------

class CImageCameraWidget(QtGui.QWidget):
    """
    QImage for openCV
    """
    # signals
    C_SGN_DATA_FRAME = QtCore.pyqtSignal(cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_camera_feed, f_parent=None):
        """
        constructor

        @param f_camera_feed: image source
        @param f_parent: parent widget
        """
        # check input
        assert f_camera_feed

        # init super class
        super(CImageCameraWidget, self).__init__(f_parent)

        # actual frame
        self.__frame = None

        # image source
        f_parent.C_SGN_DTCT_FRAME.connect(self.__on_dtct_frame) 

        # image source
        # self.__camera_feed = f_camera_feed
        # self.__camera_feed.C_SGN_DATA_FRAME.connect(self.__on_new_frame)

        # setup widget size
        self.setMinimumSize(gdefs.D_CAM_WIDTH, gdefs.D_CAM_HEIGHT)
        self.setMaximumSize(gdefs.D_CAM_WIDTH, gdefs.D_CAM_HEIGHT)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(cv.iplimage)
    def __on_dtct_frame(self, f_frame):
        """
        callback new frame arrived
        """
        # saves its own version of the frame
        self.__frame = f_frame

        # it emits a signal with the saved frame
        # (to process the frame is not responsibility of the widget)
        # self.C_SGN_DATA_FRAME.emit(self.__frame)

        # forces a schedule of a paint event
        self.update()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(cv.iplimage)
    def __on_new_frame(self, f_frame):
        """
        callback new frame arrived
        """
        # saves its own version of the frame
        self.__frame = f_frame

        # it emits a signal with the saved frame
        # (to process the frame is not responsibility of the widget)
        # self.C_SGN_DATA_FRAME.emit(self.__frame)

        # forces a schedule of a paint event
        self.update()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtGui.QPaintEvent)
    def paintEvent(self, f_evt):
        """
        draw frame
        """
        # have frame ?
        if self.__frame is not None:
            # create painter
            l_painter = QtGui.QPainter(self)
            assert l_painter

            # effectively draws it
            l_painter.drawImage(QtCore.QPoint(0, 0), imocv.CImageOpenCV(self.__frame))

# < the end >--------------------------------------------------------------------------------------
        