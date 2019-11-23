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

from GrabBox.grabber.dashgrabber import DASHGrabber
from urllib.parse import urlencode
import urllib.request as req
import shlex
import json


class Tele5Grabber(DASHGrabber):

    __url = None

    def __init__(self, url_, out_):
        super(Tele5Grabber, self).__init__(url_, out_)
        self.__url = url_

    def url(self):

        t5req = req.Request(self.__url)
        t5rsp = req.urlopen(t5req)
        t5pag = str(t5rsp.read())
        t5idx = t5pag.index('data-id=\"')
        t5len = t5pag[t5idx+9:t5idx+1024].index('\"')
        t5vid = t5pag[t5idx+9:t5idx+9+t5len]

        data_ = urlencode({'nxp_devh': '1548566809:9479'})
        requ_ = req.Request('https://api.nexx.cloud/v3/759/session/init',
                            data_.encode('utf-8'),
                            {'X-Request-Enable-Auth-Fallback': '1'})
        resp_ = req.urlopen(requ_)
        json_ = json.loads(resp_.read())

        cid = json_['result']['general']['cid']

        data_ = urlencode({'addStreamDetails': '1'})
        requ_ = req.Request('https://api.nexx.cloud/v3/759/videos/byid/' +
                            t5vid, data_.encode('utf-8'), {
                                'X-Request-Token':
                                    'e40c07933eee1500e9251dff3afcceb0',
                                    'X-Request-CID': cid})
        resp_ = req.urlopen(requ_)
        json_ = json.loads(resp_.read())

        loc = json_['result']['streamdata']['azureLocator']

        return shlex.quote("https://tele5nexx.akamaized.net/" + loc + "/" +
                           t5vid + "_src.ism/Manifest(format=mpd-time-cmaf)")


# kate: indent-mode: python
