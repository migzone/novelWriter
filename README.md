# novelWriter

[![Linux (3.6)](https://github.com/vkbo/novelWriter/workflows/Linux%20(3.6)/badge.svg?branch=main)](https://github.com/vkbo/novelWriter/actions)
[![Linux (3.7)](https://github.com/vkbo/novelWriter/workflows/Linux%20(3.7)/badge.svg?branch=main)](https://github.com/vkbo/novelWriter/actions)
[![Linux (3.8)](https://github.com/vkbo/novelWriter/workflows/Linux%20(3.8)/badge.svg?branch=main)](https://github.com/vkbo/novelWriter/actions)
[![Linux (3.9)](https://github.com/vkbo/novelWriter/workflows/Linux%20(3.9)/badge.svg?branch=main)](https://github.com/vkbo/novelWriter/actions)
[![Windows (3.8)](https://github.com/vkbo/novelWriter/workflows/Windows%20(3.8)/badge.svg?branch=main)](https://github.com/vkbo/novelWriter/actions)
[![macOS (3.8)](https://github.com/vkbo/novelWriter/workflows/macOS%20(3.8)/badge.svg?branch=main)](https://github.com/vkbo/novelWriter/actions)
[![flake8](https://github.com/vkbo/novelWriter/workflows/flake8/badge.svg)](https://github.com/vkbo/novelWriter/actions)
[![codecov](https://codecov.io/gh/vkbo/novelWriter/branch/main/graph/badge.svg)](https://codecov.io/gh/vkbo/novelWriter)
[![docs](https://readthedocs.org/projects/novelwriter/badge/?version=latest)](https://novelwriter.readthedocs.io/en/latest/?badge=latest)
[![release](https://img.shields.io/github/v/release/vkbo/novelwriter)](https://github.com/vkbo/novelWriter/releases)
[![pypi](https://img.shields.io/pypi/v/novelwriter)](https://pypi.org/project/novelWriter)
[![python](https://img.shields.io/pypi/pyversions/novelwriter)](https://pypi.org/project/novelWriter)

<img align="left" style="margin: 0 16px 4px 0;" src="https://raw.githubusercontent.com/vkbo/novelWriter/main/setup/icons/scaled/icon-novelwriter-96.png">

novelWriter is a Markdown-like text editor designed for writing novels and larger projects of many
smaller plain text documents. It uses its own flavour of Markdown that supports a meta data syntax
for comments, synopsis, and cross-referencing between files. It's designed to be a simple text
editor that allows for easy organisation of text files and notes, built on plain text files for
robustness.

The plain text storage is suitable for version control software, and also well suited for file
synchronisation tools. The core project structure is stored in a project XML file. Other meta data
is primarily saved in JSON files.

The full documentation is available at
[novelwriter.readthedocs.io](https://novelwriter.readthedocs.io/).

The contributing guide is available in [CONTRIBUTING](CONTRIBUTING.md).


### Development Status

The application is still under initial development, but all core features have now been added.
The core functionality has been in place for a while, and novelWriter is being used for writing
projects by the author and collaborators.

No new major features will be added at this time, until the application is stable. Until then,
novelWriter is in a _beta_ state. Please report any issues you encounter via the repository's issue
tracker.

You should be able to use novelWriter for real projects, but as with all software, please make
regular backups of your data. There is a built in backup feature that can pack the entire project
into a zip file each time the main window or the project is closed. Please check the documentation
for further details.


## Implementation

The application is written in Python 3 using Qt5 via PyQt5. It is developed on Linux, but it should
in principle work fine on other operating systems as well as long as dependencies are met. The unit
tests are run on the latest versions of Ubuntu Linux, Windows Server and macOS.


# Installing and Running

novelWriter is available on [pypi.org](https://pypi.org/project/novelWriter/), and can be installed
with:
```bash
pip install novelwriter
```

To upgrade an existing installation, use:
```bash
pip install --upgrade novelwriter
```

Dependencies are installed automatically, but can generally be installed with:
```bash
pip install -r requirements.txt
```

Below are some brief instructions on how to get started on different operating systems.


## Linux

Either download the source, or install with pip.

If you run from source, install the dependencies via pip, or directly from the OS repo. There are
very few dependencies, and they should be available in the standard repo. The Python packages
needed are `pyqt5`, `lxml` and `pyenchant`.

### Installing from Source

You can also install novelWriter from source with:
```bash
python3 setup.py sample
sudo python3 setup.py install
sudo python3 setup.py launcher
```

The last line will install the application icons and set up a launcher for novelWriter. The method
uses hardcoded paths, so it may or may not work for your Linux distro. If you have any issues,
please submit a ticket so the script can be tuned.

The script may prompt you to choose which executable to configure if it finds more than one.

### Running from Source

If you want to run directly from the source, the application can be started with:
```bash
./novelWriter.py
```

You can also create a launcher for running directly from source with:
```bash
python3 setup.py xdg-install
```
This will install the launcher and icons for the current user. To install them system-wide, run the
above command with `sudo` or as root.

For more install options, see [Build and Install novelWriter](setup/README.md).


## macOS

These instructions assume you're using brew, and have Python and pip set up. If not, see the
[brew docs](https://docs.brew.sh/Homebrew-and-Python) for help.

Main requirements are installed via the requirements file. You also need to install the `pyobjc`
package on macOS, so you must run:
```bash
pip3 install --user -r requirements.txt
pip3 install --user pyobjc
```

For spell checking you may also need to install the enchant package. It comes with a lot of default
dictionaries.
```bash
brew install enchant
```

## Windows

On Windows, you may first need to install Python. See the [python.org](https://www.python.org/)
website for download packages. It is recommended that you install the latest version of Python 3.8.

To install dependencies, run:
```bash
pip install --user -r requirements.txt
```

**Note:** On Windows, make sure Python3 is in your PATH if you want to launch novelWriter from
command line. You can also right click the `novelWriter.py` file, create a shortcut, then right
click again, select "Properties" and change the target to your python executable and
`novelWriter.py`.

It should look something like this:
```
C:\...\AppData\Local\Programs\Python\Python38\python.exe novelWriter.py
```

You can also run the `make.py` script to generate a single executable, or an installer.
See [Build and Install novelWriter](setup/README.md) for more details.


## Package Versions

Exporting to Markdown requires PyQt/Qt 5.14. There are no known minimum for `lxml`, but the code
was originally written with 4.2. The optional spell check library must be at least 3.0.0 to work
with Windows 64 bit systems. On Linux, 2.0.0 also works fine.

If no external spell checking tool is installed, novelWriter will use a basic spell checker based
on standard Python package `difflib`. Currently, only English dictionaries are available for this
spell checker, but more can be added to the `nw/assets/dict` folder. See the
[README](nw/assets/dict/README.md) file in that folder for how to generate more dictionaries. Note
that the difflib-based option is both slow and limited.

## Debugging

If you need to debug novelWriter, you must run it from command line. It takes a few parameters,
which can be listed with the switch `--help`. The `--info`, `--debug` or `--verbose` flags are
particularly useful for increasing logging output for debugging.


# Key Features

Some features of novelWriter are listed below. Consult the documentation for more information.

### Markdown Flavour

novelWriter is _not_ a full-feature Markdown editor. It allows for a minimal set of formatting
needed for writing text documents for novels. These are currently limited to:

* Headings level 1 to 4 using the `#` syntax only.
* Emphasised and strong text. These are rendered as italicised and bold.
* Strikethrough text.
* Hard line breaks using two or more spaces at the end of a line.

That is it. Features not supported in the editor are also not exported when using the export tool.

In addition, novelWriter adds the following, which is otherwise not supported by Markdown:

* A line starting with `%` is treated as a comment and not rendered on exports unless requested.
  Comments do not count towards the word count. If the first word of the comment is `synopsis:`,
  the comment is indexed and treated as the synopsis for the section of text under the same header.
  These synopsis comments can be used to build an outline and exported to external documents.
* A set of meta data keyword/values starting with the character `@`. This is used for tagging
  and inter-linking documents, and can be used to generate a project outline.
* Non-breaking spaces are supported as long as your system is using at least Qt 5.9. For earlier
  version, non-breaking spaces are converted to normal spaces when saving the document. This is
  done by the Qt library.
* Thin spaces are also supported, as well as non-breaking thin spaces, with the same library
  version restriction as above.
* Tabs can be used in the text, and should be properly aligned. The width of a tab in pixels can be
  changed in Preferences. Note that for the HTML format, most browsers will treat a tab as a space,
  so it may not show up like expected. If you import the HTML file to Libre Office, for instance,
  they should appear as expected.

The core export format of novelWriter is HTML5. You can also export the entire project as a single
novelWriter Markdown-flavour document. In addition, other exports to Open Document, PDF, and plain
text is offered through the Qt library, although with limitations to formatting.

The HTML format is well suited for file conversion tools and import into other text editors.


### Colour Themes

The editor has syntax highlighting for the features it supports, and includes a set of different
syntax highlighting themes. The GUI also has an optional dark theme in addition to the default
system theme.

New themes can easily be added to the `nw/assets/themes` folder. Have a look in the existing
folders for examples of how to define the colours.


### Easy Organising of Project Files

The structure of the project is shown on the left hand side of the main GUI. Project files are
organised into root folders, indicating what class of file they are. The most important root folder
is the Novel folder, which contains all of the files that makes up the finished novel. Each root
folder can have subfolders. Folders have no impact on the final project structure, they are purely
tools for organising the files in whatever way the user needs.

The editor supports four levels of headings, which determines what level the following text belongs
to. Headings of level one signify a book or partition title. Headings of level two signify the
start of a new chapter. Headings of level three signify the start of a new scene. Headings of level
four can be used internally in each scene to separate sections.

Each novel file can be assigned a layout format, which shows up as a flag next to the item in the
project tree. These are mostly to help the user track what they contain, but they also have some
impact on the format of the exported document. See the documentation for further details.


#### Project Notes

Supporting note files can be added for the story plot, characters, locations, story timeline, etc.
These have their separate root folders. These are optional files.


### Visualisation of Story Elements

The different notes can be assigned tags, which other files can refer back to using the `@` meta
keywords. This information can be used to display an outline of the story, showing where each scene
connects to the plot, and which characters, etc. occur in them. In addition, the tags themselves
are clickable in the document view pane, and control-clickable in the editor. They make it possible
to quickly navigate between the documents while editing.


## Licenses

This is Open Source software, and novelWriter is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](LICENSE.md) file.

Bundled assets have the following licenses:

* The Typicon-based icon themes by Stephen Hutchings are licensed under
  [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/). The icons have been altered in
  size and colour for use with novelWriter, and some additional icons added. The original icon set
  is available at
  [stephenhutchings/typicons.font](https://github.com/stephenhutchings/typicons.font).
* The Cantarell font by Dave Crossland is licensed under
  [OPEN FONT LICENSE Version 1.1](http://scripts.sil.org/OFL).
  It is available at [Google Fonts](https://fonts.google.com/specimen/Cantarell).
* The Tomorrow syntax themes use colour schemes taken from Chris Kempson's collection of code
  editor themes, licensed with the
  [MIT License](https://github.com/chriskempson/tomorrow-theme/blob/master/LICENSE.md),
  and the main repo is available at
  [chriskempson/tomorrow-theme](https://github.com/chriskempson/tomorrow-theme).
* Likewise, the Owl syntax themes use colours from Sarah Drasner's code editor themes, licensed
  with the [MIT License](https://github.com/sdras/night-owl-vscode-theme/blob/master/LICENSE), and
  the main repo is available at
  [sdras/night-owl-vscode-theme](https://github.com/sdras/night-owl-vscode-theme).


## Screenshot

**novelWriter with default system theme:**
![Screenshot 1](https://raw.githubusercontent.com/vkbo/novelWriter/main/docs/source/images/screenshot_default.png)

**novelWriter with dark theme:**
![Screenshot 2](https://raw.githubusercontent.com/vkbo/novelWriter/main/docs/source/images/screenshot_dark.png)
