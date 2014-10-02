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
from xml.etree.ElementTree import SubElement,Element
from mylibs.myPersistent import PersistentObject


class MyList(list, PersistentObject):
    def __init__(self, *args, **kwargs):
        #super(MyList,self).__init__(*args, **kwargs)
        list.__init__(self, *args, **kwargs)
        self.nid = "None"
        self.dog_class = "unchanged"
        self.dog_class = None


    def toXml2(self, tree, attributename):

        if tree is not None:
            song = SubElement(tree, attributename)
        else:

            song =  Element(str(self.__class__.__name__))

        #song = SubElement(tree, attributename)
        song.attrib["nid"]= repr(self.nid)

        titles = self.__dict__.iterkeys()
        for i, o in enumerate(self):
            #pdb.set_trace()
            #window = SubElement(song, "pos")
            #window.attrib["pos"]=repr(i)
            window = song


            #o = self.__getattribute__(title)
            title = str(i)

            # exceptions
            """
            if title in self.persistentexception:
                print "skipping" , title
                continue
            """

            """
            if title in self.persistentexceptiondontexpand:
                newtitle = ET.SubElement(song, str(title))
                newtitle.text = repr(o)
                continue
            """


            if hasattr(o, "toXml2"):
                o.toXml2(window,"pos_"+repr(i))
            else:
                newtitle = SubElement(window, o.__class__.__name__)
                newtitle.text = repr(o)

        return song

    def fromXml2(self,tree):
        for pos in tree:
            dog = None
            if self.dog_class is None:
                dog=PersistentObject()
            else:
                dog = self.dog_class()

            dog.fromXml2(pos)

            #print dog.__dict__

            self.append(dog)


    def append(self, p_object):
        list.append(self,p_object)

    def items(self):
        return list(enumerate(self))



