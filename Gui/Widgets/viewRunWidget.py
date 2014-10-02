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
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Gui.Screens.aViewNotesScreen import SelectNotes
from Gui.Widgets.kivyNoteMap import KivyNoteMap
from Gui.Widgets.listview8 import ListView8
import myglobals
from mylibs.myDict import MyDict

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(__name__ + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)



class ViewRunAdapter(SelectNotes, SimpleListAdapter):

    def __init__(self):
        self.song= None
        self.stream=None
        self.build()
        self.cache={}

        self.wcache=[]

        # cache all
        self.docache=False

    def build(self):
        SelectNotes.build(self)
        self.widget = GridLayout(cols=10, size_hint_y=None)
        self.widget.bind(minimum_height=self.widget.setter('height'))
        return self.widget

    def updateGui(self):
        pass
        #print "update ViewRunWidget\n"


    def clear(self,children):
        if not(self.docache):
            for c in children:
                #print c.__class__.__name__
                try:
                    if c.__class__.__name__ == "KivyNoteMap":
                        self.wcache.append(c)
                except:
                    pass



    def get_view(self, index):
        if len (self.data) == 0:
            return None

        if index >= len(self.data):
            return None
        #return self.buildkivyMelodyRating(index)

        #print self.stream[-1].prettyprint()
        #return self.data[index]

        # on demand creation
        (toshow,i,wi) = self.data[index]

        if self.docache:
            try:
                return self.cache[self.data[index]]
            except:
                pass

        w = self.buildKivyNoteMap(toshow,i)[wi]
        if self.docache:
            self.cache[self.data[index]]= w

        if self.docache:
            # funny politics, tabula rasa
            # cut memory usage
            if len(self.cache) > 500:
                self.cache = {}
        return w



    def set_view(self,index, item):
        while index >= len(self.data):
            self.data.append(None)
        self.data[index] = item




    def buildObjectButton(self, attr, p = None ,o = None):
        btnid = Button(text=str(attr))

        if o is None:
            x = p.__getattribute__(attr)
        else:
            x = o

        #print "got ", x

        def callback(instance):
            myglobals.ScreenState.mystate.selectedobject = x
            myglobals.ScreenState["ConfigObjectScreen"].object = x
            # force rebuild
            s = myglobals.ScreenState["ConfigObjectScreen"]
            try:
                s.notesscroller.remove_widget(s.layout)
            except:
                pass
            myglobals.ScreenState.change_state("ConfigObjectScreen")


        btnid.bind(on_press=callback)
        return btnid


    def buildKivyNoteMap(self, toshow, i, notesandrightspeed = None):

        x = toshow.list[i]

        childs=[]

        if len(self.wcache) > 0:
            btn = self.wcache.pop()
            #print "btn.parent " , btn.parent , "len(self.wcache)", len(self.wcache)
            btn.config(toshow.list[i].getInNote(), toshow.list[i].getKnownNote())
            childs=btn.children
            btn.clear_widgets()
        else:
            #print "btn new "
            btn = KivyNoteMap()
            btn.build(toshow.list[i].getInNote(), toshow.list[i].getKnownNote())
        """

        btnid = Button(text="id:" + str(id(x)))
        btn.add_widget(btnid)

        def callback(instance):
            myglobals.ScreenState.mystate.selectedobject = x
            myglobals.ScreenState["ConfigObjectScreen"].object = x
            myglobals.ScreenState.change_state("ConfigObjectScreen")


        btnid.bind(on_press=callback)

        """
        btn.add_widget(self.buildObjectButton(str(id(x)), o=x))


        """
        if type(x) is list:
            btn.build(x)
        else:
            btn.build([x])
        """

        #btn.progress.value=1
        btn.speed.text=str(x)
        btn.add_widget(btn.orgchord)
        btn.orgchord.bind(on_press=self.selectBtn)
        btn.add_widget(btn.chord)
        btn.chord.bind(on_press=self.selectBtn)



        #btn.add_widget(Label(text="id:" + str(id(x))))

        #btn.myduration.text="id:" + str(id(x))

        #btn.add_widget(btn.myduration)

        if toshow.list[i].getKnownNote():
            btn.myvolume.text="("+str(toshow.list[i].getKnownNote().myoffset)+")"
        else:
            btn.myvolume.text="None"

        btn.add_widget(btn.myvolume)

        btn.add_widget(btn.myoffset)

        """
        if x:
            xd = x.rspeed()
            if xd is None:
                xd = "None"
        else:
            xd ="None"
        btn.add_widget(self.buildObjectButton("rspeed", o=xd))
        btn.add_widget(self.buildObjectButton("maxRightSpeedRunState", p=x))
        btn.add_widget(self.buildObjectButton("minRightSpeedRunState", p=x))
        """


        if x.getCurrent2RunSpeed():
            #if x.rightspeederror:
            if False:
                text='[color=ff0000]'+str(x.getCurrent2RunSpeed())[0:5] +'[/color]'
                btn.speed.markup=True
            else:
                text = str(x.getCurrent2RunSpeed())[0:5]
            btn.speed.text= text
            btn.speed.halign="right"
            #btn.add_widget(btn.speed)

        else:
            btn.speed.text="-"

        btn.error.text=""

        if hasattr(x,"errorstr"):
            if x.errorstr:
                btn.error.text ='[color=ff0000]'+str(x.errorstr) +'[/color]'
                btn.error.markup=True


        btn.add_widget(btn.error)

        #if x.getCurrent2RunSpeed():
        #self.notesscroller.data.append(btn.speed)
        #self.notesscroller.widget.add_widget(btn.speed)

        #if x.getCurrent2RunSpeed():

        if x.lastRunState and x.lastRunState.getKnownChordInNoteMap().chordfull():
            #self.notesscroller.data.append(btn.speed)
            #self.notesscroller.widget.add_widget(btn.speed)
            btn.speed.height = btn.height
            btn.speed.size_hint_y=None
            return [btn, btn.speed]
            #btn.add_widget(btn.speed)

        #self.notesscroller.data.append(btn)
        #self.notesscroller.widget.add_widget(btn)

        return [btn]




