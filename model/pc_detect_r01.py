#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_detect

papi calibra

revision 0.1  2017/apr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "mlabru, sophosoft"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os

# numPy
import numpy as np

# openCV
import cv2
import cv2.cv as cv

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

M_RED_1 = 0
M_RED_2 = 170
M_GREEN = 65

# color range
M_LOWER_RED_1 = np.array([M_RED_1, 100, 100])
M_UPPER_RED_1 = np.array([M_RED_1 + 10, 255, 255])

M_LOWER_RED_2 = np.array([M_RED_2 - 10, 100, 100])
M_UPPER_RED_2 = np.array([M_RED_2 + 10, 255, 255])

M_LOWER_GREEN = np.array([M_GREEN - 25, 50, 50])
M_UPPER_GREEN = np.array([M_GREEN + 25, 255, 255])

# font
M_FONT = cv2.FONT_HERSHEY_SIMPLEX

# -------------------------------------------------------------------------------------------------
def __search(f_img, ft_size, f_img_mask, f_circles, ff_threshold, fs_label):
    """
    procura pelas luzes em uma imagem
    
    @param f_img: imagem original
    @param ft_size: tamanho da imagem
    @param f_img_mask: máscara de cores
    @param f_circles: círculos encontrados
    @param ff_threshold: threshold
    @param fs_label: label
    """
    r = 5
    bound = 4. / 10

    # evenly round to 0 decimals
    f_circles = np.uint16(np.around(f_circles))
    #M_LOG.debug("f_circles: {}".format(f_circles))
    #M_LOG.debug("detected {} circles.".format(len(f_circles)))

    # for all detected circles...
    for l_circle in f_circles:
        #M_LOG.debug("x: {} / y: {}".format(l_circle[0], l_circle[1]))

        #M_LOG.debug("ft_size[0]:", ft_size[0]
        #M_LOG.debug("ft_size[1]:", ft_size[1]

        # check if circle is outside image bounds
        #if (l_circle[0] > ft_size[1]) or (l_circle[1] > ft_size[0]) or (l_circle[1] > ft_size[0] * bound):
            #continue

        h, s, rr = 0.0, 0.0, int(l_circle[2])
        # M_LOG.debug("h: {} s: {} r: {} (1):".format(h, s, rr))
        for m in xrange(-rr, rr):
            #M_LOG.debug("m:", m
            for n in xrange(-rr, rr):
                #M_LOG.debug("n:", n
                # check if circle is outside bounds
                if (l_circle[1] + m) >= ft_size[0] or (l_circle[0] + n) >= ft_size[1]:
                    continue

                # acumula contador (0 ou 255)
                # h += f_img_mask[l_circle[1] + m, l_circle[0] + n]
                h += 1 if f_img_mask[l_circle[1] + m, l_circle[0] + n] > 0 else 0
                # incrementa contador de área 
                s += 1

        #M_LOG.debug("h: {} s: {} r: {} (2):".format(h, s, rr))
        cv2.circle(f_img_mask, (l_circle[0], l_circle[1]), l_circle[2] + 4, (255, 255, 255), 2)
        # M_LOG.debug("(h / 255) & (0.2 * s):", (h / 255), (0.2 * s)
        # M_LOG.debug("(h / 255) & ((h / 255) / s):", (h / 255), ((h / 255) / s)
        #M_LOG.debug("(h / s): {}".format(h / s))

        # if h / s > 50:
        # if (h / 255) >= (0.2 * s):
        # if ((h / 255) / s) >= 0.3:
        if (h / s) >= ff_threshold:
            # destaca o ponto na máscara
            # cv2.circle(f_img_mask, (l_circle[0], l_circle[1]), l_circle[2] + 30, (255, 255, 255), 2)
            # destaca o ponto na imagem original
            cv2.circle(f_img, (l_circle[0], l_circle[1]), l_circle[2] + 10, (0, 255, 0), 2)
            # coloca um label
            cv2.putText(f_img, fs_label, (l_circle[0], l_circle[1]), M_FONT, 1, (255, 0, 0), 2)

    # retorna a imagem e a máscara
    return f_img, f_img_mask

# -------------------------------------------------------------------------------------------------
def detect(fimg_ptr):
    """
    faz detecção das luzes brancas e vermelhas na imagem

    @param fimg_ptr: image
    """
    # convert iplimage to cvMat to np.array
    fimg_ptr = np.asarray(fimg_ptr[:])

    # obtém o tamanho da imagem
    lt_size = fimg_ptr.shape

    # salva imagem original
    limg_ptr = fimg_ptr

    # reduce the noise so we avoid false circle detection
    # limg_hsv = cv2.GaussianBlur(fimg_ptr, (9, 9), 2, 2)  # era (5, 5), 2
    # converte a imagem para HSV
    limg_hsv = cv2.cvtColor(fimg_ptr, cv2.COLOR_BGR2HSV)

    # filtra a imagem, criando máscaras de cores
    limg_mask_1 = cv2.inRange(limg_hsv, M_LOWER_RED_1, M_UPPER_RED_1)
    limg_mask_2 = cv2.inRange(limg_hsv, M_LOWER_RED_2, M_UPPER_RED_2)
    limg_mask_r = cv2.add(limg_mask_1, limg_mask_2)
    limg_mask_g = cv2.inRange(limg_hsv, M_LOWER_GREEN, M_UPPER_GREEN)

    # hough circle detect  era (80, 50, 10)
    r_circles = cv2.HoughCircles(limg_mask_r, cv.CV_HOUGH_GRADIENT, 1, 60, param1=50, param2=5,  minRadius=0, maxRadius=10)
    g_circles = cv2.HoughCircles(limg_mask_g, cv.CV_HOUGH_GRADIENT, 1, 60, param1=50, param2=10, minRadius=0, maxRadius=30)

    # achou círculos vermelhos ?
    if r_circles is not None:
        limg_ptr, limg_mask_r = __search(limg_ptr, lt_size, limg_mask_r, r_circles[0, :], 0.3, "VRM")

    # achou círculos brancos ?
    if g_circles is not None:
        limg_ptr, limg_mask_g = __search(limg_ptr, lt_size, limg_mask_g, g_circles[0, :], 0.3, "BRA")

    # convert np.array to iplimage
    l_bitmap = cv.CreateImageHeader((limg_ptr.shape[1], limg_ptr.shape[0]), cv.IPL_DEPTH_8U, 3)

    cv.SetData(l_bitmap, limg_ptr.tostring(), limg_ptr.dtype.itemsize * 3 * limg_ptr.shape[1])

    # exibe imagem resultado
    return l_bitmap

# <the end>----------------------------------------------------------------------------------------
