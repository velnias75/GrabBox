# -*- coding: utf-8 -*-
#
# Copyright 2019 by Heiko Schäfer <heiko@rangun.de>
#
# This file is part of GrabBox.
#
# GrabBox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# GrabBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with GrabBox.  If not, see <http://www.gnu.org/licenses/>.
#

from GrabBox.grabber.srfgrabber import SRFGrabber
from GrabBox.grabber.dashgrabber import DASHGrabber
from GrabBox.grabber.artegrabber import ArteGrabber
from GrabBox.grabber.tele5grabber import Tele5Grabber
from GrabBox.grabber.servusgrabber import ServusGrabber
from GrabBox.grabber.artelivegrabber import ArteLiveGrabber
from GrabBox.grabber.generichlsgrabber import GenericHLSGrabber
import shlex
import sys


class GrabberFactory:

    __grabber = None
    __grabUrl = False
    __grabbers = ["generic", "srf", "servus", "dash", "artelive", "arte",
                  "tele5", "url"]

    def __init__(self, args=None):

        if args is not None:
            if self.__grabbers[7] != args.source:
                self.__grabber = self.__getGrabber(args.source, args.url,
                                                   args.out, args.map)
            else:
                try:
                    idx_ = args.url.index(':')
                    self.__grabUrl = True
                    self.__grabber = self.__getGrabber(args.url[:idx_],
                                                       args.url[idx_+1:],
                                                       args.out, args.map)
                except ValueError:
                    pass

    def __getGrabber(self, src, url, out, map):

        if self.__grabbers[0] == src:
            return GenericHLSGrabber(url, out, map)
        elif self.__grabbers[1] == src:
            return SRFGrabber(url, out)
        elif self.__grabbers[2] == src:
            return ServusGrabber(url, out)
        elif self.__grabbers[3] == src:
            return DASHGrabber(url, out)
        elif self.__grabbers[4] == src:
            return ArteLiveGrabber(url, out)
        elif self.__grabbers[5] == src:
            return ArteGrabber(url, out)
        elif self.__grabbers[6] == src:
            return Tele5Grabber(url, out)

        raise ValueError("source \'" + src + "\' not supported.")

    def grab(self):

        if self.__grabUrl:
            sys.stdout.write(self.__grabber.url(False) + '\n')
        else:
            self.__grabber.grab()

    def sources(self):
        return ", ".join(self.__grabbers)

# kate: indent-mode: python
