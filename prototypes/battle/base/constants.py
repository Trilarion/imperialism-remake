# Imperialism remake
# Copyright (C) 2014 Trilarion
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

import os
from enum import unique

import lib.utils as u

"""
    Game specific path locations for artwork, music, ...
    Only static values here.
"""


def extend(path, *parts):
    """
        Uses os.path.join to join parts of a path. Also checks for existence and raises an error
        if the path is not existing.
    """
    extended = os.path.join(path, *parts)
    if not os.path.exists(extended):
        raise RuntimeError('constructed path {} does not exist'.format(extended))
    if Debug_Mode:
        Used_Resources.add(extended)
    return extended

# debug mode and helpers
Debug_Mode = False
Used_Resources = set()

# base folders (do not directly contain data)
Data_Folder = extend('.', 'data')
Artwork_Folder = extend(Data_Folder, 'artwork')

# scenarios (save games)
Battle_Folder = extend(Data_Folder, 'battle')
Battle_Ruleset_Folder = extend(Battle_Folder, 'rules')
Battle_Ruleset_Standard_File = extend(Battle_Ruleset_Folder, 'standard.rules')

# graphics related folders
Graphics_Folder = extend(Artwork_Folder, 'graphics')
Graphics_UI_Folder = extend(Graphics_Folder, 'ui')
Graphics_Map_Folder = extend(Graphics_Folder, 'map')
Graphics_Flag_Folder = extend(Graphics_Folder, 'flag')
Graphics_Unit_Folder = extend(Graphics_Folder, 'unit')

#UI file
Graphics_Background = extend(Graphics_UI_Folder,'background.jpg')
Graphics_End = extend(Graphics_UI_Folder,'end.png')
Graphics_General = extend(Graphics_UI_Folder,'general.png')
Graphics_Help = extend(Graphics_UI_Folder,'help.png')
Graphics_Retreat = extend(Graphics_UI_Folder,'retreat.png')
Graphics_Target = extend(Graphics_UI_Folder,'target.png')

#Flag file
Graphics_Flag0 = extend(Graphics_Flag_Folder,'flag0.png')
Graphics_Flag1 = extend(Graphics_Flag_Folder,'flag1.png')
Graphics_Flag2 = extend(Graphics_Flag_Folder,'flag2.png')
Graphics_Flag3 = extend(Graphics_Flag_Folder,'flag3.png')
Graphics_Flag4 = extend(Graphics_Flag_Folder,'flag4.png')
Graphics_Flag5 = extend(Graphics_Flag_Folder,'flag5.png')
Graphics_Flag6 = extend(Graphics_Flag_Folder,'flag6.png')
Graphics_Flag7 = extend(Graphics_Flag_Folder,'flag7.png')
Graphics_Flag8 = extend(Graphics_Flag_Folder,'flag8.png')
Graphics_Flag9 = extend(Graphics_Flag_Folder,'flag9.png')
Graphics_Flag10 = extend(Graphics_Flag_Folder,'flag10.png')
Graphics_Flag11 = extend(Graphics_Flag_Folder,'flag11.png')

#Unit File
Graphics_Unit0 = extend(Graphics_Unit_Folder,'unit0.png')
Graphics_Unit1 = extend(Graphics_Unit_Folder,'unit1.png')
Graphics_Unit2 = extend(Graphics_Unit_Folder,'unit2.png')
Graphics_Unit3 = extend(Graphics_Unit_Folder,'unit3.png')
Graphics_Unit0_small = extend(Graphics_Unit_Folder,'unit0_128.png')
Graphics_Unit1_small = extend(Graphics_Unit_Folder,'unit1_128.png')
Graphics_Unit2_small = extend(Graphics_Unit_Folder,'unit2_128.png')
Graphics_Unit3_small = extend(Graphics_Unit_Folder,'unit3_128.png')


# minimal screen resolution
Screen_Min_Size = (800, 600)