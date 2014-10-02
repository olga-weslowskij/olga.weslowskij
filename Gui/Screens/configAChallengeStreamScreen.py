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
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Gui.Screens.aViewNotesScreen import AViewNotesScreen, SelectNotes
from Gui.Widgets.kivyNoteMap import KivyNoteMap
from Game.myJumpChordsAndSpeedTols import MyJumpChordsAndSpeedTols
from myglobals import ScreenState
from Gui.Widgets.viewStream2Widget import ViewStream2Widget

import myglobals
from Game.options import getOptionValue

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class ViewNotesSongWidget(SelectNotes, SimpleListAdapter):

    def __init__(self):
        self.stream=None
        self.kivybtn={}
        self.build()

    def build(self):
        SelectNotes.build(self)
        self.widget = GridLayout(cols=10, size_hint_y=None)
        self.widget.bind(minimum_height=self.widget.setter('height'))
        return self.widget

    def updateGui(self):
        print "update ViewRunWidget\n"
        self.data= range(len(self.stream))
        return

    def buildkivyMelodyRating(self, index):

        x = self.stream[index]
        btn = KivyNoteMap()

        btn.build(x)


        btn.progress.value=1
        btn.speed.text=str(x)
        btn.add_widget(btn.chord)
        btn.chord.bind(on_press=self.selectBtn)
        btn.add_widget(btn.myoffset)
        btn.add_widget(btn.myduration)
        btn.add_widget(btn.myvolume)


        #btn.add_widget(btn.myoffset)

        #self.widget.add_widget(btn)

        return btn


    def get_view(self, index):
        if self.stream is None:
            return  None
        if len (self.stream) == 0:
            return None

        if index >= len(self.stream):
            return None

        if self.kivybtn.has_key(self.stream[index]):
            return self.kivybtn[self.stream[index]]
        else:
            self.kivybtn[self.stream[index]] = self.buildkivyMelodyRating(index)
            return self.kivybtn[self.stream[index]]





    """
    def get_view(self, index):
        if len (self.data) == 0:
            return None

        if index >= len(self.data):
            return None

        #return self.buildkivyMelodyRating(index)

        #print self.stream[-1].prettyprint()
        return self.data[index]
    """

class ConfigAChallengeStreamScreen(AViewNotesScreen):
    def __init__(self):
        super(ConfigAChallengeStreamScreen,self).__init__()
        self.challenge = None
        #self.song = None


    def on_enter(self, tostate):
        hands = getOptionValue("hand")

        print "ConfigAChallengeScreen"

        if self.notesscroller.toshow is None:
            self.notesscroller.toshow = myglobals.gameState.song.mystream

            #self.song  = myglobals.OlgaMode.song

            # chords
            #self.notesscroller.song= self.song

            #print "ConfigAChallengeScreen " + str(self.song)

            #.getHand(hands).chordify()
            #self.notesscroller.stream = self.song.mystream.getHand(hands).chordify()
            #ScreenState["Song"].notesscroller.stream=self.challengestream
            #notes
            #ScreenState["Song"].notesscroller.stream=myKnownNotes.notes

        super(ConfigAChallengeStreamScreen,self).on_enter(tostate)

        #code.interact(local=locals())


        """
    def update(self):
        pass
        """

    def updateGui(self):
        #self.notesscroller._trigger_reset_populate()
        self.notesscroller.updateGui()



    def buildbtnbar(self):
        self.btnbar=GridLayout(cols=3, size_hint=(1,0.2))


        """
        def declareChallengeBtnCallback(instance):
            rl=self.notesscroller.getStream()
            #newstream.build(rl[0][rl[1]], rl[0][rl[2]])
            nc = SimonModeChallengeFeedback()
            nc.createSimpleChallenge(rl[0],rl[-1])
            myglobals.SimonMode.simonModeChallenges.append(nc)

            print "declareChallengeBtnCallback"


        btn13 = Button(text='Set selected part\n as SimpleChallenge')
        btn13.mystate = "Song"
        btn13.bind(on_press=declareChallengeBtnCallback)
        self.btnbar.add_widget(btn13)
        """





        def declareStartBtnCallback(instance):
            rl=self.notesscroller.adapter.getList()
            #newstream.build(rl[0][rl[1]], rl[0][rl[2]])
            logger.info("self.challenge.jumpToStates.registerStream(rl) rl: " + str(rl))
            # clear old ones ??
            self.challenge.jumpToStates=MyJumpChordsAndSpeedTols()
            self.challenge.jumpToStates.registerStream(rl, myglobals.OlgaMode.challenge.speed, myglobals.OlgaMode.challenge.speedtol)


        btn131 = Button(text='Set selected part\n as StartNotes')
        #btn131 = Button(text='Declare\n Challenge')
        btn131.mystate = self.mystate
        btn131.bind(on_press=declareStartBtnCallback)
        self.btnbar.add_widget(btn131)


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



    def build(self, name = None):
        if not name:
            self.mystate = self.__class__.__name__
        else:
            self.mystate = name





        # super(OlgaViewChallengeScreen,self).build()

        #self.btnbar=GridLayout(cols=7, size_hint=(1,0.2))
        if not hasattr(self,"btnbar"):
            self.btnbar=None


        if self.btnbar is None:
            self.btnbar = self.buildbtnbar()


        if self.notesscroller is None:
            self.notesscroller = ViewStream2Widget()


        self.widget = BoxLayout(orientation='vertical')

        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True
        self.widget.add_widget(self.notesscroller)

        #self.notesscroller = anotesscroller
        #self.notesscroller.add_widget(self.notesscroller.widget)

        self.widget.add_widget(self.btnbar)

        ScreenState.add_state(self)









