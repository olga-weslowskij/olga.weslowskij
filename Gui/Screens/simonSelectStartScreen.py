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
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Gui.Screens.aViewNotesScreen import AViewNotesScreen
from myglobals import ScreenState
from Gui.Widgets.viewStream2Widget import ViewStream2Widget
import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


class SimonSelectStartScreen(AViewNotesScreen):
    def __init__(self):
        super(SimonSelectStartScreen,self).__init__()
        self.song = None
        self.mystate = self.__class__.__name__
        self.notesscroller = ViewStream2Widget()
        """
        self.notesscroller = Label()
        self.notesscroller.text="CAN you see me??"
        self.notesscroller.toshow=None
        """
        #self.notesscroller = ViewSongWidget()


    def on_enter(self, tostate):
        print self.__class__.__name__
        super(SimonSelectStartScreen,self).on_enter(tostate)


    def updateGui(self):
        #super(SimonSelectStartScreen, self).updateGui()
        self.notesscroller.updateGui()
        pass

    def update(self):

        if self.song is None:
            self.song = myglobals.SimonMode.song

        if self.notesscroller.toshow is None:
            self.notesscroller.toshow= self.song.mystream
            # testing view Song Widget
            self.notesscroller.song = self.song
            self.dirty=True


        super(SimonSelectStartScreen, self).update()


    def build(self):
        super(SimonSelectStartScreen,self).build()



    def buildbtnbar(self):
        self.btnbar=GridLayout(cols=3, size_hint=(1,0.2))

        """
        def declareChallengeBtnCallback(instance):

            rl=self.notesscroller.getStreamAndIntervall()
            ret = _newChallenge2(rl[0],rl[1],rl[2])
            print "declareChallengeBtnCallback " + str(ret)


        btn13 = Button(text='Declare\n Challenge')
        btn13.mystate = self.mystate
        btn13.bind(on_press=declareChallengeBtnCallback)
        self.btnbar.add_widget(btn13)
        """


        def declareStartBtnCallback(instance):
            anote = self.notesscroller.adapter._selectedBtn[0].myStreamNote
            myglobals.SimonMode.startchord= anote.chord
            ScreenState.change_state_back()
            #myglobals.SimonMode.initSimonChallenges(anote)
            pass



        btn13 = Button(text='Start learning here')
        btn13.mystate = self.mystate
        btn13.bind(on_press=declareStartBtnCallback)
        self.btnbar.add_widget(btn13)


        def callbackplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            self.notesscroller.play()

        btn4 = Button(text='Play\nselected\nChords')
        btn4.speed = 1.0
        btn4.bind(on_press=callbackplay)
        self.btnbar.add_widget(btn4)



        def callback(instance):
            ScreenState.change_state_back()

        btn = Button(text='Back')
        btn.bind(on_press=callback)
        self.btnbar.add_widget(btn)



        def changeStateCallback(instance):
            ScreenState.change_state(instance.mystate)

        btnOlgasDuty = Button(text='OlgasDuty')
        btnOlgasDuty.mystate = "OlgasDuty"
        btnOlgasDuty.bind(on_press=changeStateCallback)
        self.btnbar.add_widget(btnOlgasDuty)

        return self.btnbar








