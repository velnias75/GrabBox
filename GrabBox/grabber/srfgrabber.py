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
from urllib.error import HTTPError
import urllib.parse as urlparse
import urllib.request as urlreq
import datetime
import shlex
import json
import sys
import re


class SRFGrabber(AbstractHLSGrabber):

    __hd = True

    def __init__(self, url_, out_):
        super(SRFGrabber, self).__init__(url_, out_)

    def map(self):
        return "-map p:5" if self.__hd else "-map p:4"

    def url(self, quote=True):

        url_ = super(SRFGrabber, self).url(quote)
        parsed_ = urlparse.urlparse(shlex.split(url_)[0],
                                    allow_fragments=False)
        subs_ = False

        if not (parsed_ is None or not ("https" == parsed_.scheme or
                                        "http" == parsed_.scheme)):
            url_ = parsed_.query[3:]

        try:
            json_ = self.__getJSONFromUrl(url_)
        except json.JSONDecodeError:
            raise ValueError("Received invalid JSON data")
        except HTTPError:
            try:
                json_ = self.__getJSONFromUrl(url_[15:])
            except HTTPError:
                raise ValueError("No video found with the ID \"" + url_[15:] +
                                 "\"")

        if quote:
            try:
                for i in json_['chapterList'][0]['subtitleList']:
                    if "VTT" == i['format']:
                        sys.stderr.write("[I] VTT subtitle file found\n")
                        vtt_ = urlreq.urlopen(i['url']).read()
                        try:
                            f_ = open(self.out() + ".vtt", "wb")
                            f_.write(vtt_)
                            f_.close()
                            subs_ = True
                        except Exception:
                            sys.stderr.write("[W] writing subtitles failed\n")

            except KeyError:
                pass
        else:
            subs_ = True

        sys.stderr.write("[I] Grabbing from " +
                         json_['channel']['title'] + ": " +
                         json_['episode']['title'] + "\n")
        sys.stderr.write("[I] Duration: " +
                         str(datetime.
                             timedelta(milliseconds=json_['chapterList'][0]
                                       ['duration'])) + "\n")

        sys.stderr.flush()

        for i in json_['chapterList'][0]['resourceList']:
            if "HD" == i['quality'] and "HLS" == i['protocol']:
                self.__hd = True

                if not subs_:
                    self.__grabVTT(i['url'])

                sys.stderr.write("[I] Grabbing HD video …\n")
                sys.stderr.flush()

                return shlex.quote(i['url']) if quote else i['url']

        for i in json_['chapterList'][0]['resourceList']:
            if "SD" == i['quality'] and "HLS" == i['protocol']:
                self.__hd = False

                if not subs_:
                    self.__grabVTT(i['url'])

                sys.stderr.write("[I] Grabbing SD video …\n")
                sys.stderr.flush()

                return shlex.quote(i['url']) if quote else i['url']

        raise ValueError("Neither HD nor SD HLS video stream "
                         "found with ID \"" + url_ + "\"")

        return url_

    def __getJSONFromUrl(self, url_):
        return json.loads(urlreq.urlopen("https://il.srgssr.ch/"
                                         "integrationlayer/2.0/"
                                         "mediaComposition/byUrn/"
                                         "urn:srf:video:" + url_ +
                                         ".json").read())

    def __getVTTSegment(self, url_):

        rsp = urlreq.urlopen(url_)
        vtt = rsp.read().decode("utf-8")

        return (vtt.replace("WEBVTT\n\n", "") + '\n').encode("utf-8")

    def __grabVTT(self, url_):

        pat = re.compile("([^:]+)://.*&caption=([^:&]+).*"
                         "&webvttbaseurl=([^&]*)")
        mat = pat.match(url_)

        if mat:

            vurl = mat.group(1) + "://" + mat.group(3) + "/" + mat.group(2)
            surl = vurl[:vurl.rindex('/')] + "/"

            sys.stderr.write("[I] VTT subtitle stream found.\n" +
                             "[I] Downloading from " + vurl + "\n")
            sys.stderr.flush()

            vre = re.compile(".*\.vtt")
            rsp = urlreq.urlopen(vurl)

            try:
                f_ = open(self.out() + ".vtt", "wb")
                f_.write("WEBVTT\n\n".encode("utf-8"))

                for line in rsp.read().decode("utf-8").splitlines():
                    if vre.match(line):
                        f_.write(self.__getVTTSegment(surl + line))

                f_.close()

                sys.stderr.write("[I] VTT subtitles downloaded to " +
                                 self.out() + ".vtt" + "\n")
                sys.stderr.flush()

            except Exception as ex:
                sys.stderr.write("[W] writing subtitles failed: " + str(ex) +
                                 "\n")

# kate: indent-mode: python
