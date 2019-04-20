#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
gbx_camera

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
import cv2
import cv2.cv as cv

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_detect as dtct

# view
import view.img_opencv as imocv
import view.wid_image_camera as wimc

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CCameraWidget >--------------------------------------------------------------------------------

class CCameraWidget(QtGui.QGroupBox):
    """
    QImage for openCV
    """
    # signals
    C_SGN_DTCT_FRAME = QtCore.pyqtSignal(cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_title, f_camera_feed, f_parent=None):
        """
        constructor

        @param fs_title: groupBox title
        @param f_camera_feed: image source
        @param f_parent: parent widget
        """
        # check input
        assert f_camera_feed

        # init super class
        super(CCameraWidget, self).__init__(fs_title, f_parent)

        # image source
        self.__camera_feed = f_camera_feed
        self.__camera_feed.C_SGN_DATA_FRAME.connect(self.__on_new_frame)

        # frame number
        self.__i_frame_no = 0

        # recording flag
        self.__v_recording = False

        # camera image
        lwid_cam = wimc.CImageCameraWidget(f_camera_feed, self)
        assert lwid_cam

        # image source
        # lwid_cam.C_SGN_DATA_FRAME.connect(self.__on_new_frame)

        # record image button
        self.__btn_rec = QtGui.QPushButton("REC")
        assert self.__btn_rec

        # connect record image button
        self.__btn_rec.clicked.connect(self.__on_btn_rec_clicked)

        # stop record image button
        self.__btn_stp = QtGui.QPushButton("STOP")
        assert self.__btn_stp

        # setup
        self.__btn_stp.setEnabled(False)

        # connect stop record image button
        self.__btn_stp.clicked.connect(self.__on_btn_stp_clicked)

        # create grid layout
        llay_gbx = QtGui.QVBoxLayout()
        assert llay_gbx is not None

        # put on layout
        llay_gbx.addWidget(lwid_cam)
        llay_gbx.addWidget(self.__btn_rec)
        llay_gbx.addWidget(self.__btn_stp)

        # set groupBox layout 
        self.setLayout(llay_gbx)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_rec_clicked(self):
        """
        callback new frame arrived
        """
        # setup buttons
        self.__btn_rec.setEnabled(False)
        self.__btn_stp.setEnabled(True)

        # recording
        self.__v_recording = True
        
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_stp_clicked(self):
        """
        callback new frame arrived
        """
        # stop recording
        self.__v_recording = False

        # setup buttons
        self.__btn_rec.setEnabled(True)
        self.__btn_stp.setEnabled(False)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(cv.iplimage)
    def __on_new_frame(self, f_frame):
        """
        callback new frame arrived
        """
        # recording ?
        if self.__v_recording:
            # convert iplimage to cvMat to np.array
            l_frame = np.asarray(f_frame[:])

            # save image
            cv2.imwrite("data/records/{0:05d}.jpg".format(self.__i_frame_no), l_frame)

            # increment frame number
            self.__i_frame_no += 1

        # detect papi lights on frame
        self.__frame = dtct.detect(f_frame)

        # it emits a signal with the detected frame
        self.C_SGN_DTCT_FRAME.emit(self.__frame)

# < the end >--------------------------------------------------------------------------------------
        