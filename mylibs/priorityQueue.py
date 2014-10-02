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
import operator

from bintrees import FastAVLTree

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class PriorityQueue(object):
    """ Combined priority queue and set data structure. Acts like
        a priority queue, except that its items are guaranteed to
        be unique.

        Provides O(1) membership test, O(log N) insertion and
        O(log N) removal of the smallest item.

        Important: the items of this data structure must be both
        comparable and hashable (i.e. must implement __cmp__ and
        __hash__). This is true of Python's built-in objects, but
        you should implement those methods if you want to use
        the data structure for custom objects.
    """
    def __init__(self, items=[], key = None , maxitems=None, maxkey=None):
        """ Create a new PriorityQueueSet.

            items:
                An initial item list - it can be unsorted and
                non-unique. The data structure will be created in
                O(N).
        """
        if key == None:
            self.key=lambda  x: x
        else:
            self.key=key

        self.tree = FastAVLTree()
        #self.tree = AVLTree()

        self.maxitems = maxitems
        self.maxkey = maxkey

        for x in items:
            self.add(x)



    def has_item(self, item):
        """ Check if *item* exists in the queue
        """
        return bool(self.tree.get(self.key(item), False))

    def pop_smallest(self):
        return self.tree.pop_min()


    def peek(self, d = None):
        try:
            return self.tree.min_item()[1]
        except:
            return d

    def __setitem__(self, key, value):
        self.tree[self.key(key)]=value

    def __getitem__(self, item):
        return self.tree[self.key(item)]


    # updateing by removing and reinserting
    # i cant find a anode by object ??
    # i hate your data structures ... index in O(n) :(
    def update(self, item):
        itemsbykey = self.tree[self.key(item):self.key(item)]
        del self.tree[self.key(item):self.key(item)]
        for x in itemsbykey:
            #if not (x is item):
            self.add(x)



    def add(self, item):
        """ Add *item* to the queue. The item will be added only
            if it doesn't already exist in the queue.
        """
        #print "PriorityQue add  " + str(item)
        if self.maxkey and self.key(item) > self.maxkey:
            return

        if self.tree.get(self.key(item), None) is None:
            self.tree[self.key(item)]=item

        # sholdnt it be pop biggest??? [yes we need a tree]
        if self.maxitems and self.tree.__len__() > self.maxitems:
            self.tree.pop_max()

        #print "PriorityQue add peek " + str(self.peek())

    def prettyprint(self):
        pp = operator.methodcaller('prettyprint')
        return "".join(map(pp,self.tree.values()))

    """
    @property
    def list(self):
        return list(self.tree.values())
    """