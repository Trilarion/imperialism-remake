# Imperialism Remake

**[Home](http://remake.twelvepm.de/) - [Community](http://remake.twelvepm.de/forum/) - [Sources](https://github.com/Trilarion/Imperialism-Remake)
- [Download](http://remake.twelvepm.de/home/download/) - [Tasks](http://remake.twelvepm.de/tasks/) - [Contact](http://remake.twelvepm.de/home/contact/)**

## Getting Started

### 1. Access the source code

The [source code](https://github.com/Trilarion/Imperialism-Remake) is on GitHub. You can also download a zipped
[one-time snapshot](https://github.com/Trilarion/imperialism-remake/archive/master.zip). Otherwise just register
with GitHub and [fork the project](https://github.com/Trilarion/imperialism-remake).
	
### 2. Using Git

[Download Git](http://git-scm.com/downloads) or on Windows install [TortoiseGit](https://code.google.com/p/tortoisegit/)
which conveniently integrates git with the explorer.

Git is not easy. Be careful and read some instructions first. Among others I liked this [tutorial](https://www.atlassian.com/git/tutorials/syncing).

- Once you forked the project, clone it on your computer with "git clone https://github.com/USER/Imperialism-Remake.git"
- Regularly get updates with fetch/pull
- Programm as usual (commit)
- When task is done, create pull request (by pushing?). Have never done this. Don't know how this works exactly.

### 3. Python

Download and install latest [Python 3.X](https://www.python.org/downloads/). The [Python documentation](https://docs.python.org/3/) is quite good.

#### 32 or 64 bit on Windows
 
 In principle it doesn't matter. I use 64 bit and also deliver packages in 64 bit only.

### Third Party Modules for Python

Only PySide is required for running, Markdown and cx_Freeze are additionally required for developing.

#### PySide

[PySide](http://qt-project.org/wiki/PySide) is a Python binding of the Qt framework (very similar to PyQt). Follow the
[installation instructions](http://qt-project.org/wiki/Get-PySide). On Windows you can also use these [binaries](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyside).

Check the [API documentation](http://pyside.github.io/docs/pyside/) and also the underlying Qt 4.8 C++
[API classes overview](http://qt-project.org/doc/qt-4.8/classes.html) which is linked better.

#### Markdown

[Markdown](https://pypi.python.org/pypi/Markdown) is required for creating the HTML pages of the manual. 

#### cx_Freeze

[cx_Freeze](http://cx-freeze.sourceforge.net/) is used for packaging Python and creating standalone versions.

### 4. Start

- Execute "./tools/manual_markdown_converter.py" once with working directory "./tools"(all paths relative to repository root).
- Run file "./source/start.py" with working directory "./".
- Start with command line parameter "debug" for (more) output on the console.
- A folder with log files and settings is created under "user folder/Imperialism Remake User Data" where "user folder" is the typical user folder of your system (Windows C:/Users/XXX/).

### 5. IDE

I use [PyCharm Community Edition](http://www.jetbrains.com/pycharm/download/). Since the .idea folder is contained the project
can probably be opened directly with PyCharm. Another nice IDE is [Spyder](https://code.google.com/p/spyderlib/).

### 6. Tools

- [Inno Setup](http://www.jrsoftware.org/isinfo.php) is needed for the creation of the Windows installer.
- Many graphics are edited with [Inkscape](http://www.inkscape.org/en/).

### 7. Packaging

- Run `tools/package_vanilla.py` to create package in the build folder.

On Windows:

- Run `tools/package_windows.py`.
- Download the [VC 2010 x64 redistributable](http://www.microsoft.com/en-us/download/details.aspx?id=13523) and store 
in folder build.
- Run `tools/installer_windows.iss` with Inno Setup 