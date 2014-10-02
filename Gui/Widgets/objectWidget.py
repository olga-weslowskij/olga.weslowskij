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


#class TreeLayout(GridLayout):
from kivy.uix.widget import Widget
from Game.options import RecommendOptionsValues
from Gui.widgetManager import widgetManager


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


            """

            def inrect(x,y,rx1,ry1,rx2,ry2):
                if x >= rx1 and x <= rx2:
                    if y >= ry1 and y <= ry2:
                        return True
                return False






            if inrect(objectposx, objectposy, x,y,x+w,y+h):
                ret.append(o)
                continue

            if inrect(objectposx2, objectposy2, x,y,x+w,y+h):
                ret.append(o)
                continue

            if inrect(x,y,objectposx, objectposy, objectposx2, objectposy2):
                ret.append(o)
                continue

            if inrect(x+w,y+h,objectposx, objectposy, objectposx2, objectposy2):
                ret.append(o)
                continue

            """


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
class TreeLayout(VpLayout):

    def build(self, scoller):

        self.scroller= scoller
        super(TreeLayout,self).build(self.scroller)

        self.builded = False
        self.rows=0
        self.index=0
        self.elementHeight=32
        self.valueWidth=500
        self.labelWidth=200
        self.indentWidth=75

        #self.size=[640,480]

        self.obj = None

        self.done={}

        self.deeplevel=1

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


#class TreeNode(GridLayout):
    def add_obj(self, obj , attrname="", indent = 0, parent = None, deeplevel=-1):
        #tb.size_hint=(16,16)
        #tb.size=(16,16)
        #tb.pos=(100,self.valueWidth)

        #tl.size_hint=(200,16)
        #tl.size=(200,self.elementHeight)
        #tl.pos = (100+self.elementHeight,100)



        if self.obj== None:
            self.obj=obj

        try:
            if obj.showattr is None:
                titles = obj.__dict__.keys()
            else:
                titles = obj.showattr

        except:
            try:
                titles = obj.__dict__.keys()
                obj.persistentexceptiondontexpand = []
                obj.persistentexception=["persistentexception", "persistentexceptiondontexpand" ]

            except:
                titles=[]

        #print "\n", obj.__class__.__name__ ,": ", titles

        #titles = vars(self)


        vpn = VPTreeElementWidget()
        vpn.titles= titles
        vpn.parentWidget = self
        vpn.parentobj = parent
        vpn.obj = obj
        try:
            vpn.lenobj= len(obj.items())
        except:
            pass
        vpn.attrname=attrname
        vpn.indent=indent
        vpn.indentWidth=self.indentWidth
        vpn.heigth=self.height
        vpn.valueWidth=self.valueWidth
        vpn.labelWidth=self.labelWidth
        vpn.elementHeight=self.elementHeight
        vpn.indentWidth=self.indentWidth
        vpn.index=self.index

        rw = widgetManager.get(vpn.parentobj, vpn.obj, vpn.attrname)

        addit = False

        if rw or self.debug or vpn.indent ==0:
            addit = True
        else:
            return

        self.rows = self.rows +1

        vpn.width=self.valueWidth+self.labelWidth
        vpn.heigth=self.elementHeight
        vpn.pos = [self.pos[0] + indent * self.indentWidth, self.pos[1]  - (self.index * (self.elementHeight))]

        #n.pos = [self.pos[0] + indent * self.indentWidth, self.pos[1]  - (self.index * (self.elementHeight))]
        #n.pos = [self.pos[0] + indent * self.indentWidth, self.pos[1] +  (self.index * (self.elementHeight))]
        #n.pos = [self.pos[0] + indent * self.indentWidth, self.pos[1] - (self.index * (self.elementHeight))]

        self.index = self.index +1

        if addit:
            self.add(vpn)
        else:
            return

        if deeplevel == 0:
            return

        # expand just ones
        if self.done.get(id(obj),False):
            return

        self.done[id(obj)] = True

        for title in titles:
            try:
                o = obj.__getattribute__(title)

                #print "expanding ", obj.__class__.__name__ , str(title)

                """
                if title=="note":
                    pdb.set_trace()
                """

                # exceptions
                if title in obj.persistentexception:
                    continue
                if title in obj.persistentexceptiondontexpand:
                    #newtitle = ET.SubElement(song, str(title))
                    #newtitle.attrname = repr(o)
                    continue
                if hasattr(o, "toXml2") and False:
                    pass

                    #o.toXml2(song, str(title))
                else:
                    self.add_obj(o, title, indent+1, obj, deeplevel-1)
            except:
                pass

        if type(obj) is str:
            return

        try:
            #print "found items: " , obj.items()
            if type(obj) is list:
                for i,o in list(enumerate(obj)):
                    self.add_obj(o, str("["+str(i)+"]"), indent+1, obj, deeplevel-1)
            else:
                for i,o in obj.items():
                    self.add_obj(o, str("["+str(i)+"]"), indent+1, obj, deeplevel-1)
        except:
            pass

        """
        else:
            # enumerates
            if deeplevel >0:
                try:
                    for i,o in enumerate(obj):
                        #print i, str(o)
                        self.add_obj(o, str("["+str(i)+"]"), indent+1, obj, deeplevel-1)
                except:
                    pass
        """

        """
        # methods
        for m in inspect.getmembers(obj, predicate=inspect.ismethod):
            title = m[0]
            self.add_obj(m[1], title, indent+1, obj, deeplevel-1)
            pass
        """

        # all
        if self.debug:
            for m in inspect.getmembers(obj):
                title = m[0]
                if title in titles:
                    continue
                if title[0] == title[1] == "_":
                    continue
                self.add_obj(m[1], title, indent+1, obj, deeplevel-1)
                pass


