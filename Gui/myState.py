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

class MyState(object):
    def __init__(self,astate):
        self.mystate=astate

    def on_enter(self, fromstate):
        pass

    def update(self):
        pass

    def on_leave(self, tostate):
        pass


class MyStateController(object):
    def __init__(self):
        self.mystate=None
        #self.mystatestr="undefined"
        self.mystates={}

    def add_state(self, astate):
        self.mystates[astate.mystate]=astate
        #self.mystatestr = str(astate.mystate)

    def change_state(self,newstatestr):
        if self.mystates.has_key(newstatestr):
            newstate=self.mystates[newstatestr]
            """
            if self.mystate == newstate:
                return
            """
            print "change State " + str(newstatestr)
            if self.mystate:
                self.mystate.on_leave(newstate)
                newstate.back = self.mystate
            newstate.on_enter(self.mystate)
            self.mystate=newstate
        else:
            print "State " + str(newstatestr) + " doesnt exists"
            #self.mystatestr = str(self.mystate)

    def change_state_back(self):
        if self.mystate.back:
            newstatestr= self.mystate.back.mystate
            if self.mystates.has_key(newstatestr):
                newstate=self.mystates[newstatestr]
                if self.mystate:
                    self.mystate.on_leave(newstate)
                newstate.on_enter(self.mystate)
                self.mystate=newstate
                #self.mystatestr = str(self.mystate)

    def update(self):
        if self.mystate:
            self.mystate.update()