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

from GrabBox.grabber.abstracthlsgrabber import AbstractHLSGrabber
from subprocess import Popen, PIPE
from urllib.error import HTTPError
import urllib.request as urlreq
import urllib.parse as urlparse
import datetime
import shutil
import json
import ast
import sys
import os


class ServusGrabber(AbstractHLSGrabber):

    _HDQualityMap = None

    def __init__(self, url_, out_):
        super(ServusGrabber, self).__init__(url_, out_)

    def map(self):
        return self.__HDQualityMap()

    def url(self, quote=True):

        url_ = super(ServusGrabber, self).url(quote).upper()

        try:
            optreq_ = urlreq.Request("https://auth.redbullmediahouse.com/"
                                     "token",
                                     headers={"Access-Control-Request-Method":
                                              "POST",
                                              "Access-Control-Request-Headers":
                                              "authorization",
                                              "Referer": url_,
                                              "Origin":
                                              "https://www.servustv.com"},
                                     method="OPTIONS")

            urlreq.urlopen(optreq_).read()

            tokreq_ = urlreq.Request("https://auth.redbullmediahouse.com/"
                                     "token",
                                     data=urlparse.
                                     urlencode({"grant_type":
                                                "client_credentials"}).
                                     encode(),
                                     headers={"Authorization":
                                              "Basic SVgtMjJYNEhBNFdEM1cxMTp"
                                              "EdDRVSkFLd2ZOMG5IMjB1NGFBWTBm"
                                              "UFpDNlpoQ1EzNA=="})

            jsonreq_ = urlreq.Request("https://sparkle-api.liiift.io/api/v1/"
                                      "stv/channels/international/assets/" +
                                      urlparse.urlparse(url_).path[8:-1],
                                      headers={"Authorization": "Bearer " +
                                               ast.
                                               literal_eval(urlreq.
                                                            urlopen(tokreq_).
                                                            read().
                                                            decode("UTF-8")).
                                               get("access_token")})
        except HTTPError:
            raise ValueError("Cannot request JSON-data for " + url_)

        m3u8_ = None

        try:
            json_ = json.loads(urlreq.urlopen(jsonreq_).read())

            title_ = None
            short_ = None
            durat_ = None

            for i in json_['attributes']:
                if i['fieldKey'] == "title":
                    title_ = i['fieldValue']
                if i['fieldKey'] == "online_short_teaser":
                    short_ = i['fieldValue']
                if i['fieldKey'] == "duration":
                    durat_ = i['fieldValue']

            for i in json_['resources']:
                if i['type'] == 'hls':
                    m3u8_ = i['url']

            if title_ is not None and short_ is not None:
                sys.stderr.write("[I] Grabbing from ServusTV: " +
                                 title_ + " - " + short_ + "\n")
            if durat_ is not None:
                sys.stderr.write("[I] Duration: " +
                                 str(datetime.
                                     timedelta(milliseconds=durat_)) + "\n")

        except json.JSONDecodeError:
            raise ValueError("Received invalid JSON data")
        except HTTPError:
            raise ValueError("No video found with the ID \"" +
                             urlparse.urlparse(url_).path[8:-1] + "\"")

        sys.stderr.flush()

        if m3u8_ is None:
            raise ValueError("No video found with the ID \"" +
                             urlparse.urlparse(url_).path[8:-1] + "\"")

        return self.__determineHDQualityMap(m3u8_)

    def __determineHDQualityMap(self, url):

        ffprobe = shutil.which("ffprobe")

        if ffprobe is None:
            raise RuntimeError("no ffprobe found")

        my_env = os.environ
        my_env['LC_ALL'] = "C"

        p = Popen([ffprobe, url], stdin=PIPE, stdout=PIPE, stderr=PIPE,
                  env=my_env)
        output, errout = p.communicate()
        lines = errout.split(b'\n')
        prog = -1

        for l in lines:
            if l[2:10] == b'Program ':
                prog += 1
            if l.find(b'1280x720') is not -1:
                break

        if prog is not -1:
            self._HDQualityMap = "-map p:" + str(prog) +\
                ":1 -map p:" + str(prog) + ":0"

        return url

    def __HDQualityMap(self):

        if self._HDQualityMap is None:
            return "-map p:1:1 -map p:1:0"
        else:
            return self._HDQualityMap

# kate: indent-mode: python
