"""
This module holds a mapper subclass used for a specialized US country 'mapper'.

See 'abstracts.py' for generic documentation about mapper objects.

Attribs:
    DIR (str) - Absolute filepath for this module's directory\n
    CONFIG_FILE (str) - Absolute filepath for this module's configuration file

Classes:
    MapperUS (Mapper): Class of 'mapper' object specialized for US *.svg map files only.

Info:
    :Date: 2017-01-31
    :Authors: B\. Seid
"""
# --- Internal Imports --- #
from mappers.abstracts import Mapper
# --- External Imports --- #
from shutil import copyfile
from os import path
import xml.etree.ElementTree as ET

# Global parameters
DIR = path.dirname(__file__)
CONFIG_FILE = path.join(DIR, "../config/USconfig.conf")


class MapperUS(Mapper):
    # TODO : Implement counties editing
    # TODO : Determine if need to add "states" or "counties" parameter to MapperUS object (self)
    # TODO : Test svg list searching by US counties. Needed for "change_region_color" and "get_region_color".

    index = 0
    """
    Class variable, keep track of # of open MapperUS objects.
    :type: int
    """

    _cfg = {}
    """
    Dictionary containing configuration variables from .conf file
    :type: dict
    """

    def __init__(self, stco="states"):
        """
        Constructor method for MapperUS.

        :param stco: "states" | "counties"
        :type stco: str
        """
        # Load configuration data
        exec(open(CONFIG_FILE).read(), self._cfg)

        # Create new mapfile based on class index
        f = path.join(DIR, self._cfg["FILE_SAVEAS"].format(MapperUS.index))
        MapperUS.index += 1
        ET.register_namespace("", self._cfg["NAMESPACE"])

        # Select type of map to copy over
        if str(stco) == "states":
            copyfile(path.join(DIR, self._cfg["FILE_STATES"]), f)
        elif str(stco) == "counties":
            raise NotImplementedError("County level map not implemented yet.")
            # copyfile(path.join(DIR, self._cfg["FILE_COUNTIES"]), f)
        else:
            # Bad value input, revert index and raise exception
            MapperUS.index -= 1
            raise ValueError("Invalid class argument. Choose 'states' or 'counties' only.")

        # Set properties
        self._mapfile = f
        root = ET.parse(f).getroot()
        t = root.find('.')
        self._mapheight = int(t.attrib['height'])
        self._mapwidth = int(t.attrib['width'])

    def __del__(self):
        super().__del__()  # delete mapfile

    def __str__(self):
        return str(self.map)

    _parse_tag = staticmethod(lambda root, tag: root.findall(".//*[@id='{0}']".format(tag)))
    """
    Find list of element ids associated with 'tag' in 'root' using findall(...).\n
    * ELEMENT MUST HAVE <... id='?'> AS ATTRIBUTE

    :param root: xml tree root to parse
    :type root: xml.etree.ElementTree
    :param tag: attribute to find
    :type tag: str

    :return: list of elements associated with 'tag' in 'root'
    :rtype: list[xml.etree.Element]
    """

    @Mapper.mapheight.setter
    def mapheight(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Map height cannot be 0 or less pixels.")

        # Write height to file
        tree = ET.parse(self.map)
        root = tree.getroot()
        t = root.find('.')
        t.attrib['height'] = str(value)
        tree.write(self.map)
        self._mapheight = value

    @Mapper.mapwidth.setter
    def mapwidth(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Map width cannot be 0 or less pixels.")

        # Write width to file
        tree = ET.parse(self.map)
        root = tree.getroot()
        t = root.find('.')
        t.attrib['width'] = str(value)
        tree.write(self.map)
        self._mapwidth = value

    def set_region_color(self, identifier, color):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Check in states list (if exists)
        try:
            states = MapperUS._parse_tag(root, self._cfg["ID_STATES"])[0]
            for child in states:
                if child.attrib["id"] == identifier:
                    child.attrib["fill"] = "#{:06x}".format(color)
                    tree.write(self.map)
                    break

            # Exit function
            return
        except IndexError as i:
            pass

        # Check in each of counties list (if exists)
        try:
            countieslist = MapperUS._parse_tag(root, self._cfg["ID_COUNTIES"])  # no [0], Multiple counties ids

            # Searching by counties not tested. Raise NotImplementedError until further testing as been done.
            raise NotImplementedError("Searching counties for US map not implemented this time.")
            # TODO : Implement change_region_color for counties

            # for counties in countieslist:
            #     for child in counties:
            #         if child.attrib["id"] == identifier:
            #             child.attrib["fill"] = "#{:06x}".format(color)
            #             tree.write(self.map)
            #             break
            #
            #     # Exit function
            #     return
        except IndexError as i:
            # No list found, should not happen
            raise Exception("No state/counties list found.")

    def set_region_number(self, identifier, number, color=None):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Check in states list (if exists)
        try:
            states = MapperUS._parse_tag(root, self._cfg["ID_NUMBERS"])[0]
            for child in states:
                if child.attrib["id"] == identifier:
                    child.text = str(number)
                    if color is not None:  # Change number color if given
                        child.attrib["fill"] = "#{:06x}".format(color)
                    tree.write(self.map)
                    break

            # Exit function
            return
        except IndexError as i:
            pass

        # Check in each of counties list (if exists)
        try:
            countieslist = MapperUS._parse_tag(root, self._cfg["ID_COUNTIES"])  # no [0], Multiple counties ids

            # Searching by counties not tested. Raise NotImplementedError until further testing as been done.
            raise NotImplementedError("Searching counties for US map not implemented this time.")
            # TODO : Implement change_region_number for counties

            # for counties in countieslist:
            #     for child in counties:
            #         if child.attrib["id"] == identifier:
            #             child.attrib["fill"] = "#{:06x}".format(color)
            #             tree.write(self.map)
            #             break
            #
            #     # Exit function
            #     return
        except IndexError as i:
            # No list found, should not happen
            raise Exception("No state/counties list found.")

    def get_region_color(self, identifier):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Check in states list (if exists)
        try:
            states = MapperUS._parse_tag(root, self._cfg["ID_STATES"])[0]
            for child in states:
                if child.attrib["id"] == identifier:
                    return int(child.attrib["fill"].lstrip("#"), 16)  # Convert from hex to int

            # Return none if no state found with string matching <identifier>
            return None
        except IndexError as i:
            pass

        # Check in each of counties list (if exists)
        try:
            countieslist = MapperUS._parse_tag(root, self._cfg["ID_COUNTIES"])  # no [0], Multiple counties ids

            # Searching by counties not tested. Raise NotImplementedError until further testing as been done.
            raise NotImplementedError("Searching counties for US map not implemented this time.")
            # TODO : Implement get_region_color for counties

            # for counties in countieslist:
            #     for child in counties:
            #         if child.attrib["id"] == identifier:
            #             return child.attrib["fill"]
            #
            # Return none if no county found with string matching <identifier>
            # return None
        except IndexError as i:
            # No list found, should not happen
            raise Exception("No state/counties list found.")

    def get_region_number(self, identifier):
        # Return number as an STRING
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Check in numbers list
        numbers = MapperUS._parse_tag(root, self._cfg["ID_NUMBERS"])[0]
        for child in numbers:
            if child.attrib["id"] == identifier:
                # If "text" has state abbrv. in it (e.g. VT 5), remove abbrv. and return
                if child.text[0:2].isalpha():
                    return str(child.text[3:].strip())
                # No state abbrv. found, return number
                else:
                    return str(child.text)
        # Return None if identifier not found
        return None

    def get_region_list(self):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Check for state list
        # states = root.findall(".//*[@id='states']")[0]
        try:
            states = MapperUS._parse_tag(root, self._cfg["ID_STATES"])[0]
            r = []
            for x in states:
                r.append(x.attrib["id"])
            if r is not None:
                return r
        except IndexError as i:
            pass

        # Check each counties list
        # counties = root.findall(".//*[@id='counties']")
        try:
            countieslist = MapperUS._parse_tag(root, self._cfg["ID_COUNTIES"])  # no [0], Multiple counties ids
            r = []
            for counties in countieslist:
                for x in counties:
                    r.append(x.attrib["id"])
            if r is not None:
                return r
        except IndexError as i:
            # No list found, should not happen
            raise Exception("No state/counties list found.")

# END OF FILE ////////////////////////////////////////////////////////////
