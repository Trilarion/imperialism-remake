# Imperialism remake
# Copyright (C) 2015 Spitaels <spitaelsantoine@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from enum import Enum
from lxml import etree

def indent(input_str):
    return input_str.replace("\n", "\n\t")
    
class WorkerType(Enum):
    NoWorker = -1
    UntainedWorker = 0
    TrainedWorker = 1
    ExpertWorker = 2

    @classmethod
    def fromInt(self, val):
        if val == "0":
            return WorkerType.UntainedWorker
        elif val == "1":
            return WorkerType.TrainedWorker
        elif val == "2":
            return WorkerType.ExpertWorker
        elif val == "-1":
            return WorkerType.NoWorker

    def toInt(self):
        if self == WorkerType.UntainedWorker:
            return 0
        elif self == WorkerType.TrainedWorker:
            return 1
        elif self == WorkerType.ExpertWorker:
            return 2
        elif self == WorkerType.NoWorker:
            return -1


class unitTypes:
    list = []

    def __init__(self,xmlfile):
        tree = etree.parse(xmlfile)
        for child in tree.xpath("/unitTypes/unitType"):
            utype = unitType()
            utype.id = child.get("id")
            utype.name = child.findtext("name")
            utype.type = child.findtext("type")
            utype.evol = child.findtext("evol")
            utype.technologyId = child.findtext("technologyId")
            utype.life = child.findtext("caracteritics/life")
            utype.firepower = child.findtext("caracteritics/firepower")
            utype.move = child.findtext("caracteritics/move")
            utype.range = child.findtext("caracteritics/range")
            utype.entrench = child.findtext("caracteritics/entrench")
            utype.description = child.findtext("caracteritics/description")
            utype.pixmap = child.findtext("graphics/pixmap")
            utype.money = child.findtext("cost/money")
            utype.arms = child.findtext("cost/arms")
            utype.horses = child.findtext("cost/horses")
            utype.petrol = child.findtext("cost/petrol")
            utype.worker = WorkerType.fromInt(child.findtext("cost/worker"))


            self.list.append(utype)
            #print(utype.findtext("type"))

#TODO implement upgrade...
class unitType:
    id = -1
    type = -1
    evol = -1
    technologyId = -1
    name = ""

    #graphics data
    pixmap = "none"

    #unit cataracteristics
    life = -1
    firepower = -1
    move = -1    
    range = -1
    entrench = False
    description = "none"
    
    #unit price
    money = -1
    arms = -1
    horses = -1
    petrol = -1
    worker = WorkerType.NoWorker

    def __str__(self):
        retval = "\n\nUnit Main Info\n"
        retval += "\t - id: " + str(self.id) + "\n"
        retval += "\t - name: " + str(self.name) + "\n"
        retval += "\t - type: " + str(self.type) + "\n"
        retval += "\t - period: " + str(self.evol) + "\n"
        retval += "\t - technologyId: " + str(self.technologyId) + "\n"
        retval += "Graphics\n"
        retval += "\t - pixmap :" + self.pixmap + "\n"
        retval += "Cataracteristics\n"
        retval += "\t - life: " + str(self.life) + "\n"
        retval += "\t - firepower: " + str(self.firepower) + "\n"
        retval += "\t - move: " + str(self.move) + "\n"
        retval += "\t - range: " + str(self.range) + "\n"
        retval += "\t - entrench: " + str(self.entrench) + "\n"
        retval += "\t - description: " + self.description + "\n"
        retval += "Price\n"
        retval += "\t - money: " + str(self.money) + "\n"
        retval += "\t - arms: " + str(self.arms) + "\n"
        retval += "\t - horses: " + str(self.horses) + "\n"
        retval += "\t - petrol: " + str(self.petrol) + "\n"
        retval += "\t - worker: "
        if self.worker == WorkerType.UntainedWorker : 
            retval += "Untained Worker"
        elif  self.worker == WorkerType.TrainedWorker : 
            retval += "Trained Worker"
        elif  self.worker == WorkerType.ExpertWorker : 
            retval += "Expert Worker"
        elif self.worker == WorkerType.NoWorker : 
            retval += "None"
        else :
            retval += self.worker
        retval += "\n"
        return retval


if __name__ == "__main__":
    data = unitTypes("data.xml")
    for d in data.list:
        print(d)
    








