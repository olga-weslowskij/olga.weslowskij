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



class mykey(list):
    def __add__(self, other):
        if isinstance(other,list):
            ret=mykey([0]*max(len(self),len(other)))
            for i in range(len(self)):
                ret[i]=ret[i]+self[i]
            for i in range(len(other)):
                ret[i]=ret[i]+other[i]
        else:
            ret=mykey()
            for i in self:
                ret.append(i)
            ret[0]=ret[0]+ other
        return ret

    def __sub__(self, other):

        if isinstance(other,list):
            ret=mykey([0]*max(len(self),len(other)))
            for i in range(len(self)):
                ret[i]=ret[i]+self[i]
            for i in range(len(other)):
                ret[i]=ret[i]-other[i]
        else:
            ret=mykey()
            for i in self:
                ret.append(i)
            ret[0]=ret[0]-other
        return ret


    def __neg__(self):
        ret=mykey()
        for i in self:
            ret.append(-i)
        return ret

    def __cmp__(self, aother):
        if isinstance(aother,list):
            other = aother
        else:
            other = [aother]


        toc = max(len(self), len(other))

        for i in range(toc):
            if i < len(self):
                a = self[i]
            else:
                a = 0
            if i < len(other):
                b = other[i]
            else:
                b = 0
            tmp=cmp(a, b)
            #print tmp
            if tmp != 0:
                return tmp

        return 0


    def __lt__(self,other):
        return self.__cmp__(other) < 0

    def __gt__(self,other):
        return self.__cmp__(other) > 0

    def __ge__(self,other):
        return self.__cmp__(other) >= 0

    def __le__(self,other):
        return self.__cmp__(other) <= 0

    def __getitem__(self, item):
        if isinstance( item, slice ) :
            return mykey(super(mykey,self).__getitem__(item))
        else:
            return super(mykey,self).__getitem__(item)


    def __getslice__(self, i, j):
        return mykey(super(mykey,self).__getslice__(i,j))