class ViewRunWidget(ListView8,object):
    def __init__(self, *args, **kwargs):
        super(ViewRunWidget,self).__init__(*args, **kwargs)

        self.donelen = 0
        self.shownMelodyRun=None
        self.shownKivyNoteMap=[]
        self.shownMelodyRating=MyDict()
        self.shownMelodyRating.defaultNone=True

        self.shownpos ={}
        self.shownpos[0]=0
        self.shownpos[1]=0

        self.widget = self

        self.adapter = ViewRunAdapter()
        self.notesscroller = self.adapter

        self.do_scroll_x=True
        self.do_scroll_y=True

        self.toshow = None


    @property
    def run(self):
        return self.toshow


    @run.setter
    def run(self, value):
        self.toshow = value

    """
    def updateGui(self):
        self.adapter.updateGui()
        self._trigger_reset_populate()
    """

    def play(self):
        self.adapter.play()

    def updateGui(self):
        """if not(self.shownMelodyRun is None or self.shownMelodyRun != self.toshow):
            return
            """

        # belongs in update, but i dont have update widget ..
        if self.shownMelodyRun == self.toshow:
            return
        # rest belong in updateGui


        toshow = self.toshow

        index = len(self.shownKivyNoteMap)

        if toshow is None:
            print "Show Run None"
            for i in xrange(index):
                self.shownKivyNoteMap[i] = None
                self.notesscroller.set_view(self.shownpos[i], None)
            self._trigger_reset_populate()
            return
        print self.toshow.prettyprint()

        newlen = len(toshow.list)



        #for x in self.notesscroller.stream:


        news = False
        # extend

        while ( len(self.shownKivyNoteMap)< newlen):
            self.shownKivyNoteMap.append(None)
            news = True

        """
        what is with changed???
        if news == False:
            return
        """

        #update all changed
        for start in xrange(newlen-1, -1,-1):
            news = True
            if toshow.list[start] == self.shownMelodyRating[start]:
                #pass
                break

        #logger.info("updating " + str([start+1,newlen]))

        #for i in xrange(start+1, newlen):
        for i in xrange(start, newlen):
        #for i in xrange(newlen):
            if toshow.list[i] != self.shownMelodyRating[i] or True:
                #if self.shownKivyNoteMap[i]:
                #    self.notesscroller.widget.remove_widget(self.shownKivyNoteMap[i])
                #    self.notesscroller.widget.remove_widget(self.shownKivyNoteMap[i].speed)
                #self.shownKivyNoteMap[i] = self.buildKivyNoteMap(toshow,i)

                x = toshow.list[i]
                if x.lastRunState and x.lastRunState.getKnownChordInNoteMap().chordfull():
                #if len(self.shownKivyNoteMap[i]) == 2:
                    self.shownpos[i+1]= self.shownpos[i] + 2
                    #self.notesscroller.set_view(self.shownpos[i]+1, self.shownKivyNoteMap[i][0])
                    self.notesscroller.set_view(self.shownpos[i]+1, (toshow,i,0))
                    #self.notesscroller.set_view(self.shownpos[i], self.shownKivyNoteMap[i][1])
                    self.notesscroller.set_view(self.shownpos[i], (toshow,i,1))
                    #
                else:
                    self.shownpos[i+1]= self.shownpos[i] + 1
                    #self.notesscroller.set_view(self.shownpos[i], self.shownKivyNoteMap[i][0])
                    self.notesscroller.set_view(self.shownpos[i], (toshow,i,0))
                    #self.notesscroller.data[self.shownpos[i]] = self.shownKivyNoteMap[i][0]

                self.shownMelodyRating[i] = toshow.list[i]

        #logger.info("clearing " + str([newlen,len(self.shownKivyNoteMap)]))

        for i in xrange(newlen, len(self.shownKivyNoteMap)):
            self.shownKivyNoteMap[i] = None
            self.shownMelodyRating[i] = None
            self.notesscroller.set_view(self.shownpos[i], None)




        self.donelen = index
        #len(self.notesscroller.stream)

        #self.notesscroller.updateGui()

        if (news):
            #self.notesscroller.data = self.shownKivyNoteMap
            self._trigger_reset_populate()

        self.shownMelodyRun = toshow
        pass


    def buildKivyNoteMap(self, toshow, i, notesandrightspeed = None):

        x = toshow.list[i]

        btn = KivyNoteMap()

        btn.build(toshow.list[i].getInNote(), toshow.list[i].getKnownNote())
        """

        btnid = Button(text="id:" + str(id(x)))
        btn.add_widget(btnid)

        def callback(instance):
            myglobals.ScreenState.mystate.selectedobject = x
            myglobals.ScreenState["ConfigObjectScreen"].object = x
            myglobals.ScreenState.change_state("ConfigObjectScreen")


        btnid.bind(on_press=callback)

        """
        btn.add_widget(self.buildObjectButton(str(id(x)), o=x))


        """
        if type(x) is list:
            btn.build(x)
        else:
            btn.build([x])
        """

        #btn.progress.value=1
        btn.speed.text=str(x)
        btn.add_widget(btn.orgchord)
        btn.orgchord.bind(on_press=self.notesscroller.selectBtn)
        btn.add_widget(btn.chord)
        btn.chord.bind(on_press=self.notesscroller.selectBtn)



        #btn.add_widget(Label(text="id:" + str(id(x))))

        #btn.myduration.text="id:" + str(id(x))

        #btn.add_widget(btn.myduration)

        if toshow.list[i].getKnownNote():
            btn.myvolume.text="("+str(toshow.list[i].getKnownNote().myoffset)+")"
        else:
            btn.myvolume.text="None"

        btn.add_widget(btn.myvolume)

        btn.add_widget(btn.myoffset)

        """
        if x:
            xd = x.rspeed()
            if xd is None:
                xd = "None"
        else:
            xd ="None"
        btn.add_widget(self.buildObjectButton("rspeed", o=xd))
        btn.add_widget(self.buildObjectButton("maxRightSpeedRunState", p=x))
        btn.add_widget(self.buildObjectButton("minRightSpeedRunState", p=x))
        """


        if x.getCurrent2RunSpeed():
            #if x.rightspeederror:
            if False:
                text='[color=ff0000]'+str(x.getCurrent2RunSpeed())[0:5] +'[/color]'
                btn.speed.markup=True
            else:
                text = str(x.getCurrent2RunSpeed())[0:5]
            btn.speed.text= text
            btn.speed.halign="right"
            #btn.add_widget(btn.speed)

        else:
            btn.speed.text="-"

        btn.error.text=""

        if hasattr(x,"errorstr"):
            if x.errorstr:
                btn.error.text ='[color=ff0000]'+str(x.errorstr) +'[/color]'
                btn.error.markup=True


        btn.add_widget(btn.error)

        #if x.getCurrent2RunSpeed():
        #self.notesscroller.data.append(btn.speed)
        #self.notesscroller.widget.add_widget(btn.speed)

        #if x.getCurrent2RunSpeed():

        if x.lastRunState and x.lastRunState.getKnownChordInNoteMap().chordfull():
            #self.notesscroller.data.append(btn.speed)
            #self.notesscroller.widget.add_widget(btn.speed)
            btn.speed.height = btn.height
            btn.speed.size_hint_y=None
            return [btn, btn.speed]
            #btn.add_widget(btn.speed)

        #self.notesscroller.data.append(btn)
        #self.notesscroller.widget.add_widget(btn)

        return [btn]

    def buildObjectButton(self, attr, p = None ,o = None):
        btnid = Button(text=str(attr))

        if o is None:
            x = p.__getattribute__(attr)
        else:
            x = o

        #print "got ", x

        def callback(instance):
            myglobals.ScreenState.mystate.selectedobject = x
            myglobals.ScreenState["ConfigObjectScreen"].object = x
            # force rebuild
            s = myglobals.ScreenState["ConfigObjectScreen"]
            try:
                s.notesscroller.remove_widget(s.layout)
            except:
                pass
            myglobals.ScreenState.change_state("ConfigObjectScreen")


        btnid.bind(on_press=callback)
        return btnid

