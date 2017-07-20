**************
State
**************

Short overview of the functionality of the game at current version 0.2.2.

- It shows a start screen with sensitive areas (help center, game lobby, preferences, editor, exit)

- It plays some background music (can be muted in the preferences)

- It displays some html pages (context sensitive) when clicking on the help center or on the little question marks in dialogs

    + The manual has to be built with tools/build_documentation.py before

    + The help is displayed in a browser on the running system, a qtwebengine implementation is available but not switched on

- The preferences dialog has a toolbar with placeholder icons (not made yet, see the tooltips for meaning) switching the
  widget below and some basic stuff to configure

- The editor screen allows to load the one scenario that is included (core/Europe1814.scenario), also a new scenario cac
  be created and an overview
  about the nations and provinces can be seen (as a list in the dialogs shown when clicking on the placeholder icons in
  the toolbar), set terrain (context menu on the map) might not work yet, graphics like borders, rivers, terrain is very crude, navigating
  the mini map with updates of the map should work

- The game lobby offers four tabs controlled by placeholder icons (start single player scenario inbuilt, load single player
  scenario, server game lobby, start multiplayer scenario)

    + Clicking on Europe1814 in the first tab shows a scenario preview which allows to select a nation and clicking on
      "start selected scenario" should show the main game screen but so far shows only a non-functional skeleton

- Internally there is a client-server infrastructure which communicates over TCP/IP as well as a scenario class which hold
  terrain, nations and provinces and allows to manipulate them