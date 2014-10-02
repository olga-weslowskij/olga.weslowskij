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
from myglobals import ScreenState
from Gui.Screens.viewARunScreen import ViewARunScreen
from Gui.Widgets.viewRunWidget import ViewRunWidget
from Requests import OlgaRequests

from mylibs.myDict import MyDict
import myglobals


logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)



class OlgaViewErrorScreen(ViewARunScreen):
    def __init__(self):
        super(OlgaViewErrorScreen,self).__init__()
        self.mystate = "OlgaViewErrorScreen"
        self.pianoSimonGame=None
        self.donelen = 0

        self.shownMelodyRun=None

        self.shownKivyNoteMap=[]
        self.shownMelodyRating=MyDict()
        self.shownMelodyRating.defaultNone=True

        self.shownpos ={}
        self.shownpos[0]=0
        self.shownpos[1]=0

        self.notesscroller = ViewRunWidget()

    def buildAll(self, astateName, anotesscroller):
        #super(OlgaViewErrorScreen,self).buildAll(astateName, ViewRunAdapter())
        super(OlgaViewErrorScreen,self).buildAll(astateName, self.notesscroller)

    def on_enter(self, tostate):
        super(OlgaViewErrorScreen, self).on_enter(tostate)
        #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)


    def updateGui(self):
        self.notesscroller.updateGui()


    def update(self):
        #print "update olgaViewErrorScreen"
        #print str(len(myglobals.HistoryMode.todaystream)) + " > " + str(len(self.shownKivyNoteMap))
        if myglobals.OlgaMode.challenge:
            if self.shownMelodyRun is None or self.shownMelodyRun != myglobals.OlgaMode.challenge.bestabsrun:
                self.notesscroller.toshow = myglobals.OlgaMode.challenge.bestabsrun
                self.dirty = True

        # includes notesscroller.updateGui() via screenstate
        # super(OlgaViewErrorScreen,self).update()

    def buildbtnbar(self):
        btnbar=GridLayout(cols=7, size_hint=(1,0.2))

        def changeStateCallback(instance):
            ScreenState.change_state(instance.mystate)


        def callbackplay70(instance):
            #main.console()
            myglobals.gameState.console = True



        btn70 = Button(text='Console')

        btn70.bind(on_press=callbackplay70)
        btnbar.add_widget(btn70)




        """
        def callbackplay8(instance):
            OlgaRequests.playChallenge()
            #ScreenState["Song"].challenge.replay()

        btn8 = Button(text='Play\nChallenge again')
        btn8.speed = 1.0
        btn8.bind(on_press=callbackplay8)
        btnbar.add_widget(btn8)
        """


        def callback14(instance):
            ScreenState.mystate.dirty = True
            ScreenState.updateGui()


        btn14 = Button(text='update\nGui')
        btn14.bind(on_press=callback14)
        btnbar.add_widget(btn14)



        def callbackplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            self.notesscroller.play()
            # play and save
            s = self.notesscroller.adapter.getStream()
            s.toXml2file("play.xml")

        btn4 = Button(text='Play\nselected\nChords')
        btn4.speed = 1.0
        btn4.bind(on_press=callbackplay)
        btnbar.add_widget(btn4)


        btn = Button(text='Show \ncontrol part')
        btn.mystate = "Simon"

        def callbackplayShowChallenge(instance):

            ## debug
            #ScreenState["Song"].levcha.draw()
            OlgaRequests.ShowChallenge()
            #ScreenState.change_state("Simon")


        btn.bind(on_press=callbackplayShowChallenge)
        btnbar.add_widget(btn)


        def callbackSetChallenge(instance):
            OlgaRequests.SetChallenge()

        btn6 = Button(text='Set \ncontrol part')
        btn6.mystate = "ConfigAChallengeStreamScreen"
        btn6.bind(on_press=callbackSetChallenge)
        btnbar.add_widget(btn6)



        def callbackplayAtyourSpeed(instance):

            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            #if ScreenState["Timing"].notesscroller.rating:
            #    ScreenState["Song"].challenge.replay(speed = ScreenState["Timing"].notesscroller.rating.medrelativespeed)

            ScreenState["SimonViewGraphScreen"].challenge = myglobals.OlgaMode.challenge
            ScreenState.change_state("SimonViewGraphScreen")
            ScreenState["SimonViewGraphScreen"].dirty=True

        btn5 = Button(text='show Graph ')
        btn5.bind(on_press=callbackplayAtyourSpeed)
        btnbar.add_widget(btn5)

        btn61 = Button(text='Config Olga')
        btn61.bind(on_press=OlgaRequests.ConfigChallenge)
        btnbar.add_widget(btn61)


        btnOlgasDuty = Button(text='OlgasDuty')
        btnOlgasDuty.mystate = "OlgasDuty"
        btnOlgasDuty.bind(on_press=changeStateCallback)
        btnbar.add_widget(btnOlgasDuty)




        return btnbar






