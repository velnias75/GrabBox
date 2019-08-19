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
import os


class DASHGrabber(AbstractGrabber):

    def __init__(self, url_, out_):
        super(DASHGrabber, self).__init__(url_, out_)

    def ext(self):
        return ".mp4"

    def cmd(self):

        youtube_dl = shutil.which("youtube-dl", os.F_OK | os.X_OK,
                                  os.getenv("HOME") + "/.local/bin")

        if youtube_dl is None:
            youtube_dl = shutil.which("youtube-dl")

        if youtube_dl is None:
            raise RuntimeError("no youtube-dl found")

        return youtube_dl + " -k " + self.url() + " -o " + self.out() + \
            ".%\\(ext\\)s"

# kate: indent-mode: python
