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
from inspect import ismethod
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from Game.options import RecommendOptionsValues, getTextfromValue
from myglobals import ScreenState


class WidgetManager(object):
    def get(self, parentobj, obj, attr):

        #if obj.__class__.__name__ == "SimonMode" and attr == "startchord":
        if parentobj.__class__.__name__ == "SimonMode" and attr == "startchord":
            #print "widgetManager , startchord" + obj.__class__.__name__ +parentobj.__class__.__name__
            def callback2(instance):
                from myglobals import ScreenState
                ScreenState.change_state("SimonSelectStartScreen")

            btn2 = Button(text='Show Start Selection Screen')
            btn2.bind(on_press=callback2)
            return btn2



        if obj.__class__.__name__ == "RunState":
            def callback2(instance):
                from myglobals import ScreenState
                ScreenState["ViewARunScreen"].notesscroller.run = obj
                ScreenState.change_state("ViewARunScreen")

            btn2 = Button(text='ViewARunScreen')
            btn2.bind(on_press=callback2)
            return btn2


        if ismethod(obj):
            if attr == "initSimonChallenges":
                def callback2(instance):
                    try:
                        print obj()
                    except:
                        pass
                btn2 = Button(text="apply config")
                btn2.bind(on_press=callback2)
                return btn2
            if attr == "prettyprint" or attr == "noteName":
                def callback2(instance):
                    try:
                        print obj()
                    except:
                        pass
                btn2 = Button(text=attr)
                btn2.bind(on_press=callback2)
                return btn2

            if attr == "toXml2file":
                def callback2(instance):
                    try:
                        print obj()
                    except:
                        pass
                btn2 = Button(text="save to: " + str(parentobj.nid)+".xml")
                btn2.bind(on_press=callback2)
                return btn2


        if attr == "songpart":
            recommendvalues = {}
            for i in range(len(parentobj.song.startparts)):
                recommendvalues[str(i)]=i
            RecommendOptionsValues[attr]=recommendvalues



        if attr in RecommendOptionsValues.keys():
            #ow = buildOptionWidget(self.attrname)
            name = attr
            #print "gettext: ", self.attrname, repr(self.obj)
            curValue = getTextfromValue(name, obj)
            if curValue is None:
                curValue = RecommendOptionsValues[name].keys()[0]
            ow = MySpinner(text=curValue, values = RecommendOptionsValues[name].keys())
            ow.attrname = attr
            return ow


        return None

class MySpinner(Spinner):

    def __init__(self, **kwargs):
        super(MySpinner, self).__init__(**kwargs)



widgetManager = WidgetManager()