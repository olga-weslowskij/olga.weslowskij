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

"""
RecommendOptionsValues = {\
    "hand": {"left":[1],"right":[0],"left and right":[0,1]},\
    "speedtol": {"dont bother me\nwith speedtol":0,"easy":0.5,"normal":0.25,"hard":0.1},\
    "chorderrors": {"one error:\nfail":0,"easy":0.1,"normal":0.05,"hard":0.025},\
    "midi.volume": {"pp":30,"p":50,"-":70,"f":90,"ff":110},\
    "update Gui": {"on every change\n(maybe slow on some Screens\n(and some computers))":True,"manual":False},\
    "repeat": {"1":1,"2":2,"3":4,"memory champion":0},\
    "midi in": {},\
    "midi out": {},\
    #"mode": {"simon":"simon","correct anything":"correct","just log":"log"}\
}
"""

RecommendOptionsValues = {\
    "hand": {"left and right":[0,1]},\
    "speedtol": {"dont bother me\nwith speedtol":0,"easy":0.5,"normal":0.25,"hard":0.1},\
    "chorderrors": {"one error:\nfail":0},\
    "midi.volume": {"pp":30,"p":50,"-":70,"f":90,"ff":110},\
    "errorvolume": {"pp":30,"p":50,"-":70,"f":90,"ff":110},\
    "update Gui": {"on every change\n(maybe slow on some Screens\n(and some computers))":True,"manual":False},\
    "repeat": {"1":1,"2":2,"3":3},\
    "midi in": {},\
    "midi out": {},\
    #"songpart": {"1":1,"2":2,"3":3},\
    #"mode": {"simon":"simon","correct anything":"correct","just log":"log"}\
    "speed": {"auto": None, "50%":0.5, "60%":0.6,"70%":0.7,"80%":0.8,"90%":0.9, "100%":1.0,"110%":1.1,"120%":1.2}, \
    "adaptive": {"Yes": True, "No":False},\
    "paused": {"Yes": True, "No":False}
    }


optionswidgets={}

optionsvalue={}

def getTextfromValue(aoption, v):
    for x,y in RecommendOptionsValues[aoption].items():
        if y == v:
            print "found ", aoption, RecommendOptionsValues[aoption].items(), v
            return x

    print "not found ", aoption, RecommendOptionsValues[aoption].items(), v




def getOptionValue(aoption, aoptionswidgets=optionswidgets):
    try:
        return RecommendOptionsValues[aoption][aoptionswidgets[aoption].text]
    except KeyError:
        try:
            return  optionsvalue[aoption]
        except KeyError:
            return None


thescorefile =None

def optionsNeeded(argv):
    global thescorefile
    thescorefile =argv[0]





