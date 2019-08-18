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


class AbstractHLSGrabber(AbstractGrabber):

    def __init__(self, url_, out_):
        super(AbstractHLSGrabber, self).__init__(url_, out_)

    def map(self):
        raise NotImplementedError("grab() not implemented yet")

    def cmd(self):

        ffmpeg = shutil.which("ffmpeg")

        if ffmpeg is None:
            raise RuntimeError("no ffmpeg found")

        return ffmpeg + " -hide_banner -i " + self.url() + " -c copy " + \
            self.map() + " -bsf:v h264_mp4toannexb -f mpegts -y " + \
            self.out() + ".ts"

# kate: indent-mode: python
