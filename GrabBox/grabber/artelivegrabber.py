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
import urllib.request
import sys
import re


class ArteLiveGrabber(AbstractLiveGrabber):

    __dursec = None

    def __init__(self, dursec_, out_):
        super(ArteLiveGrabber, self). \
              __init__(self.__extractHDUrl(dursec_), out_, dursec_)

    def map(self):
        return "-map p:0 -map -0:2"

    def __extractHDUrl(self, dursec_):

        rnl = False
        rsp = urllib.request.urlopen("https://artelive-lh.akamaihd.net/i/"
                                     "artelive_de@393591/master.m3u8")
        pat = re.compile("(#EXT-X-STREAM-INF:.*,RESOLUTION=1280x720,"
                         "CODECS=.*)", re.I)
        urls = []

        for line in rsp.read().decode("utf-8").splitlines():

            if rnl:
                urls.append(line)
                rnl = False

            if pat.match(line):
                rnl = True

        if len(urls) > 0:
            url = urls.pop()
            sys.stderr.write("[I] Grabbing " + str(dursec_) +
                             " seconds from URL: " + url + "\n")
            return url

        raise ValueError("No usable HD stream URL found.")

# kate: indent-mode: python
