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
from kivy.uix.label import Label
from Game.myLogHandler import infoLog


class InfoLogWidget(BoxLayout):

    def build(self):
        self.orientation="horizontal"

        self.next = Button(text="next" , size_hint=(0.05,1))

        self.last = Button(text="last", size_hint=(0.05,1))


        def nextcb(instance):
            infoLog.setPos(infoLog.pos + 1)

        def lastcb(instance):
            print "last"
            infoLog.setPos(infoLog.pos -1)


        self.next.bind(on_press=nextcb)
        self.last.bind(on_press=lastcb)

        self.logWidget = Label(size_hint=(0.6,1))
        self.logWidget.text = "InfoLog"

        self.errorWidget = Label(size_hint=(0.3,1))
        self.errorWidget.text = "ErrorLog"


        self.add_widget(self.last)
        self.add_widget(self.logWidget)
        self.add_widget(self.next)
        self.add_widget(self.errorWidget)


        self.size_hint=(1,0.1)
        #infoLog.handlers.append(self.logWidget)
        infoLog.handlers.append(self)

    @property
    def text(self):
        pass

    @text.setter
    def text(self, atest):
        self.logWidget.text = atest

    @property
    def error(self):
        pass

    @error.setter
    def error(self, atest):
        #print atest
        self.errorWidget.text = atest

