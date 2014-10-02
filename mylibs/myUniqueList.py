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

import logging
#from mylibs.myList import MyList

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

class MyUniqueList(list):
#class MyUniqueList(MyList):
    def __init__(self, *args, **kwargs):
        #super(MyList,self).__init__(*args, **kwargs)
        list.__init__(self, *args, **kwargs)
        self.seen = set()
        self.key=lambda x: x


    def append(self, p_object):
        pkey = self.key(p_object)
        if pkey in self.seen:
            return
        list.append(self,p_object)
        self.seen.add(pkey)

    def items(self):
        return list(enumerate(self))


