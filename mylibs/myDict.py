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

class MyDict(dict):
    def __init__(self, *args, **kwargs):
        #super(MyList,self).__init__(*args, **kwargs)
        dict.__init__(self, *args, **kwargs)
        self.nid = "None"
        self.dog_class = "unchanged"
        self.defaultvalue=None
        self.defaultNone=False

    def __getitem__(self, item):
        try:
            return super(MyDict,self).__getitem__(item)
        except KeyError:
            if self.defaultNone:
                return None
            if self.defaultvalue:
                return self.defaultvalue
            else:
                return super(MyDict,self).__getitem__(item)

