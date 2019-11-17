#
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

from GrabBox.grabber.grabberfactory import GrabberFactory
from argparse import RawTextHelpFormatter
import argparse
import sys


def main():

    parser = argparse.ArgumentParser(description='GrabBox grabs videos from '
                                     'various sources.',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument("source", help="source to grab stream from\n"
                        "Available sources: " + GrabberFactory().sources())
    parser.add_argument("url", help="URL of the stream")
    parser.add_argument("out", help="output filename")
    parser.add_argument("map", nargs='?', help="map option for generic source",
                        default=None)

    args = parser.parse_args()

    try:
        sys.stderr.write("[I] GrabBox v0.7 - (c) 2019 by Heiko Schäfer "
                         "(heiko@rangun.de)\n")
        sys.stderr.flush()
        GrabberFactory(args).grab()
    except Exception as e:
        print("[E] " + str(e))


if __name__ == "__main__":
    main()

# kate: indent-mode: python
