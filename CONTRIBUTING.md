## Introduction

Thank you for considering contributing to the [Imperialism Remake](http://remake.twelvepm.de/) project!

Volunteers are always welcome. There are plenty of chances to take part in coding,
graphics design, discussing the game rules or just giving feedback.

Most of these tasks can be discussed in the [community forum](http://remake.twelvepm.de/forum/),
please consider registering there.

## Feedback

For programmers direct interaction with the [github repository](https://github.com/Trilarion/imperialism-remake)
by forking and pushing merge requests are preferred. Please use the
[issues tracker](https://github.com/Trilarion/imperialism-remake/issues) to report problems.
Requests for enhancement should be posted in the community forum or if they are more technical
(coding related) also at the issues tracker.

## Getting started (programming)

### Sources

The [source code](https://github.com/Trilarion/Imperialism-Remake) is on GitHub.

The folder structure is as follow:

- `.idea` Workspace for Pycharm IDE
- `documentation` Game manuals as sphinx projects
- `examples` Code snippets demonstrating certain aspects of the code base. No tests
- `prototypes` Showcase implementation of larger parts of the game before they are integrated in the code base.
- `source` The code base of the game with game assets (artwork, sound, ..) located at `source/imperialism_remake/data`
- `test` Collection of tests.
- `tools` Helper scripts for creating content files, building the documentation, ..


#### Using Git

Please use the usual fork and create pull request scheme for suggesting changes to the code. Also see this tutorial
[learngitbranching](http://learngitbranching.js.org/). On Windows, [TortoiseGit](https://code.google.com/p/tortoisegit/)
conveniently integrates git with the explorer.

### Developer documentation

- [![Documentation Status](https://readthedocs.org/projects/imperialism-remake-definition/badge/?version=latest)](http://imperialism-remake-definition.readthedocs.io/en/latest/?badge=latest) Game Design
- [![Documentation Status](https://readthedocs.org/projects/imperialism-remake-developer/badge/?version=latest)](http://imperialism-remake-developer.readthedocs.io/en/latest/?badge=latest) Developer Manual

### Python environment

Install [Python 3.X](https://www.python.org/downloads/). See also the [Python documentation](https://docs.python.org/3/).

Only PyQt5 is required for running. Sphinx and ushahidi_sphinx_rtd_theme for creating the documentation.

#### PyQt5

[PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5) is a Python binding of the Qt framework and is required for running.

PyQt5 has not much [documentation](http://pyqt.sourceforge.net/Docs/PyQt5/) on its own but the [API classes overview](http://doc.qt.io/qt-5/classes.html)
of the underlying C++ Qt 5.X framework is very useful since PyQt5 is almost 100% recreating it. 

### Start the game

- Run file `source/imperialism_remake/start.py`
- Start with command line parameter "--debug" for (more) output on the console.
- A folder with log files and settings is created under "user folder/Imperialism Remake User Data" where "user folder" is the typical user folder of your system (Windows: C:/Users/XXX/, Linux: ~/.config/).

### Tests

All tests in folder `test` can be run by executing `test/run_tests.py`. We also use Travis CI to run the tests
automatically.

[![Build Status](https://travis-ci.org/Trilarion/imperialism-remake.svg?branch=master)](https://travis-ci.org/Trilarion/imperialism-remake)

### IDE

I use [PyCharm Community Edition](http://www.jetbrains.com/pycharm/download/). The `.idea` folder is included in the source, the project
can probably be opened directly with PyCharm.

### Packaging

Packaging on Linux and macOS has not progressed much so far. Windows packaging is with pynsist. Instructions will be added later.

