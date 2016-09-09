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
* Military garnisons can only be seen by neighbored provinces with some degree of uncertainty depending on how many
  units (especially officers) you have for yourself.

.. todo:: Provide details of how capacity and speed depend on development of railroad system and make this
information available to the player.

What if two neighboring powers attack each other in neighboring provinces or even in a triangle. Who becomes
priority? The one with largest, fastest army?

.. todo:: Solve this problem.

Land Units

5 types of units

* militia (stationed in provinces, number is limited per province, only good in defense)
* infantry (cheap, slow, short distance, good in defense and city attack)
* cavallery (expensive, fast, short distance, weak against cities)
* artillery (expensive, slow, large distance)
* officers (at most one per army, increases moral and attack of surrounding units)

Unit properties

* attack strength (IN 0 – 20), no separate defense strengthen: how strong a unit attacks
* unit strength (percentage 0 – 100%): relative amount of soldiers present in this unit
* range (IN 2 – 8): firing distance to target in tiles of the battlefield
* speed (IN 2 – 10): movement speed in tiles of the battlefield
* creation cost ($): amount of money to create from the soldier pool
* upkeep ($ and FN units of fuel): payment per turn for upkeeping this unit, also including fuel costs
* experience level (IN 1-5): experience increase efficiency and is gained by taking part in combats, is lowered when the unit is refilled

Production and Refilling after combat

* units can be produced from the soldier pool and need each one unit of soldiers and the indicated creation costs, next turn they are available at the capital province
* units with less than 100% unit strength can be refilled from the soldier pool without delay but at costs (equal to production costs of such a part of a unit plus a deployment fee ($20)) and experience is reduced
* units with less than 30% unit strength are liquidised to manpower pool

Land Units Strengths

Type - Attack - Range - Speed - Creation Costs - Upkeep

Militia I  | 6 | 2 | 3 | - | -
Militia II | 8 | 2 | 3 | - | -
Infantry I | 8 | 2 | 4 | 1.0 | 1.0