************************
Military
************************

Philosophy: The role of the military in this game is quite large, but not dominant. We should not forget that the
game is also about industrial development and diplomacy, not only about war. Therefore battles must be complex and
offer diversification, but on a simplified level. The battle and army model of Imperialism 1 needs to be extended
without making it too complex. Some ideas from other games (like unit promotions) should be incorporated. The main
points here:

* A strong military needs a strong industrial base for paying high upkeep
* It can be either defensively or offensively aligned
* Battles can take more than a turn, delaying action and allowing reinforcement.
* The number of units taking part in battle is limited (due to limited organization and area) but should seldom be
  reached.
* Healing is not for free, it may also take time.
* Battles are carried out on a detailed hex map and can take several turns per game turn.  Panzer General like feeling.
* Terrain is determined by defending province (and specific for each)
* Maybe add training time (cheap units, short training time, long units, large training time) - during training will
  be shown in barracks of ministry of defense, deployed right after training
* Fortification should be expensive and less useful, so artillery orgies are not necessary.
* Militia might actually only be present in the defense case and tied to the province. This could be reflected by the
  naming also.
* Light and heavy cavalry (move and attack or heavy artillery attack only, or move attack and move on, light cavalry)
* Health status is displayed as a bar with green yellow and red (red is casualties, green is full morale) or so
* Movement capacity and speed depends on development of railroad system.
* Military garrisons can only be seen by neighbored provinces with some degree of uncertainty depending on how many
  units (especially officers) you have for yourself.

.. todo:: Provide details of how capacity and speed depend on development of railroad system and make this
          information available to the player.

What if two neighboring powers attack each other in neighboring provinces or even in a triangle. Who becomes
priority? The one with largest, fastest army?

.. todo:: Solve this problem.

Land Units
=====================================

**5 types of units**

* militia (stationed in provinces, number is limited per province, only good in defense)
* infantry (cheap, slow, short distance, good in defense and city attack)
* cavalry (expensive, fast, short distance, weak against cities)
* artillery (expensive, slow, large distance)
* officers (at most one per army, increases moral and attack of surrounding units)

**Unit properties**

* attack strength (IN 0 – 20), no separate defense strengthen: how strong a unit attacks
* unit strength (percentage 0 – 100%): relative amount of soldiers present in this unit
* range (IN 2 – 8): firing distance to target in tiles of the battlefield
* speed (IN 2 – 10): movement speed in tiles of the battlefield
* creation cost ($): amount of money to create from the soldier pool
* upkeep ($ and FN units of fuel): payment per turn for upkeep of this unit, also including fuel costs
* experience level (IN 1-5): experience increase efficiency and is gained by taking part in combats, is lowered when the
  unit is refilled

**Production and Refilling after combat**

* units can be produced from the soldier pool and need each one unit of soldiers and the indicated creation costs, next
  turn they are available at the capital province
* units with less than 100% unit strength can be refilled from the soldier pool without delay but at costs (equal to
  production costs of such a part of a unit plus a deployment fee ($20)) and experience is reduced
* units with less than 30% unit strength are liquidised to manpower pool

Land Units Strengths:

=============  ====== ===== ===== ============== ========
Type           Attack Range Speed Creation costs Upkeep
=============  ====== ===== ===== ============== ========
Militia I      6      2     3
Militia II     8      2     3
Infantry I     8      2     4     1.0            1.0
Infantry II    10     2     4     1.4            1.0
Infantry III   12     3     6     1.8            1.1
Artillery I    14     4     3     1.5            1.3
Artillery II   18     6     3     2.0            1.5
Artillery III  22     8     4     2.5            1.7
Cavalry I      12     2     6     1.5            1.2
Cavalry II     16     2     8     2.0            1.4
Tank(Cav III)  20     4     8     2.5            1.6+fuel
Officers       8      0     4     1.0            1.0
=============  ====== ===== ===== ============== ========

Additionally:

* Artillery -50% when defending
* Cavalry -50% when attacking a city area
* Officers only defending

Creation cost is a multiplier on the base creation cost ($500).

Upkeep (per turn) is a multiplier on the base upkeep ($50)

.. todo:: Upkeep multiplier depends on experience level of unit. Define how.

* Special defence multiplier: Entrenched (Militia, Infantry +2 if it hasn't moved the last battle round)
* Promotion of Officers: Base is Lieutenant (attack +1 for 3 random units), then Colonel (attack +1 for 6 random
  units), then General (attack +2 for 8 random units)
* Earliest time of introduction: Type I from 1814, Type II from 1850, Type III from 1880, introduced by techs
* Strategic movement limited to 2-3 provinces per turn, faster with railroads?

.. todo:: Specify how much faster movement is with railroad, specify how overseas transport is done.

Navy
=====================================

**General properties**

* Upgrade means we basically buy a new ship but get some discount on raw material from scrapping the old vessel.
* Land invasion from sea with a large number of provinces in between delays the action, strong naval defense delays
  it even further or blocks it altogether.
* Merchant marine does not appear on the map, only somewhere within the trade screens.
* Movement of war ships takes one turn per one sea zone always.

.. todo:: Provide details how naval defense blocks or delays sea invasion.

**Sea zones**

* The sea area of a map is divided in sea zones which form a connected network of sea zones.
* Each sea zone contains all the fleets from different nations in this sea zone as well as all the provinces with
  borders to this sea zone.
* Information displayed is the approximate amount and change and mission of other ships (with more details depending
  on the amount of your ships).

.. todo:: Provide details how this scouting works and on what it depends.

**Possible actions**

* Evasive action: avoid contact
* Defensive actions: guard the trade in a sea zone, secure landing operation
* Offensive actions: interfere trade in a sea zone, engage enemy fleets
* Default action is no other command is issued is: avoid contact

**Classification of units**

* small and fast merchant ships (superior blockade runner, expensive in relation to cargo)
* large and slow merchant ships (inferior blockade runner, cheap in relation to cargo)
* light and fast war ships (efficient for merchant hunting, inefficient for naval battle)
* heavy and slow war ships (inefficient for merchant hunting, efficient for naval battle)
* 3 (merchants) or 3 (war ships) levels of improvement for each type where cargo and speed improves while upkeep stays
  constant. All higher levels must be researched first.
* small merchants: carrack, trader, clipper
* large merchants: fluyt, indiamen, freighter
* light war ships: frigate, raider, battle cruiser
* heavy war ships: ship-of-the-line, ironclad, dreadnought

Properties of merchant ships:

============ ============= ============= ==============
Name         Speed         Cargo [units] Building costs
============ ============= ============= ==============
Carrack      3             3
Trader       4             3
Clipper      5             4
Fluyt        1             8
Indiamen     2             10
Freighter    4             12
============ ============= ============= ==============

.. todo:: Provide costs

Properties of war ships:

================ ============= ============= ==============
Name             Speed         Strength      Building costs
================ ============= ============= ==============
Frigate          3             8
Raider           4             12
Battle Cruiser   5             20
Ship-of-the-Line 2             16
Ironclad         2             20
Dreadnought      3             26
================ ============= ============= ==============

.. todo:: Provide costs and re-balance

Ideas behind:

* Clippers are fast and can outrun almost anything but do not carry much cargo
* 5 speed levels, higher speed level means very high chance to escape/outrun a blockade

