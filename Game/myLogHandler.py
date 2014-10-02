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
from kivy.properties import StringProperty
from myglobals import ScreenState
import myglobals
from mylibs.myUniqueList import MyUniqueList


letmereadit= 2000

class InfoLog(object):
    # im too blind to see how this should be done easy with the logging module..
    def __init__(self):
        self.handlers=MyUniqueList()
        self.queue = []
        # -1 the last, -2 ...
        self.pos=-1

        self.lastautoupdate=None
        self.lastautoupdatepos=0


    def log(self, atxt):
        #print atxt
        self.queue.append(atxt)
        self.update()


    def error(self, atxt):
        #print atxt
        for x in self.handlers:
            #print x
            x.error = atxt





    def update(self):
        #print "autoupdate pre" , str(self.pos), str(len(self.queue)) ,str (self.lastautoupdatepos)
        if self.pos==-1 and len(self.queue) > self.lastautoupdatepos:
            time = myglobals.gameState.getMidiTick()
            #print "autoupdate 1"
            if self.lastautoupdate:
                #print "autoupdate 2", str(time - self.lastautoupdate)
                if time - self.lastautoupdate > letmereadit:
                    #print "autoupdate done"
                    self.lastautoupdatepos=self.lastautoupdatepos +1
                    self.lastautoupdate=time
                    self.update_listeners(apos = self.lastautoupdatepos-1)

            else:
                #print "autoupdate None"
                self.lastautoupdate=time
                self.lastautoupdatepos=self.lastautoupdatepos +1
                self.update_listeners(apos = self.lastautoupdatepos-1)



    def update_listeners(self, apos = None):
        pos = self.pos
        if self.pos >= -1:
            self.pos = -1
            pos = -1

        if self.pos < -len(self.queue) and self.pos != -1:
            self.pos = -len(self.queue)
            pos = self.pos


        if apos:
            pos = apos


        if pos > len(self.queue):
            pos = -1

        if pos < -len(self.queue):
            pos = 0

        #print "infolog.pos:" +str(self.pos) , "pos " +str(pos), str(self.queue[pos])


        for x in self.handlers:
            try:
                x.text = self.queue[pos]
            except:
                pass


    def setPos(self, apos):
        self.pos= apos
        self.update_listeners()





infoLog = InfoLog()