************************
Artificial Intelligence
************************

General requirements

* Three difficulty level: easy, normal, challenging
* Moderate thinking time
* Include elements of chance, but also predictable
* Some central switches: peacefulness, ruthlessness (diplomacy), special affections (technology, navy, ...)
* Memorize past actions during a game (maybe also between games but then can be turned off)
* Should communicate reasons for its actions

Minor Nations should

* act defensively (never wage war, not even on other minor nations)
* sell resources and buy consumer goods

Requirements
=========================

* Should have optional a personal flavor for each grand nation, definable by some sort of sliders (peacefulness,
  greediness, ...)
* Should have aims/goals like assimilation in X years, war in Y years and act according to these goals but also
  redefine them from time to time
* free parameters not determined by the goals are maximized for certain general criteria (money, military, industry)
* Military AI: takes roles (defender, attacker) but never defends completely, always at least tries to counter-attack
* Military AI: single provinces: rather defend (aggressive, cautious), rather attack(aggressive, cautious)
* Declare War, Beg for Peace and then shortly after Declare Ware again without rebuilding phase – this should not happen!
* As a inferior Nation an A.I should basically try to not attack meaningless but also not give in. Just concentrate
  on defending and surviving.

Rapid feedback
========================

I would like to test AIs fully automatic against each other. This means that I can adjust parameters and then let
them run against each other. Ideally I would also get online feedback from players playing against the AI, probably
more detailed than just who won. Possible benefits:

* Improve AI performance
* Find optimal parameters (preferences) depending on country and starting value
* Get fast feedback on new algorithms.