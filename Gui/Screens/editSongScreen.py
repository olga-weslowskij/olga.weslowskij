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
from Gui.Screens.aViewNotesScreen import AViewNotesScreen
from Gui.Widgets.viewSongWidget import ViewSongWidget

import myglobals
from Game.options import getOptionValue


class EditSongScreen(AViewNotesScreen):
    def __init__(self):
        super(EditSongScreen,self).__init__()
        self.song = None
        self.mystate = self.__class__.__name__
        self.notesscroller= ViewSongWidget()

    def on_enter(self, tostate):
        hands = getOptionValue("hand")

        print self.__class__.__name__

        if self.song is None:
            #self.song  = myglobals.SimonMode.activeChallenge().song

            self.song = myglobals.gameState.song

            # chords
            self.notesscroller.song= self.song#.getHand(hands).chordify()
            #self.notesscroller.stream = self.song.mystream.getHand(hands).chordify()
            #ScreenState["Song"].notesscroller.stream=self.challengestream
            #notes
            #ScreenState["Song"].notesscroller.stream=myKnownNotes.notes

        super(EditSongScreen,self).on_enter(tostate)

        #code.interact(local=locals())


        """
    def update(self):
        pass
        """

    def updateGui(self):
        self.notesscroller.updateGui()

    def update(self):
        if self.song is None:
            self.song = myglobals.gameState.song

        if self.notesscroller.toshow is None:
            self.notesscroller.toshow= self.song.mystream
            self.dirty=True


        super(EditSongScreen, self).update()



    def buildbtnbar(self):


        if self.btnbar is None:
            self.btnbar=GridLayout(cols=4, size_hint=(1,0.2))



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


        """
        def declareStartBtnCallback(instance):
            anote = self.notesscroller.adapter._selectedBtn[0].myStreamNote
            myglobals.SimonMode.initSimonChallenges(anote)
            pass



        btn13 = Button(text='Start learning here')
        btn13.mystate = self.mystate
        btn13.bind(on_press=declareStartBtnCallback)
        self.btnbar.add_widget(btn13)

        """


        def callbackplay(instance):
            #print "replaying " + str(self.notesscroller._selectedBtn[0]) + " " + str(self.notesscroller._selectedBtn[1])
            self.notesscroller.play()

        btn4 = Button(text='Play\nselected\nChords')
        btn4.speed = 1.0
        btn4.bind(on_press=callbackplay)
        self.btnbar.add_widget(btn4)

        """
        def callback(instance):
            myglobals.gameState.initdone=False
            ScreenState.change_state("Played")

        btn = Button(text='Play Game')
        btn.bind(on_press=callback)
        """


        def saveStateCallback(instance):
            self.song.startparts =[]
            for (k,v) in self.notesscroller.levelstarts.items():
                if  v.state == "down":
                    self.song.startparts.append(k)
                    #self.song.startparts.append(k.pos)

            self.song.endparts =[]
            for (k,v) in self.notesscroller.levelends.items():
                if  v.state == "down":
                    #self.song.endparts.append(k.pos)
                    self.song.endparts.append(k)


            self.song.startparts.sort()
            self.song.endparts.sort()

            for (k,v) in self.notesscroller.hands.items():
                if k.hand:
                    k.hand = int(v.text)

            self.song.mystream=self.song.mystream.decorate()

            self.song.toXml2file("Song.xml")

        btnsave = Button(text='Save to\nSong.xml')
        btnsave.bind(on_press=saveStateCallback)
        self.btnbar.add_widget(btnsave)

        """
        def changeStateCallback(instance):
            ScreenState.change_state(instance.mystate)

        btnOlgasDuty = Button(text='OlgasDuty')
        btnOlgasDuty.mystate = "OlgasDuty"
        btnOlgasDuty.bind(on_press=changeStateCallback)
        self.btnbar.add_widget(btnOlgasDuty)
        """

        super(EditSongScreen,self).buildbtnbar()

        return self.btnbar








