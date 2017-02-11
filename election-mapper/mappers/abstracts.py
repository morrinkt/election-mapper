"""
INTRO
=====
Summary
-------
This module holds abstracts class meant to be subclassed by specialized country 'mapper' and 'electoral' classes.

An abstract class structure was used due to the varying nature of maps and SVG code between different countries. This
structure allows for a country's subclass to implement this 'API' best optimized for that country's exact SVG code on
a **PURELY GRAPHICAL LEVEL** (i.e. only graphical changes.). An external client should edit 'any' country's map using
this interface.

Mappers
-------
A 'mapper' class should be able to dynamically edit a SVG file containing a map. This includes changing the fill colors
of regions, changing numbers (if present), retrieving region colors, numbers and lists of regions.

Election Mappers
----------------
An 'electoral' class should be able add or remove candidates (name, squares, pictures), update the electoral vote bar,
and candidate's EV numbers. It is a pure graphical manipulator class. Logic or calculations based on the map's features
(e.g. compare candidate's votes to other candidate) should be handled by an external class.

CLASSES
=======
    Mapper (ABCMeta): Abstract class of 'mapper' objects.\n
    Electoral (ABCMeta): Abstract class for objects that add, remove and keep track of candidates.

EXAMPLE
=======
    MapperUS - implements abstract class Mapper to create and edit *.svg US map files.\n
    ElectionUS - implements abstract class Electoral and class MapperUS to create *.svg US election maps.

INFO
====
    :Date: 2017-01-31
    :Authors: B\. Seid
"""
from abc import ABCMeta, abstractmethod
from os import remove

class Mapper(metaclass=ABCMeta):
    """
    Abstract class class meant to be subclassed by specialized country 'mapper' classes.
    """

    _mapfile = None
    """
    filepath location of *.svg map to be dynamically edited during runtime.
    Should not be modified except at object __init__.
    :type : str
    """

    _mapheight = None
    """
    height of svg map in pixels.
    :type : int
    """

    _mapwidth = None
    """
    width of svg map in pixels.
    :type : int
    """

    @abstractmethod
    def __init__(self, mapfile):
        """
        Constructor method.

        :param mapfile: filename of *.svg map to edit
        :type mapfile: str
        """
        self._mapfile = mapfile

    @abstractmethod
    def __del__(self):
        """Destructor method."""
        remove(self.map)

    @property
    def map(self):
        """
        :return: mapfile filename.
        :rtype: str
        """
        return self._mapfile

    @property
    def mapheight(self):
        """
        :return: height of svg map in pixels.
        :rtype: int
        """
        return self._mapheight

    @mapheight.setter
    @abstractmethod
    def mapheight(self, value):
        """
        Set the value of the *.svg map height.

        :param value: new height of map in pixels.
        :type value: int
        """
        raise NotImplementedError

    @property
    def mapwidth(self):
        """
        :return: width of svg map in pixels.
        :rtype: int
        """
        return self._mapwidth

    @mapwidth.setter
    @abstractmethod
    def mapwidth(self, value):
        """
        Set the value of the *.svg map width.

        :param value: new width of map in pixels.
        :type value: int
        """
        raise NotImplementedError

    @abstractmethod
    def set_region_color(self, identifier, color):
        """
        Change the color of a state/providence.

        :param identifier: identifier of state/providence
        :type identifier: str

        :param color: color in RGB hex (0x??????)
        :type color: int

        :return:
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def set_region_number(self, identifier, number, color=None):
        """
        Change the **number** of a state/providence (if exists).

        :param identifier: identifier of state/providence
        :type identifier: str

        :param number: integer to change to
        :type number: int

        :param color: color of number in RGB hex (0x??????). If None, color is unchanged.
        :type color: None | int

        :return:
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_region_color(self, identifier):
        """
        Retrieve color of region <identifier>.

        :param identifier: identifier of state/providence
        :type identifier: str

        :return: color of region in RGB hex (0x??????).
        :rtype: int
        """
        raise NotImplementedError

    @abstractmethod
    def get_region_number(self, identifier):
        """
        Retrieve integer of number of region (if exists).

        :param identifier: identifier of region
        :type identifier: str

        :return: string of text in number attribute of identifier
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_region_list(self):
        """
        Get list of all regions.

        :return: array of strings
        :rtype: list[str]
        """
        raise NotImplementedError


class Electoral(metaclass=ABCMeta):
    """
    Abstract class class meant to be subclassed by specialized country 'election map' classes.
    """

    @abstractmethod
    def get_candidate_list(self):
        """
        Get list of candidates and their colors.

        :return: list of tuples with candidate name and color in RGB hex.
        :rtype: list[(str,int)]
        """
        raise NotImplementedError

    @abstractmethod
    def add_candidate(self, name, color, picture=None):
        """
        Adds a candidate to the map.

        :param name: name of candidate
        :type name: str

        :param color: color in RGB hex (0x??????)
        :type color: int

        :param picture: filepath of candidate picture to add
        :type picture: None | str

        :return:
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def remove_candidate(self, name):
        """
        Removes a candidate from the map.\n
        *** THIS METHOD SHOULD NOT REMOVE THE COLORED REGIONS THIS CANDIDATE HELD.

        :param name: name of candidate
        :type name: str

        :return:
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_candidate_regions(self, name):
        """
        Get list of colored regions held by 'name':\n
        * If name is a string, retrieve name's color and find regions.\n
        * If name is an integer, turn to RGB hex and find by color.\n

        :param name: name of candidate OR color of candidate
        :type name: str | int

        :return: list of identifiers colored with candidate's color.
        :rtype: list[str]
        """
        raise NotImplementedError

    @abstractmethod
    def set_candidate_votes(self, name, votes, color=None):
        """
        Sets the 'vote' number for a candidate in the map.

        :param name: name of candidate
        :type name: str

        :param votes: number of votes candidate has.
        :type votes: int

        :param color: color of vote in RGB hex (0x??????). If None, color is unchanged.
        :type color: None | int

        :return:
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def set_candidate_color(self, name, color):
        """
        Sets the candidate's color to <color>.\n
        *** THIS METHOD SHOULD NOT CHANGE THE COLOR OF CANDIDATE'S "REGIONS".

        :param name: name of candidate
        :type name: str

        :param color: color to change to in RGB hex (0x??????).
        :type color: int

        :return:
        :rtype: None
        """

    @abstractmethod
    def set_bar(self, data):
        """
        Set the electoral vote bar, parliament seats, or other "counting" system up with given values
        from user in <dic>.

        This 'bar' may include some logic to graphically show who wins the 'election' after values are given.

        :param data: User values needed to set up the election 'bar'.
        :type data: dict

        :return:
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def set_title(self, title=None, color=None):
        """
        Set the title of the election map.

        :param title: title of election map. If None, title is removed.
        :type title: (str)

        :param color: color of title in RGB hex (0x??????). If None, color is unchanged.
        :type color: (int)

        :return:
        :rtype: None
        """
        raise NotImplementedError

# END OF FILE ////////////////////////////////////////////////////////////
