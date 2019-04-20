#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_plot_model

papi calibrate

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
from PyQt4 import Qwt5

# model
import model.pc_utils as util

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# max curves per plot
M_CURVES = 3

# max number of samples
M_SAMPLE_SIZE = 100

# < CWidgetPlotModel >-----------------------------------------------------------------------------

class CWidgetPlotModel(QtGui.QWidget):
    """
    plot chart widget
    """
    # signals
    # C_SIG_NEW_FRAME = QtCore.pyqtSignal(cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_source_feed, f_parent=None):
        """
        constructor

        @param f_source_feed: image source
        @param f_parent: parent widget
        """
        # check input
        assert f_source_feed

        # init super class
        super(CWidgetPlotModel, self).__init__(f_parent)

        # list of timestamps
        self.__lst_timestamps = []

        # samples
        self.__lst_samples = [[] for _ in xrange(M_CURVES)]

        # plot
        self.__plot = None

        # curve
        self.__lst_curves = [None] * M_CURVES

        # flag on/off to curve (by default all curve are plotted)
        self.__v_curve_on = [True] * M_CURVES

        # list of checkBoxes
        self.__lst_checkboxes = []

        # image source
        #self.__camera_feed = f_source_feed
        #self.__camera_feed.C_SIG_NEW_FRAME.connect(self.on_new_frame)

    # ---------------------------------------------------------------------------------------------
    def _activate_curve(self, fi_axe):
        """
        activate curve
        """
        # check input
        assert -1 < fi_axe < M_CURVES

        # activate curve
        self.__v_curve_on[fi_axe] = self.__lst_checkboxes[fi_axe].isChecked()

    # ---------------------------------------------------------------------------------------------
    def _clear_plot(self):
        """
        clear screen
        """
        # for all list samples
        for l_samples in self.__lst_samples:
            # clear list
            l_samples = []

        # clear timestamp list
        self.__lst_timestamps = []

    # ---------------------------------------------------------------------------------------------
    def _create_checkbox(self, fs_label, l_color, f_connect_fn, f_connect_param):
        """
        create a personalized checkbox

        @param fs_label: the label
        @param l_color: color
        @param f_connect_fn: activated function
        @param f_connect_param: transmitted parameter

        @return return a checkbox widget
        """
        # create checkBox
        l_check_box = QtGui.QCheckBox(fs_label)
        assert l_check_box

        # setup
        l_check_box.setChecked(1)
        l_check_box.setFont(QtGui.QFont("Arial", pointSize=12, weight=QtGui.QFont.Bold))

        # create a pallete
        l_pal = QtGui.QPalette()
        assert l_pal

        # set checkBox color
        l_pal.setColor(QtGui.QPalette.Foreground, l_color)

        # set checkBox pallete
        l_check_box.setPalette(l_pal)

        # make connections
        l_check_box.clicked.connect(util.partial(f_connect_fn, f_connect_param))

        # return
        return l_check_box

    # ---------------------------------------------------------------------------------------------
    def _create_plot(self, fs_title, fi_ymin, fi_ymax):
        """
        create the pyqwt plot

        @param fs_title: plot title
        @param fi_ymin: minimum
        @param fi_ymax: maximum

        @return a list containing the plot and the list of the curves
        """
        # create plot
        self.__plot = Qwt5.QwtPlot(self)
        assert self.__plot

        # background colour
        self.__plot.setCanvasBackground(QtCore.Qt.black)

        # config bottom axis
        self.__plot.setAxisTitle(Qwt5.QwtPlot.xBottom, "Time (s)")
        self.__plot.setAxisScale(Qwt5.QwtPlot.xBottom, 0, 10, 1)

        # config left axis
        self.__plot.setAxisTitle(Qwt5.QwtPlot.yLeft, fs_title)
        self.__plot.setAxisScale(Qwt5.QwtPlot.yLeft, fi_ymin, fi_ymax, (fi_ymax - fi_ymin) / 10.)
        self.__plot.setAxisAutoScale(Qwt5.QwtPlot.yLeft)
        # self.__plot.axisScaleEngine(Qwt5.QwtPlot.yLeft).setAttribute(Qwt5.QwtScaleEngine.Floating, True)

        # redraw
        self.__plot.replot()

        # define 3 curves
        self.__lst_curves = [None] * M_CURVES

        # define pen
        llst_pen = [QtGui.QPen(QtGui.QColor("limeGreen")),
                    QtGui.QPen(QtGui.QColor("red")),
                    QtGui.QPen(QtGui.QColor("yellow"))]

        # for all curves...
        for li_ndx in xrange(M_CURVES):
            # create curve
            self.__lst_curves[li_ndx] = Qwt5.QwtPlotCurve("{}".format(li_ndx))
            assert self.__lst_curves[li_ndx]

            # config curve
            self.__lst_curves[li_ndx].setRenderHint(Qwt5.QwtPlotItem.RenderAntialiased)

            # config pen
            llst_pen[li_ndx].setWidth(2)

            # set pen
            self.__lst_curves[li_ndx].setPen(llst_pen[li_ndx])

            # attach curve to plot
            self.__lst_curves[li_ndx].attach(self.__plot)

        # return
        return self.__plot, self.__lst_curves

    # ---------------------------------------------------------------------------------------------
    def _update_plot(self, flst_data):
        """
        updates the state of the plot widget with new data

        @param flst_data: data list
        """
        # save timestamp
        self.__lst_timestamps.append(float(flst_data[0]))

        # timestamp overflow ?
        if len(self.__lst_timestamps) > M_SAMPLE_SIZE:
            # make some room
            self.__lst_timestamps.pop(0)

        # for all curves...
        for li_ndx in xrange(M_CURVES):
            # save sample
            self.__lst_samples[li_ndx].append(float(flst_data[li_ndx + 1]))

            # samples overflow ?
            if len(self.__lst_samples[li_ndx]) > M_SAMPLE_SIZE:
                # make some room
                self.__lst_samples[li_ndx].pop(0)

            # show curve ?
            if self.__v_curve_on[li_ndx]:
                # set curve data (xdata, ydata)
                self.__lst_curves[li_ndx].setData(self.__lst_timestamps, self.__lst_samples[li_ndx])

            # axis scale (xBottom, xdata[0], max(20, xdata[-1]))
            self.__plot.setAxisScale(Qwt5.QwtPlot.xBottom, self.__lst_timestamps[0], max(9, self.__lst_timestamps[-1]))

            # update plot
            self.__plot.replot()
        
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_checkboxes(self):
        return self.__lst_checkboxes

    @lst_checkboxes.setter
    def lst_checkboxes(self, f_val):
        self.__lst_checkboxes = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def plot(self):
        return self.__plot

# < the end >--------------------------------------------------------------------------------------
