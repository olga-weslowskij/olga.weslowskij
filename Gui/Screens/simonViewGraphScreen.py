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
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from Game import myNoteMap

from Gui.Screens.aViewNotesScreen import AViewNotesScreen
from Gui.Screens.myScreen import MyScreen
from Gui.Widgets.kivyNoteMap import KivyNoteMap
from myglobals import ScreenState
from libtesting.myscrollview import ScrollView
#from myMelodyRun import MelodyRun
import myglobals


class SimonViewGraphScreen(MyScreen):
    def __init__(self):
        super(SimonViewGraphScreen,self).__init__()
        self.mystate = "SimonViewGraphScreen"
        self.pianoSimonGame=None

        self.challenge=None

        self.buided=False

        self.tmppos={}
        self.scatters={}
        self.drawedges={}

    def on_enter(self, tostate):
        self.updateGui()
        super(SimonViewGraphScreen, self).on_enter(tostate)

    """
    def update(self):
        pass
    """

    

    def updateGui(self):
        print "update Gui "
        #self.challenge= myglobals.SimonMode.activeChallenge().challenge
        if self.buided:
            print "update Gui 1"
            return
        if self.challenge is None:
            print "update Gui 2"
            self.challenge =myglobals.SimonMode.activeChallenge().activeChallenge()
        print "update Gui 3"

        if self.challenge:
            #for x in self.challenge.nodes.items():

            minx=100000
            miny=100000

            maxx=0
            maxy=0

            allNodes=self.challenge.G.node.items()

            tmp= self.challenge.challengestartnote

            ## fake knownnotes
            """
            out = False
            while out:
                n = KnownChordPos()
                n.knownChord=tmp


                m = MelodyRating(None,n)

                r = MelodyRun()

                r.append(m)

                self.challenge.myadd_node(r)

                self.challenge.pos[r]= [self.challenge.pos[r][0], -100]
                if hasattr(tmp,"next"):
                    tmp=tmp.next
                else:
                    out = False

            """

            print "SimonViewGraphScreen dimensions\n"
            for y in  allNodes:
                x=y[0]
                # why build?

                """
                tmp = KivyNoteMap()
                #tmp.build(x.currentMelodyRating.getInNote(), x.currentMelodyRating.getKnownNote())
                tmp.build(x.getInNote(), x.getKnownNote())
                """

                pos = self.challenge.pos[x]

                self.drawedges[x]=[]


                print "pos " +str(pos) +"\n"

                #print "hash: " +str(x.EqValueState())

                minx = min(minx,pos[0])
                miny= min(miny,pos[1])

                maxx = max(maxx,pos[0])
                maxy= max(maxy,pos[1])


            print "minx,miny,maxx,maxy " + str([minx,miny,maxx,maxy])



            tmppos={}
            ss = True
            tmp = KivyNoteMap()

            tmp.width = myNoteMap.width
            tmp.height = myNoteMap.height

            #tmp.width=200
            #tmp.height=150



            for y in   allNodes:
                #print y
                x=y[0]
                               
                vpwidget= VPRunWidget()
                vpwidget.object = x


                #vpwidget.widget = vpwidget.build()

                    
                pos = self.challenge.pos[x]
                                
                npos=(pos[0]-minx+tmp.width/2, pos[1]-miny+tmp.height/2)


                self.tmppos[x]=npos

                tmp.pos=npos

                vpwidget.pos =npos
                vpwidget.width = tmp.width
                vpwidget.heigth = tmp.height


                self.graphwidget.add(vpwidget)


                #scatter = Scatter(size=tmp.size, size_hint=(None, None))
                #scatter.add_widget(tmp)

                #self.layout.size=(maxx-minx+5/2*tmp.width,maxy-miny+5/2*tmp.height)

                #self.scatters[x] = tmp
                #self.layout.add_widget(scatter)

                #self.widget.add_widget(tmp)

                #print " adding " + str(tmp) + "to graphview " + str(tmp.pos)
                self.buided=True


            for y in  self.challenge.G.edges(data=True):

                
                pos1=list(self.tmppos[y[0]])
                pos2=list(self.tmppos[y[1]])

                pos1[0]=pos1[0]+tmp.width/2
                pos1[1]=pos1[1]+tmp.height/2


                pos2[0]=pos2[0]
                pos2[1]=pos2[1]

                points=pos1+pos2

                #code.interact(local=locals())

                if (len(y[2]["str"]) > 0 ) and False:
                    #wl = MyLine(points, c=(0.0,1.0
                    pass
                else:
                    vpwidget = VPLineWidget()
                    vpwidget.setPos(points[0],points[1],points[2],points[3])

                    self.graphwidget.add(vpwidget)

                    #wl = MyLine(points)


                    #self.drawedges[y[0]].append(wl)
                    #self.drawedges[y[1]].append(wl)


                # print "build Line " + str(y[0])


                #self.updateVP(0,0,800,800)




        pass


        #draw all lines bad ..



    def build(self):

        self.widget = BoxLayout(orientation='vertical')

        self.notesscroller = ScrollView()

        atmp = AViewNotesScreen()

        self.btnbar = atmp.buildbtnbar()

        #self.widget=FloatLayout(size_hint=(1,1))
        #self.notesscroller = ScrollView(size_hint=(1,1))
        self.notesscroller = ScrollView(size_hint=(1,1-self.btnbar.size_hint_y), size=(800,800))

        self.notesscroller.do_scroll_x=True
        self.notesscroller.do_scroll_y=True

        #
        #self.layout.bind(minimum_height=layout.setter('height'))


        #self.layout = RelativeLayout(size=(10000,10000), size_hint=(None,None))
        self.graphwidget = VpLayout(size=(10000,10000), size_hint=(None,None))
        self.graphwidget.build(self.notesscroller)
        #self.layout.t = self
        #scatter = Scatter()
        #scatter.add_widget(self.layout)
        #self.layout = FloatLayout(size=(10000,10000), size_hint=(0,0))


        #self.notesscroller.add_widget(scatter)
        self.notesscroller.add_widget(self.graphwidget)


        #self.layout.bind(minimum_size=self.layout.setter('size'))
        #self.layout.bind(minimum_width=self.layout.setter('width'))

        self.widget.add_widget(self.notesscroller)
        self.widget.add_widget(self.btnbar)


        #self.widget= self.notesscroller

        ScreenState.add_state(self)

        pass



