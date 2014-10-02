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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Game import gameEngineRoot, options
from Gui.MyScreenController import ScreenState
from Gui.Screens.myScreen import MyScreen
import myglobals


class OlgasDutyScreen(MyScreen):

    def build(self, astateName):
        # only too build MdidController and fill options midi in and midi out
        #myglobals.gameState = pianoSimonGame.PianoSimonGame()

        self.widget = FloatLayout()

        self.mystate=astateName


        self.buttons = BoxLayout(orientation='vertical', size_hint=(.4, .6), pos_hint={'x':.55, 'y':.2})

        #self.text = TextInput( size_hint=(.4, .6), pos_hint={'x':.05, 'y':.2})
        self.text = Label( size_hint=(.4, .6), pos_hint={'x':.05, 'y':.2} ,markup = True)
        #self.text = Label( size=(.4, .6), pos=(0.05, 0.2) ,markup = True)
        #self.text = Label( size=(.05, .2), markup = True)
        self.text.halign="left"
        self.text.font_size=18
        self.text.text= "[color=ff0000]Olga is a strict single russian piano teacher.\n\
Rumor has it that Olga has a past in the KGB,\n\
because Olga remembers everything\n" \
                        "and logs everything.\n\
Olga has no work permit and works\n on the side for a lousy payment\n\
and is therefore usually in a \n bad mood (and condition at the moment).\n\
Olga's English skills are unfortunately rather poor.\n\
\n\
What does Olga do:\n\
Olga trains your ear by helping you \nmemorize the songs you want to learn.\n\
Olga can notice you on errors.\n\
It tries to implement some of the ideas from:\n\
Fundamentals of Piano Practice\nby Chuan C. Chang (http://www.pianofundamentals.com/)[/color]"""

        self.widget.add_widget(self.text)

        self.widget.add_widget(self.buttons)

        button = Button(text='Learn a new part')
        self.buttons.add_widget(button)

        def callback(instance):
            options.optionsvalue["mode"]="simon"
            ScreenState.change_state("Simon")

        button.bind(on_press=callback)

        button = Button(text='Correct me')

        def callback2(instance):
            print instance.text
            options.optionsvalue["mode"]="simon"
            ScreenState.change_state("OlgaViewErrorScreen")

        button.bind(on_press=callback2)

        self.buttons.add_widget(button)

        """
        button = Button(text='Log')
        self.buttons.add_widget(button)

        def callback(instance):
            options.optionsvalue["mode"]="log"
            ScreenState.change_state("Log")


        button.bind(on_press=callback)
        """

        button = Button(text='History')
        self.buttons.add_widget(button)

        def callback(instance):
            options.optionsvalue["mode"]="log"
            ScreenState.change_state("History")

        button.bind(on_press=callback)


        def callback(instance):
            ScreenState.change_state("EditSongScreen")

        btn12 = Button(text='Edit Song')

        btn12.bind(on_press=callback)
        self.buttons.add_widget(btn12)

        def callbackplayEdit(instance):
            #main.console()
            myglobals.gameState.edit()

        btnedit = Button(text='edit')

        btnedit.bind(on_press=callbackplayEdit)
        self.buttons.add_widget(btnedit)

        def callbackplaydocu(instance):
            #main.console()
            ScreenState.change_state("OlgaDocuScreen")


        btndocu = Button(text='docu')

        btndocu.bind(on_press=callbackplaydocu)
        self.buttons.add_widget(btndocu)




        def callbackplay80(instance):
            #main.console()
            myglobals.gameState.test()

        btn80 = Button(text='test')

        btn80.bind(on_press=callbackplay80)
        self.buttons.add_widget(btn80)


        ScreenState.add_state(self)





        return self.widget


    def on_enter(self, tostate):
        super(OlgasDutyScreen,self).on_enter(tostate)


    def on_leave(self, tostate):
        print "leaving OlgasDuty"
        super(OlgasDutyScreen,self).on_leave(tostate)

        # redo init
        if myglobals.gameState:
            myglobals.gameState.initdone=False
        else:
            myglobals.gameState = gameEngineRoot.GameEngineRoot()

            #myglobals.gameState = pianoSimonGame.PianoSimonGame()

        myglobals.gameState.initGame()


    def update(self):
        pass
        #if optionswidgets["speedtol"].text == "normal":
        #    ScreenState.change_state("Played")
