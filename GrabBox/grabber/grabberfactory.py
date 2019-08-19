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
from GrabBox.grabber.servusgrabber import ServusGrabber
from GrabBox.grabber.artelivegrabber import ArteLiveGrabber
from GrabBox.grabber.generichlsgrabber import GenericHLSGrabber


class GrabberFactory:

    __grabber = None

    def __init__(self, args):

        if "generic" == args.source:
            self.__grabber = GenericHLSGrabber(args.url, args.out, args.map)
        elif "srf" == args.source:
            self.__grabber = SRFGrabber(args.url, args.out)
        elif "servus" == args.source:
            self.__grabber = ServusGrabber(args.url, args.out)
        elif "dash" == args.source:
            self.__grabber = DASHGrabber(args.url, args.out)
        elif "artelive" == args.source:
            self.__grabber = ArteLiveGrabber(args.url, args.out)
        else:
            raise ValueError("source \'" + args.source + "\' not supported.")

    def grab(self):
        self.__grabber.grab()

# kate: indent-mode: python
