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
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Game import gameEngineRoot, options
from Gui.MyScreenController import ScreenState
from Gui.Screens.myScreen import MyScreen
import myglobals


class OlgasDocuScreen(MyScreen):

    def build(self, astateName):
        # only too build MdidController and fill options midi in and midi out
        #myglobals.gameState = pianoSimonGame.PianoSimonGame()

        self.widget = FloatLayout()

        self.mystate=astateName

        self.buttons = BoxLayout(orientation='vertical', size_hint=(1, .2), pos_hint={'x':0, 'y':0})

        self.image = Image(source='docu.png', size_hint=(1, .8), pos_hint={'x':0, 'y':0.2})


        self.widget.add_widget(self.image)

        self.widget.add_widget(self.buttons)


        """
        button = Button(text='Learn a new part')
        self.buttons.add_widget(button)

        def callback(instance):
            options.optionsvalue["mode"]="simon"
            ScreenState.change_state("Simon")

        button.bind(on_press=callback)
        """


        button = Button(text='Main Menu')
        self.buttons.add_widget(button)

        def callback(instance):
            ScreenState.change_state("OlgasDuty")

        button.bind(on_press=callback)

        ScreenState.add_state(self)


        return self.widget


    def on_enter(self, tostate):
        super(OlgasDocuScreen,self).on_enter(tostate)

    def on_leave(self, tostate):
        super(OlgasDocuScreen,self).on_leave(tostate)


    def update(self):
        pass
        #if optionswidgets["speedtol"].text == "normal":
        #    ScreenState.change_state("Played")
