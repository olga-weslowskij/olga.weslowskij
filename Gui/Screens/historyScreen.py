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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from Gui.Screens.aViewNotesScreen import AViewNotesScreen
from myglobals import ScreenState
from Gui.Widgets.viewStream2Widget import ViewStream2Widget

from Game.mySong import MySong

import myglobals


class HistoryScreen(AViewNotesScreen):
    def __init__(self):
        super(HistoryScreen,self).__init__()
        self.mystate = "History"
        self.pianoSimonGame=None
        self.donelen = 0

        self.lastshownevent=None

        self.notesscroller=ViewStream2Widget()

    def on_enter(self, tostate):
        super(HistoryScreen, self).on_enter(tostate)
        #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)

        print self.mystate


    def update(self):
        #print str(myglobals.HistoryMode.todaystream[-1]) + " != " + str(self.lastshownevent)
        #if len(myglobals.HistoryMode.todaystream) > len(self.shownnotes):
        try:
            curevent= myglobals.HistoryMode.todaystream[-1]
        except:
            curevent=None
        if self.lastshownevent != curevent:
            self.dirty = True
        super(HistoryScreen,self).update()




    def updateGui(self):
     #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)
        print "updating History"

        if myglobals.HistoryMode:
            print "updating History 1"
            if self.notesscroller.toshow is None:
                print "updating History 2"
                self.notesscroller.toshow=myglobals.HistoryMode.todaystream

        self.notesscroller.updateGui()
        try:
            curevent= myglobals.HistoryMode.todaystream[-1]
        except:
            curevent=None
        self.lastshownevent = curevent

    #def add2btnbar(self):
    def buildbtnbar(self):

        if self.btnbar is None:
            self.btnbar=GridLayout(cols=7, size_hint=(1,0.2))

        def saveStateSongCallback(instance):
            if self.notesscroller.toshow:
                s = MySong()
                st = self.notesscroller.adapter.getStream()
                st.shift(0 - st[0].myoffset)
                st.song = s
                s.mystream = st
                s.toXml2file("Song.xml")

        btnsave = Button(text='Save selected\n Chords to\nSong.xml')
        btnsave.bind(on_press=saveStateSongCallback)
        self.btnbar.add_widget(btnsave)

        def setSongStateSongCallback(instance):
            if self.notesscroller.toshow:
                s = MySong()

                st = self.notesscroller.adapter.getStream()

                st.song = s
                s.mystream = st
                #s.toXml2file("Song.xml")
                myglobals.gameState.song = s

        btnsave = Button(text='Set selected\n Chords as\nSong')
        btnsave.bind(on_press=setSongStateSongCallback)
        self.btnbar.add_widget(btnsave)

        super(HistoryScreen,self).buildbtnbar()

        return self.btnbar


    def build(self):
        super(HistoryScreen,self).build()
        #self.add2btnbar()
        """
        def saveStateCallback(instance):
            if self.notesscroller.stream:
                self.notesscroller.stream.toXml2file("Stream.xml")

        btnsave = Button(text='Save to\nStream.xml')
        btnsave.bind(on_press=saveStateCallback)
        self.btnbar.add_widget(btnsave)
        """


        pass


    def buildAll(self, astateName, anotesscroller):
        self.widget = BoxLayout(orientation='vertical')


        self.notesscroller = anotesscroller

        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True
        self.widget.add_widget(self.notesscroller)

        self.mystate=astateName

        ScreenState.add_state(self)

        #btnbar=GridLayout(cols=8, size_hint=(1,0.2))
        #btnbar=GridLayout(cols=7, size_hint=(1,0.2))
        self.btnbar = self.buildbtnbar()
        self.widget.add_widget(self.btnbar)

        #self.add2btnbar()