class MyLine(Widget):
    def __init__(self, points,c=(1.0,1.0,1.0)):
        super(MyLine,self).__init__()

        #dp = points[2]-points[0], points[3]-points[1]
        #self.canvas.add(Line(points=dp))
        self.canvas.add(Color(c))
        self.canvas.add(Line(points=points))

        #self.pos=(points[0],points[1])
        self.shown=False
        pass


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

        self.scroller = scroller

        self.object2VPWidget={}

        self.maxx = 0
        self.minx = 0
        self.maxy = 0
        self.miny = 0


    def add(self,vpwidget):
        self.widgets.append(vpwidget)
        self.object2VPWidget[vpwidget.object]=vpwidget

        self.maxx = max(self.maxx, vpwidget.pos[0]+ vpwidget.width)
        self.maxy = max(self.maxy, vpwidget.pos[1]+ vpwidget.heigth)

        self.minx = min(self.minx, vpwidget.pos[0])
        self.miny = min(self.miny, vpwidget.pos[1])


        self.size=(self.maxx - self.minx , self.maxy - self.miny)



    def getWidgetsInView(self,x,y,w,h):
        if len(self.widgets) == 0:
            return []
        print("vp " + str([x,y,w,h]))
        ret=[]
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


            if rectintersect(objectposx,objectposy,objectposx2,objectposy2,x,y,x+w,y+h):
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
        #r = self.getWidgetsInView(0-x,0-y,w,h)

        #self.layout.clear_widgets()
        self.clear_widgets()
        #self.layout.canvas.clear()
        count = 0
        for x in r:
            #w = self.scatters[x]
            #w.pos = w.pos - (x,y)
            #self.layout.add_widget(x.getWidget())
            self.add_widget(x.getWidget())
            x.shown=True

            count = count +1

        print "vpwidgets count " + str(count)



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

        #self.width = self.widget.size[0]
        #self.heigth = self.widget.size[1]


        self.widget.pos = self.pos
        return self.widget

    def setPos(self,x1,y1,x2,y2):
        self.pos = (min(x1,x2),min(y1,y2))
        self.width = abs(x1-x2)
        self.heigth = abs(y1-y2)




class VPRunWidget(VPWidget):

    def build(self):
        obj = self.object
        widget = KivyNoteMap()
        #widget.build(obj.currentMelodyRating.getInNote(), obj.currentMelodyRating.getKnownNote())
        widget.build(obj.getInNote(), obj.getKnownNote())

        btn = Button(text="id:" + str(id(obj)))
        widget.add_widget(btn)

        def callback(instance):
            myglobals.ScreenState.mystate.selectedobject = self.object


        btn.bind(on_press=callback)

        #widget.add_widget(widget.orgchord)
        #widget.add_widget(widget.chord)
        #widget.error.text=str(len(widget.errors))
        #widget.add_widget(widget.error)
        #widget.add_widget(TextInput(text="id:" + str(id(obj))))
        widget.add_widget(Label(text="lenlist " + str(obj.lenlist)))

        #widget.add_widget(Label(text= obj.getKnownChordInNoteMap().prettyprint()))
        widget.add_widget(Label(text=str(obj.EqValueState())))
        widget.add_widget(TextInput(text= obj.getKnownChordInNoteMap().prettyprint()))

        #atxt= str(self.challenge.seen.get(obj,None))
        atxt= str(obj.rcost)

        widget.add_widget(Label(text=atxt))

        widget.size_hint=(None,None)
        return widget

class VPLineWidget(VPWidget):

    def build(self):
        points = [self.pos[0], self.pos[1], self.pos[0] + self.width , self.pos[1]+ self.heigth]
        widget =MyLine(points)
        return widget

