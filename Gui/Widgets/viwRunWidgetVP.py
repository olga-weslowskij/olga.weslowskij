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
import ast
import inspect
import pdb
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox

from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
#from Gui.Widgets.mytreeview import TreeViewNode, TreeView, TreeViewLabel



from Gui.Widgets.kivyNoteMap import KivyNoteMap
from Gui.widgetManager import widgetManager
from libtesting.myscrollview import ScrollView
import myglobals
from mylibs.myDict import MyDict


def rectintersect(x,y ,x2, y2, rx1,ry1,rx2,ry2):
    # top
    if min(y,y2) > max(ry1,ry2):
        return False

    # bot
    if max(y,y2) < min(ry1,ry2):
        return False

    # right
    if min(x,x2) > max(rx1,rx2):
        return False

    # left
    if max(x,x2) < min(rx1,rx2):
        return False

    # intersect
    return True


class VpLayout(RelativeLayout):
    # ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh ugly
    # t is simonGraphView
    #def updateVP(self,x,y,w, h):
    #    self.t.updateVP(x,y,w,h)



    """
    def __init__(self, *args, **kwargs):
        super(VpLayout,self).__init__(self, *args, **kwargs)
        self.build()
    """

    def build(self, scroller):
        self.widgets=[]

        self.shownWidgets=[]

        self.scroller = scroller

        scroller.vp = self

        self.object2VPWidget={}

        self.maxx = None
        self.minx = None
        self.maxy = None
        self.miny = None


    def add(self,vpwidget):
        self.widgets.append(vpwidget)
        #self.object2VPWidget[vpwidget.object]=vpwidget

        if self.maxx is None:
            self.maxx = vpwidget.pos[0]+ vpwidget.width
        if self.maxy is None:
            self.maxy = vpwidget.pos[1]+ vpwidget.heigth

        if self.minx is None:
            self.minx = vpwidget.pos[0]

        if self.miny is None:
            self.miny = vpwidget.pos[1]


        self.maxx = max(self.maxx, vpwidget.pos[0]+ vpwidget.width)
        self.maxy = max(self.maxy, vpwidget.pos[1]+ vpwidget.heigth)

        self.minx = min(self.minx, vpwidget.pos[0])
        self.miny = min(self.miny, vpwidget.pos[1])


        self.size=(self.maxx - self.minx , self.maxy - self.miny)

        #self.scroller.size = self.size
        #print "self.size ",self.size



    def getWidgetsInView(self,sx,sy,w,h):
        if len(self.widgets) == 0:
            return []
        #print("avp " + str([ax,ay,w,h]))
        ret=[]

        x= sx + self.minx
        y= sy + self.miny
        #x= ax
        #y= ay

        print("vp " + str([x,y,w,h]))

        #return self.widgets

        for o in  self.widgets:

            pos= o.pos

            #print("checking " + str(o) + " " + str(pos))
            """
            if pos[0] > x -w/2.0 and pos[0] < x + 3/2.0* w:
                if pos[1] > y - h/2.0 and pos[1] < y + 3/2.0 * h:
                    ret.append(o)
                    continue
            """

            objectposx = pos[0]
            objectposy = pos[1]

            objectposx2 = pos[0] +  o.width
            objectposy2 = pos[1] + o.heigth


            if rectintersect(objectposx,objectposy,objectposx2,objectposy2,x,y,x+w,y+2*h):
                ret.append(o)
                print(str(o.pos) +" "),

        print("adding " + str(len(ret)) + " items to vp\n")
        return ret



    def updateVP(self,x,y,w, h):
        r = self.getWidgetsInView(0-x,0-y,self.scroller.width,self.scroller.height)

        #r = self.getWidgetsInView(self.minx+0-x,self.miny+0-y,self.scroller.width,self.scroller.height)

        #r = self.getWidgetsInView(0-x,0-y,w,h)

        #self.layout.clear_widgets()

        #self.clear_widgets()

        for x in self.shownWidgets:
            x.shown=False

        #self.layout.canvas.clear()
        count = 0
        for x in r:
            #w = self.scatters[x]
            #w.pos = w.pos - (x,y)
            #self.layout.add_widget(x.getWidget())
            wx = x.getWidget()
            if not(wx in self.children):
                self.add_widget(wx)
                pass
            x.shown=True

        for x in self.shownWidgets:
            if x.shown == False:
                self.remove_widget(x.widget)

        self.shownWidgets=r

        print "vpwidgets count " + str(len(self.shownWidgets))


class ScrollViewUpdate(ScrollView):

    def updateGui(self):
        #print "ScrollView.updateGui"
        self.vp.updateGui()

        self._trigger_update_from_scroll()


        pass

    @property
    def run(self):
        return self.vp.toshow

    @run.setter
    def run(self, value):
        self.vp.toshow=value


class VPWidget(object):
    def __init__(self):
        self.pos=(0,0)
        self.width=10
        self.heigth=10

        self.shown = False
        self.widget=None
        self.object=None

    def build(self):
        return None

    def getWidget(self):
        if self.widget is None:
            self.widget=self.build()

        if self.widget is None:
            print "Not a widget"

        self.widget.size=(self.width,self.heigth)

        self.width = self.widget.size[0]
        self.heigth = self.widget.size[1]


        #self.widget.pos = self.pos
        #print "self.widget.pos ", self.widget.pos
        return self.widget

    def setPos(self,x1,y1,x2,y2):
        self.pos = (min(x1,x2),min(y1,y2))
        self.width = abs(x1-x2)
        self.heigth = abs(y1-y2)



