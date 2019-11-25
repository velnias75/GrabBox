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

from GrabBox.grabber.abstracthlsgrabber import AbstractHLSGrabber
import re


class ServusGrabber(AbstractHLSGrabber):

    def __init__(self, url_, out_):
        super(ServusGrabber, self).__init__(url_, out_)

    def map(self):
        return "-map p:1:1 -map p:1:0"

    def url(self, quote=True):

        url_ = super(ServusGrabber, self).url(quote).upper()

        re_ = re.compile(".*/videos/([^/]+).*", re.I)
        ma_ = re_.match(url_)

        if ma_:
            url_ = ma_.group(1)

        return "https://stv.rbmbtnx.net/api/v1/manifests/" + url_ + ".m3u8"

# kate: indent-mode: python
