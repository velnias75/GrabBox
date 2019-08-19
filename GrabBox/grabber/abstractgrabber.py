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

import os
import sys
import shlex


class AbstractGrabber:

    __url = None
    __out = None

    def __init__(self, url_, out_):

        self.__url = shlex.quote(url_)
        self.__out = shlex.quote(out_)

    def ext(self):
        raise NotImplementedError("ext() not implemented yet")

    def out(self):
        return self.__out

    def url(self):
        return self.__url

    def cmd(self):
        raise NotImplementedError("cmd() not implemented yet")

    def grab(self):
        sys.stderr.write("[I] Writing to: " + shlex.split(self.__out)[0] +
                         self.ext() + "\n")
        os.system(self.cmd())

# kate: indent-mode: python
