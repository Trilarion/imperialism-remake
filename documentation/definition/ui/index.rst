************************
User interface
************************

We start full screen and expect at least 1024 x 768 (see base/constants.py)

Conventions
===========================

* Style: Water color or pencil drawings
* Standard graphics format is Portable Network Graphics (png) because of wide adoption, losless compression and transparency
* More editable files (PhotoShop, CorelDraw) including all layers can and should be saved too

Screens
===========================

Start Screen
--------------------------

Actions

* Enter the Game lobby (start or continue single-, multiplayer game)
* Change Preferences
* Open help browser
* Open the Editor
* Exit

Main Map Screen
--------------------------

* Default Tile size is 80 x 80 pixel (square tiles)
* Terrain view as background (showing provinces, units, military movements)
* One right side: mini-map
* Selected unit function box
* Menu toolbar (all the different dialogs and help)
* Transport Dialog
* All, the dialogs (Transport, Industry, Trade) run in one Frame with top toolbar for other dialogs and help
* Listing for each commodity currently connected to transport network, slider bar representing the amount of each commodity to transport vs. total amount

Sound effects
===========================

* Click on a button
* ...

Various things
===========================

* There will be a real time clock in one corner of the screen, allowing even to set an alarm or a timer. But it also
  can be turned off if wished.
* Do we want to have customized mouse cursors? Easy to implement, but is there any real benefit? Mouse cursors should
  indicate possible actions.
* Savegames should have a screen shown always.
* Inbuilt functionality to make a screenshot.