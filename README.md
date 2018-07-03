# Easy GUI

EasyGUI is a module for very simple, very easy GUI programming in Python. EasyGUI is different from other GUI
libraries in that EasyGUI is NOT event-driven. Instead, all GUI interactions are invoked by simple function calls.

## Getting Started

### Prerequisites

EasyGUI runs on Python 2 and 3, and does not have any dependencies beyond python and tkinter.

### Installing

Easy GUI is available PyPI so can be installed with PIP:

    $ pip install easygui
    # or 
    $ easy_install install easygui

Then to use it:

    >>> import easygui
    >>> easygui.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))
    1
    >>> easygui.msgbox('This is a basic message box.', 'Title Goes Here')
    'OK'
    >>> easygui.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))
    'Chocolate'

## Running the tests

Unit tests are currently being added, and can be run with unittest.

## Documentation

Full documentation is always available at [easygui.readthedocs.org](http://easygui.readthedocs.org/en/master/).

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - An awesome IDE
* [git](https://git-scm.com/) - Version Control
* [GitHub](https://github.com/) - Source Code hosting and collaboration
* [Travis CI](https://travis-ci.org/) - Continuous Integration

## Contributing

Please look at the [EasyGUI GitHub project](https://github.com/robertlugg/easygui)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/robertlugg/easygui/releases).

## Authors

* **Stephen R. Ferg** - *Initial work*
* **Robert M Lugg** - *Maintainer*
* **Alexander Zawadzki** - *Maintainer*

See also the list of [contributors](https://github.com/robertlugg/easygui/graphs/contributors) who participated in this project.

## License

This project is licensed under the Modified BSD License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Stephen Ferg for instigating this project! 
* Thanks to Juan José Denis Corrales for numerous contributions
