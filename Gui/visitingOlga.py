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

import kivy
from Gui.Screens.ConfigObjectScreen import ConfigObjectScreen

from Gui.Screens.MidiConfigScreen import MidiConfigScreen
from Gui.Screens.OlgasDocu import OlgasDocuScreen
from Gui.Screens.OlgasDuty import OlgasDutyScreen

from Gui.Screens.aViewNotesScreen import AViewNotesScreen
from Gui.Screens.configAChallengeOptionsScreen import ConfigAChallengeOptionsScreen

from Gui.Screens.configAChallengeStreamScreen import ConfigAChallengeStreamScreen
from Gui.Screens.configOlgaOptionsScreen import ConfigOlgaOptionsScreen
from Gui.Screens.historyScreen import HistoryScreen
from Gui.Screens.viewARunScreen import ViewARunScreen
from myglobals import ScreenState
from Gui.Screens.olgaViewChallengeScreen import OlgaViewChallengeScreen
from Gui.Screens.olgaViewErrorScreen import OlgaViewErrorScreen
from Gui.Screens.editSongScreen import EditSongScreen
from Gui.Screens.simonConfigOptionsScreen import SimonConfigOptionsScreen
from Gui.Screens.simonGameScreen import SimonGameScreen
from Gui.Screens.simonSelectStartScreen import SimonSelectStartScreen
from Gui.Screens.simonViewBestActiveScreen import SimonViewBestActiveScreen
from Gui.Screens.simonViewChallengeScreen import SimonViewChallengeScreen
from Gui.Screens.simonViewDoneScreen import SimonViewDoneScreen
from Gui.Screens.simonViewErrorScreen import SimonViewErrorScreen
from Gui.Screens.simonViewGraphScreen import SimonViewGraphScreen
from Gui.Screens.simonViewInScreen import SimonViewInScreen
from Gui.Screens.simonViewMissingScreen import SimonViewMissingScreen
from Gui.Widgets.viewRunWidget import ViewRunWidget
from Gui.Widgets.viewStream2Widget import ViewStream2Widget
import myglobals


kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App

# run is the default start method for a kivy app it calls build which builds my gui Screens
# the game is run by periodically calling ScreenState.update in main.py

class VisitingOlga(App):

    def build(self):
        #aNewScreen = AViewNotesScreen()
        aNewScreen = SimonViewDoneScreen()
        aNewScreen.buildAll(aNewScreen.mystate,ViewRunWidget())

        #bNewScreen = AViewNotesScreen()
        bNewScreen = SimonGameScreen()
        #bNewScreen.buildAll("Simon",ViewNotesChallengeWidget())
        #bNewScreen.buildAll("Simon",ViewNotesPlayedWidget())
        bNewScreen.buildAll("Simon",ViewStream2Widget())

        #bNewScreen.buildAll("Simon",ViewNotesRatedWidget())

        cNewScreen = AViewNotesScreen()
        cNewScreen.buildAll("Played",ViewStream2Widget())

        #dNewScreen = AViewNotesScreen()
        dNewScreen = SimonGameScreen()
        dNewScreen.buildAll("nowTiming",ViewRunWidget())

        #eNewScreen = AViewNotesScreen()
        #eNewScreen.buildAll("Song",ViewNotesPlayedWidget())


        simonViewBestActiveScreen = SimonViewBestActiveScreen()
        simonViewBestActiveScreen.build()
        #simonViewBestActiveScreen.buildAll(simonViewBestActiveScreen.mystate,ViewRunWidget())

        simonViewInScreen = SimonViewInScreen()
        simonViewInScreen.build()
        #simonViewInScreen.buildAll(simonViewInScreen.mystate,simonViewInScreen.notesscroller)

        simonViewChallengeScreen = SimonViewChallengeScreen()
        #simonViewChallengeScreen.buildAll(simonViewChallengeScreen.mystate,simonViewChallengeScreen.notesscroller)
        simonViewChallengeScreen.build()


        fNewScreen = SimonViewErrorScreen()
        fNewScreen.buildAll("SimonViewErrorScreen",ViewRunWidget())

        fmNewScreen = SimonViewMissingScreen()
        fmNewScreen.buildAll("SimonViewMissingScreen",ViewRunWidget())

        gNewScreen = SimonViewGraphScreen()
        gNewScreen.build()

        hmNewScreen = EditSongScreen()
        hmNewScreen.build()
        #hmNewScreen.buildAll("EditSongScreen", ViewNotesRatedWidget())

        #ScreenState.change_state("Simon")

        configAChallengeStreamScreen = ConfigAChallengeStreamScreen()
        configAChallengeStreamScreen.build()


        #logScreen = LogScreen()
        #logScreen.buildAll("Log", ViewNotesPlayedWidget())


        historyScreen = HistoryScreen()
        historyScreen.mystate = "History"
        historyScreen.build()



        #historyScreen.buildAll("History", ViewNotesPlayedWidget())

        olgaViewErrorScreen = OlgaViewErrorScreen()
        olgaViewErrorScreen.build()


        olgaViewChallengeScreen = OlgaViewChallengeScreen()
        olgaViewChallengeScreen.build()

        configAChallengeOptionsScreen = ConfigAChallengeOptionsScreen()
        configAChallengeOptionsScreen.build("ChallengeConfigScreen")



        simonConfigOptionsScreen = SimonConfigOptionsScreen()
        simonConfigOptionsScreen.build()

        simonSelectStartScreen = SimonSelectStartScreen()
        simonSelectStartScreen.build()


        configOlgaOptionsScreen = ConfigOlgaOptionsScreen()
        configOlgaOptionsScreen.build(None)


        OlgaMidiConfigScreen = MidiConfigScreen()
        OlgaMidiConfigScreen.build()


        OlgaConfigScreen = OlgasDutyScreen()
        OlgaConfigScreen.build("OlgasDuty")


        OlgaDocuScreen = OlgasDocuScreen()
        OlgaDocuScreen.build("OlgaDocuScreen")

        configOjbectScreen = ConfigObjectScreen()
        configOjbectScreen.build()

        viewArunScreen = ViewARunScreen()
        viewArunScreen.build()

        # first Screen
        #ScreenState.change_state("ChallengeConfigScreen")
        #ScreenState.change_state("OlgasDuty")
        ScreenState.change_state("MidiConfig")
        #ScreenState.change_state("SimonSelectStartScreen")
        #ScreenState.change_state("EditSongScreen")



        #aNewScreen.show(True)

        #Clock.schedule_interval(pianosimon.updateGame, 1/50.0)
        return ScreenState.root

    def on_stop(self):
        # saving today stream
        print "saving today stream"
        myglobals.HistoryMode.save()

        pass
