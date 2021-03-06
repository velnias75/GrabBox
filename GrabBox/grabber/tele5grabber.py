# -*- coding: utf-8 -*-
#
# Copyright 2019-2020 by Heiko Schäfer <heiko@rangun.de>
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

# nexx-API in youtube-dl:
# https://github.com/ytdl-org/youtube-dl/blob/eb22d1b55744b69d5ec3556529868acfba6c217f/youtube_dl/extractor/nexx.py

from GrabBox.grabber.generichlsgrabber import GenericHLSGrabber
from GrabBox.grabber.dashgrabber import DASHGrabber
from urllib.parse import urlencode
from urllib.error import HTTPError
import urllib.request as req
import shlex
import json
import sys


class Tele5Grabber(DASHGrabber):

    __url = None

    def __init__(self, url_, out_):
        super(Tele5Grabber, self).__init__(url_, out_)
        self.__url = url_

    def url(self, quote=True):

        sys.stderr.write("[I] Analyzing Tele5-URL for videos …\n")
        sys.stderr.flush()

        try:
            t5req = req.Request(self.__url)
            t5rsp = req.urlopen(t5req)
            t5pag = str(t5rsp.read())
            t5idx = t5pag.index('data-video-id=\"')
            t5len = t5pag[t5idx+15:t5idx+1024].index('\"')
            t5vid = t5pag[t5idx+15:t5idx+15+t5len]

            try:
                jwreq = req.Request("https://cdn.jwplayer.com/v2/media/" +
                                    t5vid)
                jwrsp = req.urlopen(jwreq)

                try:
                    json_ = json.loads(jwrsp.read())
                    jaux_ = json_['playlist'][0]['sources'][0]['file']. \
                        split("/")
                    jlen_ = jaux_[4].find("_")

                    if jlen_ is not -1:
                        t5vid = jaux_[4][0:jlen_]
                    elif jaux_[4].find(".ism"):
                        t5vid = json_['playlist'][0]['sources'][0]['file']

                except json.JSONDecodeError:
                    raise ValueError("Received invalid " +
                                     "JSON data from jwplayer")

            except HTTPError as hex:
                raise ValueError("Error in connecting jwplayer: " +
                                 str(hex.code) + " " + hex.reason)

        except HTTPError as hex:
            raise ValueError("Error in connecting Tele5 at \"" +
                             self.__url + "\": " + str(hex.code) + " "
                             + hex.reason)
        except ValueError:
            raise ValueError("No video-ID found at: \"" + self.__url + "\"")

        if "https://" == t5vid[0:8]:
            resu = t5vid
        else:
            try:
                data_ = urlencode({'nxp_devh': '1548566809:9479'})
                requ_ = req.Request('https://api.nexx.cloud/v3/759/session/" \
                    "init', data_.encode('utf-8'),
                                    {'X-Request-Enable-Auth-Fallback': '1'})
                resp_ = req.urlopen(requ_)

                try:
                    json_ = json.loads(resp_.read())
                except json.JSONDecodeError:
                    raise ValueError("Received invalid JSON data")

                try:
                    cid = json_['result']['general']['cid']
                except KeyError:
                    raise ValueError("Received no client id from nexx")

                data_ = urlencode({'addStreamDetails': '1'})
                requ_ = \
                    req.Request('https://api.nexx.cloud/v3/759/videos/byid/' +
                                t5vid, data_.encode('utf-8'),
                                {'X-Request-Token':
                                 'e40c07933eee1500e9251dff3afcceb0',
                                 'X-Request-CID': cid})
                resp_ = req.urlopen(requ_)

                try:
                    json_ = json.loads(resp_.read())
                except json.JSONDecodeError:
                    raise ValueError("Received invalid JSON data")

                try:
                    loc = json_['result']['streamdata']['azureLocator']
                except KeyError:
                    raise ValueError("Received no azureLocator from nexx")

            except HTTPError as ex:
                raise ValueError("Error in connecting the nexx-API: " +
                                 str(ex.code) + " " + ex.reason)

            resu = "https://tele5nexx.akamaized.net/" + loc + "/" + t5vid + \
                "_src.ism/Manifest(format=mpd-time-cmaf)"

        sys.stderr.write("[I] Downloading video from \"" + resu + "\" …\n")
        sys.stderr.flush()

        return shlex.quote(resu) if quote else resu

    def grab(self):

        gurl_ = self.url(False)

        if "https://" == gurl_[0:8]:
            GenericHLSGrabber(gurl_, self.out(), "-map p:2").grab()
        else:
            super().grab()

# kate: indent-mode: python
