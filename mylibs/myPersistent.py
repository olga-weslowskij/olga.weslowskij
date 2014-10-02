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

import xml.etree.ElementTree as ET
from mylibs.myUniqueList import MyUniqueList


class Persistent(object):

    def __init__(self):
        self.tree=None
        try:
            self.rtree = ET.parse('persistent.xml')
            self.tree = self.rtree.getroot()
            self.id = ast.literal_eval(self.tree.text)
        except:
            self.tree = ET.Element("id")

            self.id=0
            self.tree.text = repr(self.id)
            #self.tree.write('persistent.xml')
            ET.ElementTree(self.tree).write('persistent.xml')

    def saveId(self):
        self.tree.text = repr(self.id)
        ET.ElementTree(self.tree).write('persistent.xml')


    def getId(self):
        self.id = self.id + 1
        self.saveId()
        return self.id




def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

#root = ElementTree.parse('/tmp/xmlfile').getroot()
#indent(root)
#ElementTree.dump(root)

class PersistentObject(object):

    def __init__(self, *args, **kwargs):
        if not hasattr(self,"nid"):
            self.nid = "None"

        # default class on rebuild
        self.dog_class = None
        self.persistentattr = None
        self.persistentexception = MyUniqueList()
        self.persistentexceptiondontexpand = MyUniqueList()
        self.persistentexception.append("persistentattr")
        self.persistentexception.append("persistentexception")
        self.persistentexception.append("persistentexceptiondontexpand")
        self.persistentexception.append("dog_class")




    def toXml2str(self, name):

        tree = self.toXml2(None, name)

        indent(tree)
        # ET.ElementTree(tree).write(name)
        return ET.tostring(tree, method='xml')
        #return ET.tostring(tree, encoding='utf8', method='xml')

    def fromXml2str(self, astr):
        try:
            rtree = ET.fromstring(astr)
        except:
            print "fromXml2str rtree error\n"

        self.fromXml2(rtree)
        try:
            pass
            #tree = rtree.getroot()
            #self.fromXml2(rtree)
        except:
            print "fromXml2str error\n"
            pass


    def fromXml2file(self, afile):
        with open(afile) as myfile:
            self.fromXml2str(myfile.read())

    def toXml2file(self, afile=None):
        thefile = afile
        if afile ==None:
            thefile = str(self.nid)+".xml"
        with open(thefile,"w+") as myfile:
            myfile.write(self.toXml2str(thefile))



    def toXml2(self, tree, attribname):
        if tree is not None:
            song = ET.SubElement(tree, attribname)
        else:
            # song =  ET.Element(attribname)
            song =  ET.Element(str(self.__class__.__name__))
        #print "toxml: " +attribname + " " + str(self.__class__.__name__)

        #pdb.set_trace()
        #self.__class__.__name__
        song.attrib["nid"]= repr(self.nid)
        # SubElement(song, str(self.nid))

        if self.persistentattr is None:
            titles = self.__dict__.iterkeys()
        else:
            titles = self.persistentattr

        #titles = vars(self)
        for title in titles:
            o = self.__getattribute__(title)
            # exceptions
            if title in self.persistentexception:
                continue
            if title in self.persistentexceptiondontexpand:
                newtitle = ET.SubElement(song, str(title))
                newtitle.text = repr(o)
                continue
            if hasattr(o, "toXml2"):
                o.toXml2(song, str(title))
            else:
                newtitle = ET.SubElement(song, str(title))
                newtitle.text = repr(o)

        if tree is None:
            return song


    def fromXml2(self, tree, nid=None):

        if nid is None:
            tmptree = tree
        else:
            tmptree = tree.find(repr(nid))
            if tmptree is None:
                print "nid not found!"
                return

        #print str(tmptree)

        for child in tmptree:
            #print "setting " + str(child.tag)+ "\n"
            if len(child) > 0:
                # get class by inspection
                dog = getattr(self, child.tag)
                if dog is None:
                    if self.dog_class is None:
                        # default
                        dog=PersistentObject()
                    else:
                        dog = self.dog_class()

                dog.fromXml2(child)

                self.__setattr__(str(child.tag), dog)
            else:
                self.__setattr__(str(child.tag), ast.literal_eval(child.text))

        """
        tmp= MyStream()
        tmp.fromXml2(streamnid,tree)

        tmp.song=self.song
        self.mystream=tmp
        """





