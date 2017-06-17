# Imperialism Remake

**[Home](http://remake.twelvepm.de/) - [Community](http://remake.twelvepm.de/forum/) - [Sources](https://github.com/Trilarion/Imperialism-Remake) - [Download](http://remake.twelvepm.de/home/download/) - [Tasks](http://remake.twelvepm.de/tasks/) - [Contact](http://remake.twelvepm.de/home/contact/)**

## Documentation

- [![Documentation Status](https://readthedocs.org/projects/imperialism-remake/badge/?version=latest)](http://imperialism-remake.readthedocs.io/en/latest/?badge=latest) Player Manual
- [![Documentation Status](https://readthedocs.org/projects/imperialism-remake-definition/badge/?version=latest)](http://imperialism-remake-definition.readthedocs.io/en/latest/?badge=latest) Game Design
- [![Documentation Status](https://readthedocs.org/projects/imperialism-remake-developer/badge/?version=latest)](http://imperialism-remake-developer.readthedocs.io/en/latest/?badge=latest) Developer Manual

## Test

[![Build Status](https://travis-ci.org/Trilarion/imperialism-remake.svg?branch=master)](https://travis-ci.org/Trilarion/imperialism-remake)

## Getting Started

### Access the source code

The [source code](https://github.com/Trilarion/Imperialism-Remake) is on GitHub. You can also download a zipped
[one-time snapshot](https://github.com/Trilarion/imperialism-remake/archive/master.zip). Otherwise just register
with GitHub and [fork the project](https://github.com/Trilarion/imperialism-remake).
	
### Using Git

[Download Git](http://git-scm.com/downloads) or on Windows install [TortoiseGit](https://code.google.com/p/tortoisegit/)
which conveniently integrates git with the explorer.

Git is not easy. Be careful and read some instructions first. I liked this [tutorial](https://www.atlassian.com/git/tutorials/syncing).

- Once you forked the project, clone it on your computer with "git clone https://github.com/USER/Imperialism-Remake.git"
- Regularly get updates with fetch/pull
- Programm as usual (commit)
- When task is done, create pull request.

### Python

Download and install latest [Python 3.X](https://www.python.org/downloads/). The [Python documentation](https://docs.python.org/3/) is quite good.

#### 32 or 64 bit on Windows
 
 Although it doesn't matter here, I use 64 bit and also deliver packages in 64 bit only.

### Third Party Modules for Python

Only PyQt5 and PyYAML are required for running.

Sphinx, PyInstaller are additionally required for development.

#### PyQt5

[PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5) is a Python binding of the Qt framework and is required for running.

PyQt5 has not much [documentation](http://pyqt.sourceforge.net/Docs/PyQt5/) on its own but the [API classes overview](http://doc.qt.io/qt-5/classes.html)
of the underlying C++ Qt 5.X framework is very useful since PyQt5 is almost 100% recreating it.  

#### PyYAML

[PyYAML](http://pyyaml.org/wiki/PyYAML) is required for running.

### Start

- Run file "./source/start.py" with working directory "./".
- Start with command line parameter "--debug" for (more) output on the console.
- A folder with log files and settings is created under "user folder/Imperialism Remake User Data" where "user folder" is the typical user folder of your system (Windows C:/Users/XXX/).

### IDE

I use [PyCharm Community Edition](http://www.jetbrains.com/pycharm/download/). Since the .idea folder is contained the project
can probably be opened directly with PyCharm. Another nice IDE is [Spyder](https://code.google.com/p/spyderlib/).

### Tools

- [Inno Setup](http://www.jrsoftware.org/isinfo.php) is needed for the creation of the Windows installer.
- Many graphics are edited with [Inkscape](http://www.inkscape.org/en/).

### Packaging

Under construction.