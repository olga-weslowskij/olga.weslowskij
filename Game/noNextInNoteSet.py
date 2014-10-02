# Copyright (C) weslowskij
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import heapq

import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)
logger.setLevel(logging.DEBUG)


def expectedNoteTime(a):
    if a.nextKnownNoteDeltaTimeLastGood() is None:
        return -1
    if a.rspeed():
        return a.nextKnownNoteDeltaTimeLastGood() / a.rspeed()
    else:
        return a.nextKnownNoteDeltaTimeLastGood() / 0.1

class NoNextInNoteSet(object):
    def __init__(self, old=None):
        if old is None:
            self.expectedtimeheap=[]
            self.set = {}
        else:
            self.expectedtimeheap=list(old.expectedtimeheap)
            self.set = dict(old.set)
        pass

    def add(self,o):
        if self.set.has_key(o):
            return
        heapq.heappush(self.expectedtimeheap,(expectedNoteTime(o),o))
        self.set[o]=o
        #logger.debug("pusching " + str(expectedNoteTime(o)))
        pass


    def getLongestTime(self):
        if len(self.expectedtimeheap)>0:
            #logger.debug("longestTime" + str(self.expectedtimeheap[0][1]))
            return self.expectedtimeheap[0][1]
        else:
            return None
        pass

    def keys(self):
        return self.set.keys()

    def values(self):
        return self.set.values()

    def __len__(self):
        return len(self.set)