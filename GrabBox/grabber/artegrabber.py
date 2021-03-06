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

# https://api.arte.tv/api/player/v1/config/de/089938-000-A

from GrabBox.grabber.abstractgrabber import AbstractGrabber
from urllib.error import HTTPError
import urllib.request as urlreq
import datetime
import shutil
import shlex
import json
import sys
import re


class ArteGrabber(AbstractGrabber):

    __dlUrls = []
    __url = None

    def __init__(self, url_, out_):
        super(ArteGrabber, self).__init__(url_, out_)

        pat = re.compile(".*/videos/([^/]+).*", re.I)
        mat = pat.match(url_)
        dsq = False
        fhq = False

        if mat:
            url = "https://api.arte.tv/api/player/v1/config/de/" + mat.group(1)
        else:
            raise ValueError("Invalid arte video url")

        try:
            json_ = json.loads(urlreq.urlopen(url).read())

            sys.stderr.write("[I] Grabbing from arte: " +
                             json_['videoJsonPlayer']['VTI'] + "\n")
            sys.stderr.write("[I] Duration: " +
                             str(datetime.timedelta(
                                 seconds=json_['videoJsonPlayer']
                                 ['videoDurationSeconds'])) + "\n")

            for vsr in json_['videoJsonPlayer']['VSR'].keys():
                try:
                    if vsr.index('HTTPS_SQ') == 0 \
                        and ("DE" == json_['videoJsonPlayer']['VSR'][vsr]
                             ['versionShortLibelle']) \
                        and (("VA" == json_['videoJsonPlayer']['VSR'][vsr]
                             ['versionCode']) or
                             ("VA-STA" == json_['videoJsonPlayer']['VSR']
                                 [vsr]['versionCode']) or
                             ("VOA" == json_['videoJsonPlayer']['VSR']
                                 [vsr]['versionCode'])):
                        self.__url = \
                            json_['videoJsonPlayer']['VSR'][vsr]['url']
                        self.__dlUrls.append((self.__url, "SQ_" +
                                              json_['videoJsonPlayer']['VSR']
                                              [vsr]['versionShortLibelle']))
                        sys.stderr.write("[I] Found HD-" +
                                         (json_['videoJsonPlayer']['VSR'][vsr]
                                          ['versionLibelle']) +
                                         " (" + json_['videoJsonPlayer']
                                         ['VSR'][vsr]['versionShortLibelle'] +
                                         ")\n")
                        dsq = True
                except ValueError:
                    pass

                try:
                    if not fhq and vsr.index('HTTPS_HQ') == 0 and \
                        ("FR" == json_['videoJsonPlayer']['VSR'][vsr]
                         ['versionShortLibelle'] or
                         "OmU" == json_['videoJsonPlayer']['VSR'][vsr]
                         ['versionShortLibelle']):

                        self.__dlUrls.append((json_['videoJsonPlayer']['VSR']
                                              [vsr]['url'], "HQ_" +
                                              json_['videoJsonPlayer']['VSR']
                                              [vsr]['versionShortLibelle']))
                        sys.stderr.write("[I] Found SD-" +
                                         (json_['videoJsonPlayer']['VSR'][vsr]
                                          ['versionLibelle']) +
                                         " (" + json_['videoJsonPlayer']
                                         ['VSR'][vsr]['versionShortLibelle'] +
                                         ")\n")
                        fhq = True
                except ValueError:
                    pass

            if not dsq:
                for vsr in json_['videoJsonPlayer']['VSR'].keys():
                    try:
                        if vsr.index('HTTPS_SQ') == 0 \
                            and ("OmU" == json_['videoJsonPlayer']['VSR'][vsr]
                                 ['versionShortLibelle']):
                            self.__url = \
                                json_['videoJsonPlayer']['VSR'][vsr]['url']
                            self.__dlUrls.append((self.__url, "SQ_" +
                                                  json_['videoJsonPlayer']
                                                  ['VSR'][vsr]
                                                  ['versionShortLibelle']))
                            sys.stderr.write("[I] Found HD-" +
                                             (json_['videoJsonPlayer']
                                              ['VSR'][vsr]['versionLibelle']) +
                                             " (" + json_['videoJsonPlayer']
                                             ['VSR'][vsr]
                                             ['versionShortLibelle'] + ")\n")
                    except ValueError:
                        pass

        except json.JSONDecodeError:
            raise ValueError("Received invalid JSON data")
        except HTTPError:
            raise ValueError("No video found at URL \"" + url_ + "\"")

        sys.stderr.flush()

        if len(self.__dlUrls) == 0:
            raise ValueError("No matching videos found")
        elif self.__url is None:
            self.__url = self.__dlUrls[0][0]
            for v in self.__dlUrls:
                try:
                    if v[1].index("OmU"):
                        self.__url = v[0]
                        break
                except ValueError:
                    pass

    def ext(self):
        return ".mp4"

    def url(self, quote=True):
        return super(ArteGrabber, self).url(quote) if quote else self.__url

    def cmd(self):

        urls_ = []

        for t in self.__dlUrls:
            urls_.append(shutil.which('sh') + " -c " +
                         shlex.quote(shutil.which('wget') +
                         " -t0 -c -O \"" + (self.out() + '_' + t[1] +
                                            self.ext()) + "\" " + t[0]))

        return "; ".join(urls_)

# kate: indent-mode: python