#class TreeLayout(Widget):
class ViewRunWidgetVP(VpLayout):

    def build(self, scoller):

        self.scroller= scoller
        super(ViewRunWidgetVP,self).build(self.scroller)

        self.builded = False
        self.rows=0
        self.index=0
        self.elementHeight=200
        self.elementWidth=150
        self.elementperrow=1
        self.size_hint=(None,None)

        #self.size=[640,480]

        self.obj = None

        self.done={}

        self.deeplevel=1


        self.donelen = 0
        self.shownMelodyRun=None
        self.shownKivyNoteMap=[]
        self.shownMelodyRating=MyDict()
        self.shownMelodyRating.defaultNone=True

        self.vpns={}
        self.shownpos ={}
        self.shownpos[0]=0
        self.shownpos[1]=0

        self.widget = self

#        self.adapter = ViewRunAdapter()

        self.toshow = None

        # all objects or only with widgets in widgetmanager
        #if not hasattr(self,"debug"):
        #    self.debug = None

        return self

    def move(self):
        #print "move" , self.__dict__
        #self.pos= [self.pos[0] +1 , self.pos[1] +1]
        self.pos= [self.pos[0] , self.pos[1]]

        self.clear_widgets()
        #print "self.obj:", self.obj

        obj = self.obj
        self.build(self.scroller)

        self.add_obj(obj, str(obj.__class__.__name__),0,None, self.deeplevel)


    def updateGui(self):
        if self.toshow:
            #print "ViewRunWidgetVP.updateGui"
            self.layout_runstate(self.toshow)


#class TreeNode(GridLayout):
    def layout_runstate(self, arunstate):

        if self.shownMelodyRun == self.toshow:
            return
        # rest belong in updateGui


        toshow = self.toshow

        index = len(self.shownKivyNoteMap)

        if toshow is None:
            print "Show Run None"
            for i in xrange(index):
                self.shownKivyNoteMap[i] = None
            return
        #print self.toshow.prettyprint()

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
                    self.set_view(self.shownpos[i]+1, (toshow,i,0))
                    #self.notesscroller.set_view(self.shownpos[i], self.shownKivyNoteMap[i][1])
                    self.set_view(self.shownpos[i], (toshow,i,1))
                    #
                else:
                    self.shownpos[i+1]= self.shownpos[i] + 1
                    #self.notesscroller.set_view(self.shownpos[i], self.shownKivyNoteMap[i][0])
                    self.set_view(self.shownpos[i], (toshow,i,0))
                    #self.notesscroller.data[self.shownpos[i]] = self.shownKivyNoteMap[i][0]

                self.shownMelodyRating[i] = toshow.list[i]

        #logger.info("clearing " + str([newlen,len(self.shownKivyNoteMap)]))

        for i in xrange(newlen, len(self.shownKivyNoteMap)):
            self.shownKivyNoteMap[i] = None
            self.shownMelodyRating[i] = None
            self.notesscroller.set_view(self.shownpos[i], None)


        self.donelen = index
        self.shownMelodyRun = toshow

        pass


    def set_view(self,pos , widget_config):
        addit = False
        try:
            vpn = self.vpns[pos]
        except:
            vpn = VPRunWidget()

            addit = True

        vpn.config = widget_config

        vpn.parentWidget = self
        #vpn.heigth=self.height//5
        #vpn.width=self.width //8
        vpn.width=self.elementWidth
        vpn.heigth=self.elementHeight
        vpn.index=pos
        indent = pos % self.elementperrow
        row = pos // self.elementperrow

        #vpn.pos = [self.pos[0] + indent * vpn.width, self.pos[1]  - (row * (vpn.heigth))]
        vpn.pos = [indent * vpn.width, - (row * (vpn.heigth))]

        #print "self.scroller.size ", self.scroller.size

        if addit:
            print "adding vpn:" ,vpn.__dict__
            self.add(vpn)
            self.vpns[vpn.index] = vpn


class VPRunWidget(VPWidget):

    @property
    def wpos(self):
        x = self.pos[0]
        y = self.pos[1]
        #y = self.parentWidget.scroller.pos[1] + self.parentWidget.scroller.size[1] + self.pos[1]
        #y = self.parentWidget.size[1] + self.pos[1]
        return x,y



    def build(self):
        print "VPRunWidget.build"
        (toshow,i,wi) = self.config
        w = self.buildKivyNoteMap(toshow,i)[wi]
        w.width = self.width
        w.heigth = self.heigth
        w.pos = self.wpos
        w.size_hint=(None,None)
        return w

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
        #btn.orgchord.bind(on_press=self.notesscroller.selectBtn)
        btn.add_widget(btn.chord)
        #btn.chord.bind(on_press=self.notesscroller.selectBtn)



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
            #btn.speed.size_hint_y=None
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

        print "got ", x

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
