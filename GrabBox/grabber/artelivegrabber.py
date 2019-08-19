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

from GrabBox.grabber.abstractlivegrabber import AbstractLiveGrabber


class ArteLiveGrabber(AbstractLiveGrabber):

    __dursec = None

    def __init__(self, dursec_, out_):
        super(ArteLiveGrabber, self). \
              __init__("https://artelive-lh.akamaihd.net/i/" +
                       "artelive_de@393591/index_1_av-p.m3u8", out_, dursec_)

    def map(self):
        return "-map p:0 -map -0:2"

#    def bsf(self):
#       return "-bsf:a aac_adtstoasc"

# kate: indent-mode: python
