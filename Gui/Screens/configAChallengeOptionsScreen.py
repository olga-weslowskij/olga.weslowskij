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

import json

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from Game import gameEngineRoot
from Gui.MyScreenController import ScreenState

from Gui.Screens.myScreen import MyScreen
import myglobals
from Game.options import optionswidgets, RecommendOptionsValues


class labeledWidget(BoxLayout):

    #def __init__(self):
        #self.build()
     #   pass


    def build(self, awidget):
        self.orientation = 'horizontal'
        self.label = Label()
        self.add_widget(self.label)
        self.widget = awidget
        self.add_widget(self.widget)




def buildLabeledTextWidget(text = "fill me", aWidget=None):
    client = labeledWidget()
    client.build(TextInput(multiline=False))
    client.label.text= text
    return client


def buildOptionWidget(name, aoptionswidgets=optionswidgets):
    client = labeledWidget()
    spinner = Spinner(text=RecommendOptionsValues[name].keys()[0], values = RecommendOptionsValues[name].keys())
    client.build(spinner)
    client.label.text= name
    aoptionswidgets[name] = spinner
    return client




class ConfigAChallengeOptionsScreen(MyScreen):
    def __init__(self):
        super(ConfigAChallengeOptionsScreen,self).__init__()
        self.options={}

        self.options["hand"] = "hand"
        self.options["speedtol"] = "speedtol"
        self.options["chorderrors"] = "chorderrors"
        self.options["repeat"] = "repeat"

        self.name = "config"


    def build(self, astateName=None):
        # only too build MdidController and fill options midi in and midi out
        #myglobals.gameState = pianoSimonGame.PianoSimonGame()
        #myglobals.gameState = gameEngineRoot.PianoSimonGame2()
        #myglobals.gameState.myMidiController = MyMidiController()

        self.widget = BoxLayout(orientation='vertical')

        #self.fileChooser = FileChooserListView()

        #self.widget.add_widget(self.fileChooser)



        #self.widget.add_widget(buildLabeledTextWidget(text="client"))
        #self.widget.add_widget(buildLabeledTextWidget(text="port"))
        #self.widget.add_widget(buildLabeledTextWidget(text="Song"))
        for x in RecommendOptionsValues.keys():
            if self.options.get(x,None) is not None:
                self.widget.add_widget(buildOptionWidget(x))

        #optionswidgets["speedtol"].text='easy'
        #optionswidgets["hand"].text='left and right'

        self.loadOptions()

        #self.widget.add_widget(buildLabeledTextWidget(text="Hand"))

        #self.widget.add_widget(buildLabeledTextWidget(text="Timing"))

        def callback(instance):
            ScreenState.change_state_back()

        btn = Button(text='Back')
        btn.bind(on_press=callback)

        self.widget.add_widget(btn)

        if astateName:
            self.mystate=astateName

        ScreenState.add_state(self)


        return self.widget


    def on_enter(self, tostate):
        super(ConfigAChallengeOptionsScreen,self).on_enter(tostate)


    def on_leave(self, tostate):

        super(ConfigAChallengeOptionsScreen,self).on_leave(tostate)


        # redo init
        if myglobals.gameState:
            myglobals.gameState.initdone=False
        else:
            #myglobals.gameState = pianoSimonGame.PianoSimonGame()
            myglobals.gameState = gameEngineRoot.GameEngineRoot()

    def update(self):
        pass
        #if optionswidgets["speedtol"].text == "normal":
        #    ScreenState.change_state("Played")

    def loadOptions(self):
        try:
            with open(self.name +'.json', 'rb') as fp:
                allOptions = json.load(fp)


            for x in allOptions.keys():
                print "challengeConfigScreen loading " + str(x)
                #pdb.set_trace()

                if self.options.get(x,None) is not None:
                    optionswidgets[x].text=str(allOptions[x])
        except:
            pass


    def saveOptions(self):
        allOptions = {}
        for x in RecommendOptionsValues.keys():
            allOptions[x]=optionswidgets[x].text

        with open(self.name +'.json', 'wb') as fp:
            json.dump(allOptions, fp)

