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

from GrabBox.grabber.abstractgrabber import AbstractGrabber
import shutil
import shlex


class AbstractHLSGrabber(AbstractGrabber):

    __url = None

    def __init__(self, url_, out_):
        super(AbstractHLSGrabber, self).__init__(url_, out_)
        self.__url = url_

    def ext(self):
        return ".ts"

    def map(self):
        raise NotImplementedError("map() not implemented yet")

    def live(self):
        return ""

    def reconnect(self):
        return ""

    def bsf(self):
        return ""

    def dursec(self):
        return ""

    def url(self, quote=True):
        return self.__url if not quote else \
            super(AbstractGrabber, self).url(quote)

    def cmd(self):

        ffmpeg = shutil.which("ffmpeg")

        if ffmpeg is None:
            raise RuntimeError("no ffmpeg found")

        return "ionice -t -c 3 chrt -b 0 " + ffmpeg + " -hide_banner " + \
            " -loglevel 8 -stats " + self.live() + " -i " + self.url() + \
            " " + self.reconnect() + " -c copy " + self.map() + \
            " -bsf:v h264_mp4toannexb " + self.bsf() + " -f mpegts " + \
            self.dursec() + " -y " + shlex.quote(self.out() + self.ext())

# kate: indent-mode: python
