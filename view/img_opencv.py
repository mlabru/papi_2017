#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
img_opencv

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

# openCV
import cv

# pyQt4
from PyQt4 import QtGui

# < CImageOpenCV >---------------------------------------------------------------------------------

class CImageOpenCV(QtGui.QImage):
    """
    QImage for openCV
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_opencv_bgr_img):
        """
        constructor

        @param f_opencv_bgr_img: BGR image
        """
        # get depth and channels
        l_depth, ln_channels = f_opencv_bgr_img.depth, f_opencv_bgr_img.nChannels

        # not valid image ?
        if (cv.IPL_DEPTH_8U != l_depth) or (3 != ln_channels):
            # raise an error
            raise ValueError("the input image must be 8-bit, 3-channel")

        # get image size
        l_w, l_h = cv.GetSize(f_opencv_bgr_img)

        # create image
        l_opencv_rgb_img = cv.CreateImage((l_w, l_h), l_depth, ln_channels)
        assert l_opencv_rgb_img

        # converts the image from BGR to RGB format. it's assumed the image is in BGR format
        cv.CvtColor(f_opencv_bgr_img, l_opencv_rgb_img, cv.CV_BGR2RGB)

        # saves a reference to the l_opencv_rgb_img byte-content to prevent the garbage
        # collector from deleting it when __init__ returns
        self.__img_data = l_opencv_rgb_img.tostring()

        # call the QImage base class constructor passing the byte-content, dimensions and format of the image
        super(CImageOpenCV, self).__init__(self.__img_data, l_w, l_h, QtGui.QImage.Format_RGB888)

# < the end >--------------------------------------------------------------------------------------
            