class VPTreeElementWidget(VPWidget):
    def __init__(self, *args, **kwargs):
        super(VPTreeElementWidget,self).__init__(*args, **kwargs)
        self.valueWidth=None
        self.labelWidth=None
        self.elementHeight=None
        self.indentWidth=None

        self.attrname=""
        self.indent=0
        self.parentWidget = None
        self.parentobj=None
        self.obj = None
        self.lenobj=0
        self.titles=None
        self.index=None


    def buildExpandButton(self, attr, p = None ,o = None):
        btnid = Button()
        btnid.txt = attr

        if o is None:
            try:
                x = p.__getattribute__(attr)
            except:
                try:
                    x = p.__getitem__(attr)
                except:
                    pass

        else:
            x = o

        def callback(instance):
            #self.parentobj.obj=x
            self.parentWidget.obj=x
            #print "expanding ",x
            self.parentWidget.move()



        btnid.bind(on_press=callback)
        return btnid


    def build(self):
        n = Widget()

        n.pos = [self.pos[0] - self.parentWidget.minx, self.pos[1] - self.parentWidget.miny]


        lenobj=0
        try:
            lenobj = len(self.obj)
        except:
            pass
        if len(self.titles) == 0 and (self.lenobj == 0 or type(self.obj) is str) and (lenobj == 0 or type(self.obj) is str):
            obj = self.object
            tv = TextInput(multiline = True)

            n.cols=2

            tl = Label()
            #tl = self.buildExpandButton(self.attrname,o=self.obj,p= self.parentobj)

            tl.text = obj.__class__.__name__
            tl.text = str(self.attrname)

            n.size=[1,0.1]

            n.size=[self.valueWidth+self.labelWidth, self.elementHeight]

            n.add_widget(tl)

            if not(inspect.ismethod(self.obj)):
                n.add_widget(tv)


            rw = widgetManager.get(self.parentobj, self.obj,self.attrname)

            if rw:
                n.add_widget(rw)

                rw.pos = (n.pos[0] + self.labelWidth , n.pos[1]+ 0)
                rw.size=(self.valueWidth,self.elementHeight)

                def on_spin(instance, value):
                    newvalue = RecommendOptionsValues[instance.attrname][value]
                    #print instance.attrname, value, newvalue
                    tv.text = repr(newvalue)

                rw.bind(text=on_spin)



            tv.size=(self.valueWidth , self.elementHeight)
            tv.pos = (n.pos[0] + self.labelWidth + self.valueWidth, n.pos[1]+ 0)



            tv.text = repr(self.obj)

            def on_text(instance, value):
                #print('The widget', instance, 'attrname', self.attrname , 'have:', value)

                if len(value) >0:
                    self.parentobj.__setattr__(self.attrname, ast.literal_eval(value))

            tv.obj = obj
            tv.bind(text=on_text)


            tl.text = obj.__class__.__name__ +" " + str(self.attrname)
            tl.text = str(self.attrname)

            tl.size=(self.labelWidth,self.elementHeight)
            tl.pos = (n.pos[0] + 0, n.pos[1]+ 0)

            #n.size_hint=(None,None)


        else:

            tb = CheckBox()

            #tl = Label()

            tl = self.buildExpandButton(self.attrname,o=self.obj)


            #tl.text = self.obj.__class__.__name__
            #tl.text = self.attrname

            n.size=[1,0.1]

            n.size=[self.valueWidth+self.labelWidth, self.elementHeight]

            tb.pos = (n.pos[0], n.pos[1]+ 0)
            tb.size=(self.elementHeight,self.elementHeight)

            #tl.size=(self.valueWidth,self.elementHeight)
            tl.size=(self.labelWidth,self.elementHeight)
            #tl.pos = (n.pos[0] + tb.size[0], n.pos[1]+ 0)
            tl.pos = (n.pos[0], n.pos[1]+ 0)
            #tl.pos = (n.pos[0] + self.labelWidth, n.pos[1]+ 0)

            if self.attrname == "":
                tl.text = self.obj.__class__.__name__
                tl.text == ""
            else:
                tl.text = self.attrname

            #tb.pos = (n.pos[0] + self.labelWidth, n.pos[1]+ 0)


            n.add_widget(tl)
            #n.add_widget(tb)

            rw = widgetManager.get(self.parentobj, self.obj,self.attrname)
            if rw:
                n.add_widget(rw)
                #rw.pos = (n.pos[0] + tb.size[0] + tl.size[0], n.pos[1]+ 0)
                rw.pos = (n.pos[0] + tl.size[0], n.pos[1]+ 0)
                rw.size = (self.valueWidth,self.elementHeight)

            #n.size_hint=(None,None)



        return n


