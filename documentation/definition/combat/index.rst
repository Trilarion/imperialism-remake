************************
Combat
************************

Land combat
==========================

**Battlefield**

Province battle board in staggered layout of tiles (as in the main map) with 24 tiles side length, 3 tile (capital is 6 tiles)  wide city

**Time**

* 5 battle turns per game turn at most
* If the city is occupied at any time during the battle, the attacker has won. Battle is over
* If all attacking units are destroyed or fleeing or the player aborts the attack, the defender has won. Battle is over.
* Otherwise (city not taken but attacking units are still present), the battle continues the next turn keeping the
  actual strategic position but with reenforcement possible

**Damage model**

* Two units are in combat with attack values :math:`a_i` and strengths :math:`s_i`
* Damage dealt is then :math:`d_i=\mbox{max}(s_i, c(s_j a_j / a_i + \Delta )),j\neq i` or in words: a constant modifier
  (:math:`c` about 0.1) times the weighted strength of the other unit (weight is ratio of attack values) plus a noise
  term math:`\Delta` with variance approx. 0.2 but which cannot be higher than our own strength in total
* Damage is calculated for both units and then subtracted from their strength
* Units with less than 30% strength will not attack anymore but flee automatically

No auto resolution of battle

* Actually there is auto battle, you can let an officer take over which will use AI routines. But apart from that the
  real model is used – no other calculations.

Special bonuses

* Encirclement factor of provinces = Number of own surrounding provinces minus Number of provinces of the enemy
  divided by the sum of both gives up to 50% bonus for attacker or defender. Reason: avoid isolated provinces in
  foreign territory, favor straight front lines
* Sea invasion ignores Encirclement factor but gives fixed 20% malus to invader because it is more difficult.
* How to add all bonuses? Additive? Multiplicative? Limit?

Strategic Combat
==========================

Tactical Combat
==========================

* Move and/or attack. Attack ends movement.
* Responsive fire maximally two times per turn.
* Entrenchment (defending bonus, if not moved last turn, only for infantry)
* terrain hills, mountains, cities and across river give a +1 bonus each (cumulative) on defense strength (i.e.
  attack value when in defending position)