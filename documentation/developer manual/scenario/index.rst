**************
Scenario
**************

Introduction
============

Server Scenario
===============

Scenario Editor
===============

Scenarios can be edited completely with the scenario editor. Game rules are soft coded. Game logic must of course be somewhat hard coded but we try to allow as much freedom as possible.

During development, need to update between versions!

Scenario parameters
* Name of scenario
* Description of scenario
* Date (year, season), Turns, ...
* Map (see Map parameters)
* Major country description
* State of industry, work force, army, specialists for each country
* State of research, diplomatic relations, gold for each country

Map parameters
* Name
* Size
* Distribution of terrain, resources, infrastructure
* Borders, Provinces, Name of provinces
* Countries (Major, Minor)

Client Scenario
===============

Scenario File Format
====================

Game data is stored in zipped YAML (JSON like) files. We have scenarios. Saved games are also valid scenarios. There is automatic saving. Upon starting (loading) a scenario, some parameters can be changed, but not all.

Adjustable parameters of stored save games upon load:
* Player nation
* Difficulty level of AI opponents

If a scenario file refers to sub-files, store a hash value to make sure the referred file is the valid one.

During development, need to update between versions!