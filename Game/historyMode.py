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

from Game.myStream import MyStream
import myglobals
import datetime

logger = logging.getLogger('history')
hdlr = logging.FileHandler('./history.log')
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class HistoryMode(object):
    def __init__(self):
        self.todaystream = MyStream()
        myglobals.HistoryMode = self

        self.starttime = datetime.datetime.now()

    def update(self, aNote, aTime):
        if aNote:
            self.todaystream.append(aNote)
            logger.info(aNote.toXml2str(str(aNote.nid)))


    def save(self):
        self.todaystream.toXml2file("./History/"+str(self.starttime).replace(" ","_").replace(":","-") +".xml")


