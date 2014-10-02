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
from Gui.Screens.configAChallengeStreamScreen import ConfigAChallengeStreamScreen
from Gui.Widgets.viewStream2Widget import ViewStream2Widget

from myglobals import ScreenState


import myglobals

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)



class OlgaViewChallengeScreen(ConfigAChallengeStreamScreen):
    def __init__(self):
        super(OlgaViewChallengeScreen,self).__init__()
        self.mystate = self.__class__.__name__
        self.notesscroller= ViewStream2Widget()
        self.challenge=None

    def on_enter(self, tostate):
        """
        if self.song is None:
            self.song  = myglobals.OlgaMode.song

            # chords
            self.notesscroller.song= self.song#.getHand(hands).chordify()
            #self.notesscroller.stream = self.song.mystream.getHand(hands).chordify()
            #ScreenState["Song"].notesscroller.stream=self.challengestream
            #notes
            #ScreenState["Song"].notesscroller.stream=myKnownNotes.notes
        """

        super(OlgaViewChallengeScreen,self).on_enter(tostate)

    def update(self):
        # poor mans init
        if self.challenge is None and myglobals.OlgaMode.challenge:
            self.challenge = myglobals.OlgaMode.challenge
            self.dirty = True


        if self.challenge:
            self.notesscroller.toshow = self.challenge.jumpToStates.knownStreams[0]


    def updateGui(self):
        self.notesscroller.updateGui()


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
        def callback14(instance):
            ScreenState.mystate.dirty = True
            ScreenState.updateGui()


        btn14 = Button(text='update\nGui')
        btn14.bind(on_press=callback14)
        self.btnbar.add_widget(btn14)



        def callbackplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            self.notesscroller.play()

        btn4 = Button(text='Play\nselected\nChords')
        btn4.speed = 1.0
        btn4.bind(on_press=callbackplay)
        self.btnbar.add_widget(btn4)

        def callbackreplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            #s = self.notesscroller.getStream()
            s = self.notesscroller.adapter.getStream()
            s.shift(0 - s[0].myoffset)
            myglobals.gameState.input.replay(s)

        btn41 = Button(text='ReInput\nselected\nChords')
        btn41.speed = 1.0
        btn41.bind(on_press=callbackreplay)
        self.btnbar.add_widget(btn41)


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

        #self.btnbar.add_widget(btn)









