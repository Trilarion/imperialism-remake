************************
Setting
************************

* 4 *turns* per year (seasons), earliest start 1814, usual end 1914 (400 turns) but the game continues running if
  players want to
* *Great powers* (GP) and *Minor nations* (MN); defines their behavior as AI; players can however choose to play any
  nation;  playing a MN is not recommended though
* Limit of 10 GP and 20 MN per game

Map and Terrain
=============================

* Map: *staggered layout* (every second row is shifted by half a tile, so every tile has six neighbours: NW, W, SW,
  SE, E, NE) and no wrapping of the map
* Only a few basic terrain types: desert, plain, swamp, jungle, hills, mountains, tundra, coastal sea, ocean
* The water area on a map must be connected, i.e. each sea tile must have a connection to each other sea tile. This
  means: no inland sea. This is follows from: trade by sea only and to simplify warfare at sea.

Victory Conditions
=============================

* **Military victory**: 60% of provinces conquered (including colonies), the game immediately ends, MP or non-MP games
  can be continued if desired
* **Diplomatic victory**: Owning less than 60% of the provinces but being so advanced that the world admires you. Can be
  achieved during a "world congress". Each 10 years after the first 40 years there is such a congress where every
  province has one vote. With 60% or more of the votes a nation can also become winner. Each province votes with 80%
  chance for their owning nation (except provinces of MN). All provinces of MN (and of GP with a 20% chance) vote
  according to greatness of each GP. For this a normalized score is calculated for all GP (individual score =
  (diplomatic standing 30% (being peaceful helps here), military power 20%, owned territory 20%, industrial output 20%
  (smoothed over the last 5 years), tech advances 10%) divided by sum of individual scores of all GP) and the provinces
  vote then according to this chances.