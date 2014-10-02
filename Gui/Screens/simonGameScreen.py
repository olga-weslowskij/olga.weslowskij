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
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Game.myLogHandler import infoLog
from Gui.Screens.aViewNotesScreen import AViewNotesScreen
from myglobals import ScreenState
from Requests import SimonRequests
import myglobals


class SimonGameScreen(AViewNotesScreen):
    def __init__(self):
        super(SimonGameScreen,self).__init__()
        self.mystate = "SimonGameScreen"
        self.pianoSimonGame=None

    def on_enter(self, tostate):
        super(SimonGameScreen,self).on_enter(tostate)
        # wrong place
        if myglobals.SimonMode is None:
            myglobals.gameState.initGame()
        if myglobals.SimonMode.activeChallenge() is None:
            myglobals.SimonMode.initSimonChallenges()

        if myglobals.SimonMode.config is False:
            myglobals.SimonMode.initSimonChallenges()

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


        def callbackplay7(instance):
            SimonRequests.playNewPart()

        btn7 = Button(text='Play new\nChords again')
        btn7.speed = 1.0
        btn7.bind(on_press=callbackplay7)
        btnbar.add_widget(btn7)


        def callbackplay9(instance):
            SimonRequests.playNewPartArp()

        btn9 = Button(text='Play new\nChord\nArpeggio')
        btn9.speed = 1.0
        btn9.bind(on_press=callbackplay9)
        btnbar.add_widget(btn9)

        btn11 = Button(text='Show new Chords')
        btn11.mystate = "Simon"

        def callbackplayShowChallengeNewpart(instance):

            ## debug
            #ScreenState["Song"].levcha.draw()
            SimonRequests.ShowChallenge(newpart=True)
            #ScreenState.change_state("Simon")


        btn11.bind(on_press=callbackplayShowChallengeNewpart)
        btnbar.add_widget(btn11)



        def callbackplay8(instance):
            SimonRequests.playChallenge()
            #ScreenState["Song"].challenge.replay()

        btn8 = Button(text='Play\nChallenge again')
        btn8.speed = 1.0
        btn8.bind(on_press=callbackplay8)
        btnbar.add_widget(btn8)


        def callbackplayShowChallenge(instance):

            ## debug
            #ScreenState["Song"].levcha.draw()
            SimonRequests.ShowChallenge()
            #ScreenState.change_state("Simon")

        btn = Button(text='Show Challenge')
        btn.mystate = "Simon"

        btn.bind(on_press=callbackplayShowChallenge)
        btnbar.add_widget(btn)




        def callbackplay81(instance):
            SimonRequests.playChallenge(part = "olgapartStream")
            #ScreenState["Song"].challenge.replay()

        btn81 = Button(text='Play Challenge \nand Pre Part again')
        btn81.speed = 1.0
        btn81.bind(on_press=callbackplay81)
        btnbar.add_widget(btn81)


        def callbackplayShowChallenge81(instance):
            ## debug
            #ScreenState["Song"].levcha.draw()
            SimonRequests.ShowChallenge(part="olgapartStream")

            #ScreenState.change_state("Simon")

        btn811 = Button(text='Show Challenge\n and Pre Part')
        btn811.mystate = "Simon"

        btn811.bind(on_press=callbackplayShowChallenge81)
        btnbar.add_widget(btn811)


        def callbackplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            self.notesscroller.play()

        btn4 = Button(text='Play\nselected\nChords')
        btn4.speed = 1.0
        btn4.bind(on_press=callbackplay)
        btnbar.add_widget(btn4)




        def callbackplayComputeBestRating(instance):
            SimonRequests.createShowDoneStream(None)

        btn2 = Button(text='Show last\ndone Challenge')
        btn2.mystate = "SimonViewDoneScreen"
        btn2.bind(on_press=changeStateCallback)
        btnbar.add_widget(btn2)


        def callbackplayAtyourSpeed(instance):

            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            #if ScreenState["Timing"].notesscroller.rating:
            #    ScreenState["Song"].challenge.replay(speed = ScreenState["Timing"].notesscroller.rating.medrelativespeed)

            ScreenState.change_state("SimonViewGraphScreen")
            ScreenState["SimonViewGraphScreen"].dirty=True

        btn5 = Button(text='Replay Challenge\n At your last\n measured speed (show Graph) ')
        btn5.speed = 1.0
        btn5.bind(on_press=callbackplayAtyourSpeed)
        btnbar.add_widget(btn5)



        def callbackplayComputeError(instance):
            #SimonRequests.createShowErrorStream(myglobals.SimonMode.activeChallenge().challenge)
            ScreenState.change_state(instance.mystate)

        """
        btn10 = Button(text='Show best Try')
        btn10.mystate = "SimonViewMissingScreen"
        btn10.bind(on_press=callbackplayComputeError)
        btnbar.add_widget(btn10)
        """


        btn102 = Button(text='Show last\nerror')
        btn102.mystate = "SimonViewErrorScreen"
        btn102.bind(on_press=callbackplayComputeError)
        btnbar.add_widget(btn102)


        def callbackplayComputeBestActiveRating(instance):
            #SimonRequests.createShowBestActiveStream(None)
            ScreenState.change_state("SimonViewBestActiveScreen")

        btn11 = Button(text='Show best active\nrating')
        #btn11.mystate = "nowTiming"
        btn11.bind(on_press=callbackplayComputeBestActiveRating)
        btnbar.add_widget(btn11)

        def callback14(instance):
            ScreenState.mystate.dirty = True
            ScreenState.updateGui()


        btn14 = Button(text='update\nGui')
        btn14.bind(on_press=callback14)
        btnbar.add_widget(btn14)



        def callbackreplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            #s = self.notesscroller.getStream()
            s = self.notesscroller.adapter.getStream()
            s.shift(0 - s[0].myoffset)
            myglobals.gameState.input.replay(s)

        btn41 = Button(text='ReInput\nselected\nChords')
        btn41.speed = 1.0
        btn41.bind(on_press=callbackreplay)
        btnbar.add_widget(btn41)


        btn3 = Button(text='Show Chords\nyou\nplayed')
        btn3.mystate = "SimonViewInScreen"
        btn3.bind(on_press=changeStateCallback)
        btnbar.add_widget(btn3)


        def callbackconfig(instance):
             myglobals.ScreenState['ConfigObjectScreen'].object = myglobals.gameState.SimonMode
             myglobals.ScreenState['ConfigObjectScreen'].debug = False
             myglobals.ScreenState.change_state('ConfigObjectScreen')


        btn6 = Button(text='Config')
        btn6.bind(on_press=callbackconfig)
        btnbar.add_widget(btn6)

        btnOlgasDuty = Button(text='OlgasDuty')
        btnOlgasDuty.mystate = "OlgasDuty"
        btnOlgasDuty.bind(on_press=changeStateCallback)
        btnbar.add_widget(btnOlgasDuty)

        return btnbar


"""
    def update(self):
        pass

    def updateGui(self):
        pass

    def build(self):
        pass
"""






