"""
This module holds an election mapper subclass used for a specialized US country 'election mapper'.

See 'abstracts.py' for generic documentation about mapper and electoral objects.

Attribs:
    DIR (str) - Absolute filepath for this module's directory\n
    CONFIG_FILE (str) - Absolute filepath for this module's configuration file

Classes:
    ElectionUS (MapperUS, Electoral): Class of 'mapperUS' and 'Electoral' object specialized for US election maps only.

Info:
    :Date: 2017-02-08
    :Authors: B\. Seid
"""
# --- Internal Imports --- #
from mappers.abstracts import Electoral
from mappers.mapperUS import MapperUS
# --- External Imports --- #
from os import path
import xml.etree.ElementTree as ET

# Global parameters
DIR = path.dirname(__file__)
CONFIG_FILE = path.join(DIR, "../config/USconfig.conf")


class ElectionUS(MapperUS, Electoral):

    def __init__(self, stco="states"):
        """
        Constructor method for ElectionUS.

        :param stco: "states" | "counties"
        :type stco: str
        """
        # Set up initial svg map
        MapperUS.__init__(self, stco)

        # Modify svg map for 'election' mode
        ET.register_namespace("", self._cfg["NAMESPACE"])

        # Add election elements to map
        self._add_election_elements()

    def _add_election_elements(self):
        """
        Private function to add all necessary 'election' elements to svg map.

        :return:
        :rtype: None
        """
        # Add to map height -------------------- #
        # <dy> = extra translation distance for current map elements
        dy = int(self._cfg["dist_tte"]) + \
            int(self._cfg["dist_etb"]) + \
            int(self._cfg["dist_btm"]) + \
            int(self._cfg["bar_h"]) + \
            int(self._cfg["trg_h"])
        self.mapheight = self.mapheight + \
            dy + \
            int(self._cfg["candpic_h"]) * 1.2 + \
            int(self._cfg["candev_d"]) + \
            int(self._cfg["candev_botb"])

        # Translate all current elements down by <dy> to create room -------------------- #
        tree = ET.parse(self.map)
        root = tree.getroot()
        for ele in root[1:]:  # exclude <title> element
            ele.attrib["transform"] = ElectionUS._update_translation("translate(0 {y})", y=dy)

        # Translate "CC" text to very bottom
        cc = MapperUS._parse_tag(root, "cc")[0]
        cc.attrib["transform"] = ElectionUS._update_translation("translate(0 {y}", y=self.mapheight-5)
        cc.attrib["y"] = "0"

        # Add blank title ;text; element -------------------- #
        titleattribs = {
            "id": "title",
            "x": str(self.mapwidth / 2),
            "y": str(self._cfg["dist_tte"]),
            "font-family": self._cfg["title_font"],
            "font-size": str(self._cfg["title_size"]),
            "font-weight": self._cfg["title_lbs"],
            "text-anchor": self._cfg["title_anch"],
            "fill": "#000000"
        }
        ele_title_txt = ET.Element(
            "{namespace}text".format(namespace="{" + self._cfg["NAMESPACE"] + "}"),
            attrib=titleattribs
        )
        ele_title_txt.text = " "
        root.append(ele_title_txt)

        # Add blank bar elements (blank bar + triangles) -------------------- #
        # General element
        xpos_bar = (self.mapwidth - int(self._cfg["bar_w"])) / 2
        ypos_bar = int(self._cfg["dist_tte"]) + int(self._cfg["dist_etb"])
        ele_bar = ET.Element(
            "{namespace}g".format(namespace="{" + self._cfg["NAMESPACE"] + "}"),
            attrib={
                "id": self._cfg["ID_BAR"],
                "transform": "translate({x} {y})".format(x=xpos_bar, y=ypos_bar)
            }
        )

        # Blank bar
        ET.SubElement(
            ele_bar,
            "rect",
            attrib={
                "id": "blank-bar",
                "height": str(self._cfg["bar_h"]),
                "width": str(self._cfg["bar_w"]),
                "fill": "#{c}".format(c=self._cfg["bar_c"]),
                "x": "0",
                "y": "0",
            }
        )

        # Blank triangles
        bw = int(self._cfg["bar_w"])
        bh = int(self._cfg["bar_h"])
        td = int(self._cfg["trg_d"])
        tw = int(self._cfg["trg_w"])
        th = int(self._cfg["trg_h"])
        pointsup = "{ax},{ay} {bx},{by} {cx},{cy}".format(
            ax=bw/2,
            ay=td*-1,
            bx=bw/2 + tw/2,
            by=td*-1 - th,
            cx=bw/2 - tw/2,
            cy=td*-1 - th
        )
        pointsdown = "{ax},{ay} {bx},{by} {cx},{cy}".format(
            ax=bw / 2,
            ay=td + bh,
            bx=bw / 2 + tw / 2,
            by=td + bh + th,
            cx=bw / 2 - tw / 2,
            cy=td + bh + th
        )
        ET.SubElement(
            ele_bar,
            "polygon",
            attrib={
                "id": "triup",
                "points": pointsup,
                "fill": "#{c}".format(c=self._cfg["bar_c"])
            }
        )
        ET.SubElement(
            ele_bar,
            "polygon",
            attrib={
                "id": "tridown",
                "points": pointsdown,
                "fill": "#{c}".format(c=self._cfg["bar_c"])
            }
        )

        # Append all elements
        root.append(ele_bar)

        # Add candidate names list element -------------------- #
        ele_names = ET.Element(
            "{namespace}g".format(namespace="{" + self._cfg["NAMESPACE"] + "}"),
            attrib={
                "id": self._cfg["ID_CAND_NM"],
                "transform": "translate{0}".format(self._cfg["candname_pos1"]),
                "font-family": self._cfg["candname_font"],
                "font-size": str(self._cfg["candname_size"]),
                "font-weight": self._cfg["candname_lbs"]
            }
        )
        root.append(ele_names)

        # Add candidate squares list element -------------------- #
        ele_sqrs = ET.Element(
            "{namespace}g".format(namespace="{" + self._cfg["NAMESPACE"] + "}"),
            attrib={
                "id": self._cfg["ID_CAND_SQ"],
                "transform": "translate{0}".format(self._cfg["candsq_pos1"])
            }
        )
        root.append(ele_sqrs)

        # Add candidate pictures list element -------------------- #
        ele_pics = ET.Element(
            "{namespace}g".format(namespace="{" + self._cfg["NAMESPACE"] + "}"),
            attrib={
                "id": self._cfg["ID_CAND_PX"],
                "transform": "translate(0 {y})".format(y=self._cfg["candpic_ypos"])
            }
        )
        root.append(ele_pics)

        # Add candidate votes list element -------------------- #
        ele_votes = ET.Element(
            "{namespace}g".format(namespace="{" + self._cfg["NAMESPACE"] + "}"),
            attrib={
                "id": self._cfg["ID_CAND_EV"],
                "transform": "translate(0 {y})".format(
                    y=int(self._cfg["candpic_ypos"]) + int(self._cfg["candev_d"]) + int(self._cfg["candpic_h"])
                ),
                "font-family": self._cfg["candev_font"],
                "font-size": str(self._cfg["candev_size"]),
                "font-weight": self._cfg["candev_lbs"]
            }
        )
        root.append(ele_votes)

        # Write to file
        tree.write(self.map)

    @staticmethod
    def _update_translation(cur_translate, x=None, y=None):
        """
        Update the transform text with <x> pixels.
        Private class method for ElectionUS objects.

        Example:
            x = 100, y = 500\n
            "translate(150 300)" --> "translate(100 500)"\n
            x = 333, y = None\n
            "translate(150 300)" --> "translate(333 300)"\n

        :param cur_translate: current translate text.
        :type cur_translate: str
        :param x: x position. If None, keep original.
        :type x: None | int
        :param y: y position. If None, keep original.
        :type y: None | int

        :return: new translate text
        :rtype: str
        """
        spl = cur_translate.strip().split(" ")
        x = int(spl[0].lstrip("translate(")) if x is None else x
        y = int(spl[-1].rstrip(")")) if y is None else y
        return "translate({x} {y})".format(x=x, y=y)

    def remove_candidate(self, name):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # ********** REMOVE SINGLE CANDIDATE FIRST ********** #
        namelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_NM"])[0]
        squarelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_SQ"])[0]
        piclist = MapperUS._parse_tag(root, self._cfg["ID_CAND_PX"])[0]
        votelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_EV"])[0]

        # Check list lengths
        n = len(namelist)
        if len(squarelist) != n | len(piclist) != n | len(votelist) != n:
            raise Exception("Candidate lists do not match.")

        # Go through each list and find first instance of <name> xml element to remove
        def _remove_from_list(_name, _list):
            """
            Remove a candidate from given Element list.
            Private method for ElectionUS.remove_candidate.

            :param _name: name of candidate
            :type _name: (str)
            :param _list: list of candidate attributes
            :type _list: list[xml.etree.Element]
            :return:
            :rtype: None
            """
            for _x in _list:
                if _x.attrib["id"].lower() == str(_name).lower():
                    _list.remove(_x)
                    return

        _remove_from_list(name, namelist)
        _remove_from_list(name, squarelist)
        _remove_from_list(name+"-pic", piclist)
        _remove_from_list(name+"-border", piclist)
        _remove_from_list(name+"-votes", votelist)

        # Write to file
        tree.write(self.map)

        # ********** UPDATE REST OF CANDIDATES ********** #
        # Reload parse
        tree = ET.parse(self.map)
        root = tree.getroot()
        namelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_NM"])[0]
        squarelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_SQ"])[0]
        piclist = MapperUS._parse_tag(root, self._cfg["ID_CAND_PX"])[0]
        votelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_EV"])[0]

        # Check list lengths
        n = len(namelist)
        if len(squarelist) != n | int(len(piclist)/2) != n | len(votelist) != n:  # Check all lists before proceeding
            raise Exception("Candidate lists do not match.")

        # Update candidate positions
        k = 0
        for c in namelist:
            c.attrib["y"] = str(k * int(self._cfg["candname_yadd"]))
            k += 1

        k = 0
        for c in squarelist:
            c.attrib["y"] = str(k * int(self._cfg["candsq_yadd"]))
            k += 1

        j, k = 0, 0  # Picture list has twice as many elements (pictures + borders)
        dxt = int(self._cfg["candpic_w"]) + int(self._cfg["candpic_dx"])
        for c in piclist:
            c.attrib["x"] = str(k * dxt)
            j += 1
            if (j % 2) == 0:
                k += 1

        k = 0
        for c in votelist:
            c.attrib["x"] = str(k * dxt)
            k += 1

        # Update picture list and vote list translations (required every time)
        pw = int(self._cfg["candpic_w"])
        pdx = int(self._cfg["candpic_dx"])
        lw = pw * n + pdx * (n - 1)
        t1 = int((self.mapwidth / 2) - (lw / 2))  # picture list x-translate
        t2 = int(t1 + pw / 2)  # vote list x-translate

        piclist.attrib["transform"] = ElectionUS._update_translation(piclist.attrib["transform"], x=t1)
        votelist.attrib["transform"] = ElectionUS._update_translation(votelist.attrib["transform"], x=t2)

        # Update name list and square list translations, if # of candidates goes back below switch case
        if n < self._cfg["SWC_CANDS"]:
            pass  # TODO : Add routine for updating translation of names/squares going below switch case

        # Write and exit function
        tree.write(self.map)
        return

    def get_candidate_list(self):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Check list lengths
        namelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_NM"])[0]
        squarelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_SQ"])[0]
        piclist = MapperUS._parse_tag(root, self._cfg["ID_CAND_PX"])[0]
        votelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_EV"])[0]
        n = len(namelist)
        if len(squarelist) != n | len(piclist) != n | len(votelist) != n:
            raise Exception("Candidate lists do not match.")

        # Get names and return
        ret_list = []
        for c in namelist:
            k = (c.text, int(c.attrib["fill"]))  # type: (str,int)
            ret_list.append(k)
        return ret_list

    def get_candidate_regions(self, name):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Get candidate's color
        squarelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_SQ"])[0]
        ck_color = None
        for sq in squarelist:
            if sq.attrib["id"].lower() == name.lower():
                ck_color = int(sq.attrib["fill"].strip("#"), 16)
                break

        # Check region list, append IDENTIFIERS only (not Elements)
        cand_regions = []
        for region in self.get_region_list():
            if self.get_region_color(region) == ck_color:
                cand_regions.append(region)

        # Return list
        return cand_regions

    def set_title(self, title=None, color=None):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Set values
        element = MapperUS._parse_tag(root, "title")[0]
        element.text = str(title)
        if color is not None:
            element.attrib["fill"] = "#{:06x}".format(int(color, 16) if isinstance(color, str) else color)

        # Write to file and return
        tree.write(self.map)
        return

    def set_candidate_votes(self, name, votes, color=None):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Check list and set values
        votelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_EV"])[0]
        for element in votelist:
            if element.attrib["id"].lower() == str(name.lower() + "-votes"):
                element.text = str(votes)
                if color is not None:
                    element.attrib["fill"] = "#{:06x}".format(int(color, 16) if isinstance(color, str) else color)

        # Write to file and return
        tree.write(self.map)
        return

    def add_candidate(self, name, color, picture=None):
        # Check picture. If none, go to default.
        if picture is None:
            picture = self._cfg["candpic_def"]
        else:
            pass  # Do nothing. Relative paths work at this time.

        # ----- NOTES: -----
        # If number of candidates is 5 or less, stay with 'position 1' (near Florida, default selection)
        # If number of candidates exceeds 5, switch to 'position 2' (far right side of map)
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Get candidate-names list, candidate-squares list
        namelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_NM"])[0]
        squarelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_SQ"])[0]
        piclist = MapperUS._parse_tag(root, self._cfg["ID_CAND_PX"])[0]
        votelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_EV"])[0]

        # Check list to see if name is already added
        for c in namelist:
            if c.attrib["id"].lower() == str(name.lower()):
                raise ValueError("Name already exists in candidate list.")

        # *** Check current amount of candidates ***
        swccase = self._cfg["SWC_CANDS"]
        maxcase = self._cfg["MAX_CANDS"]
        n = len(namelist)
        if len(squarelist) != n | len(piclist) != n | len(votelist) != n:  # Check all lists before proceeding
            raise Exception("Candidate lists do not match.")

        # Too many candidates -------------------------------------------------- #
        if n >= maxcase:
            raise ValueError("Maximum number of candidates ({0}) reached in list.".format(maxcase))
        # Before switch case -------------------------------------------------- #
        elif (n < swccase) & (n >= 0):
            # Get coordinates
            ynplus = int(self._cfg["candname_yadd"])
            ysplus = int(self._cfg["candsq_yadd"])
            xpplus = int(self._cfg["candpic_w"]) + int(self._cfg["candpic_dx"])

            # Add candidate-name subelement to svg xml
            nameattributes = {
                "id": str(name).lower(),  # use lower case only in id field (text field remains unchanged)
                "x": "0",
                "y": str(ynplus * n),
                "font-size": "24"
            }
            newname = ET.SubElement(namelist, "text", attrib=nameattributes)
            newname.text = str(name)

            # Add candidate-square subelement to svg xml
            sqattributes = {
                "id": str(name).lower(),
                "x": "0",
                "y": str(ysplus * n),
                "height": str(self._cfg["candsq_h"]),
                "width": str(self._cfg["candsq_w"]),
                "fill": "#{:06x}".format(int(color, 16) if isinstance(color, str) else color),
                "stroke": "#{c}".format(c=self._cfg["candsq_c"]),
                "stroke-width": str(self._cfg["candsq_sw"])
            }
            ET.SubElement(squarelist, "rect", attrib=sqattributes)

            # Add candidate to picture list (picture + border)
            picattributes = {
                "id": str(name).lower() + "-pic",
                "x": str(xpplus * n),
                "y": "0",
                "height": str(self._cfg["candpic_h"]),
                "width": str(self._cfg["candpic_w"]),
                "{ns}href".format(ns="{" + self._cfg["XLINK"] + "}"): picture
            }
            borderattributes = {
                "id": str(name).lower() + "-border",
                "x": str(xpplus * n),
                "y": "0",
                "height": str(self._cfg["candpic_h"]),
                "width": str(self._cfg["candpic_w"]),
                "fill": "none",
                "stroke": "#{:06x}".format(int(color, 16) if isinstance(color, str) else color),
                "stroke-width": str(self._cfg["candpic_sw"])
            }
            ET.SubElement(piclist, "image", attrib=picattributes)
            ET.SubElement(piclist, "rect", attrib=borderattributes)

            # Add candidate to vote list
            voteattributes = {
                "id": str(name).lower() + "-votes",
                "x": str(xpplus * n),
                "y": "0",
                "fill": "#{:06x}".format(int(color, 16) if isinstance(color, str) else color),
                "stroke": "#{c}".format(c=self._cfg["candev_c"]),
                "stroke-width": str(self._cfg["candev_sw"]),
                "text-anchor": self._cfg["candev_anch"]
            }
            v = ET.SubElement(votelist, "text", attrib=voteattributes)
            v.text = "0"  # Start with zero votes

            # Change picture list and vote list x-position translations based on new candidate list
            n += 1
            pw = int(self._cfg["candpic_w"])
            pdx = int(self._cfg["candpic_dx"])
            lw = pw*n + pdx*(n-1)
            t1 = int((self.mapwidth / 2) - (lw / 2))  # picture list x-translate
            t2 = int(t1 + pw/2)  # vote list x-translate

            piclist.attrib["transform"] = ElectionUS._update_translation(piclist.attrib["transform"], x=t1)
            votelist.attrib["transform"] = ElectionUS._update_translation(votelist.attrib["transform"], x=t2)

            # Write to file and exit
            tree.write(self.map)
            return
        # At or above switch case -------------------------------------------------- #
        elif n >= swccase:
            raise NotImplementedError(
                "Cannot add more than {0} candidates at this time.".format(swccase)
            )
            # TODO : Implement routine for additional candidates above switch case
        # Should not reach this -------------------------------------------------- #
        else:
            raise Exception("Invalid candidate lists.")

    def set_candidate_color(self, name, color):
        tree = ET.parse(self.map)
        root = tree.getroot()

        # Prepare color string
        ckstr = "#{:06x}".format(int(color, 16) if isinstance(color, str) else color)

        # Get lists that have associated colors
        squarelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_SQ"])[0]
        piclist = MapperUS._parse_tag(root, self._cfg["ID_CAND_PX"])[0]
        votelist = MapperUS._parse_tag(root, self._cfg["ID_CAND_EV"])[0]
        barlist = MapperUS._parse_tag(root, self._cfg["ID_BAR"])[0]

        # Check lists and update lists
        for element in squarelist:
            if element.attrib["id"].lower() == name.lower():
                element.attrib["fill"] = ckstr
                break
        for element in piclist:
            if element.attrib["id"].lower() == str(name.lower() + "-border"):
                element.attrib["stroke"] = ckstr
                break
        for element in votelist:
            if element.attrib["id"].lower() == str(name.lower() + "-votes"):
                element.attrib["fill"] = ckstr
                break
        for element in barlist:
            if element.attrib["id"].lower() == str(name.lower() + "-bar"):
                element.attrib["fill"] = ckstr
                break

        # Write to file and return
        tree.write(self.map)
        return

    def set_bar(self, data):
        """
        Update vote bar with <data> given. See below for exact data format.\n

        data = {
            0: ["<name1>", <color1>, <votes1>],\n
            1: ["<name2>", <color2>, <votes2>],\n
            ...\n
            N: ["<nameN", <colorN>, <votesN>],\n
            "total": <total>,\n
            "tri": <colorT>
        }\n
        <total> : (int) total number of votes (100% of bar)\n
        <nameK> : (str) Name of candidate\n
        <colorK>: (int) color of candidate in RGB hex (0x??????)\n
        <votesK>: (int) number of votes received by candidate\n
        <colorT>: (int | -1 | None) color of triangles in RGB hex (0x??????).
            \t-1 = Reset to default.\n
            \tIf none, leave color unchanged.

        :param data: User values needed to set up the election 'bar'.
        :type data: dict

        :return:
        :rtype: None
        """
        # TODO : Maybe do multiple bars?
        # Verify data ------------------------- #
        try:
            for n in range(0, len(data)-2):
                    str(data[n][0])  # <nameN>
                    int(data[n][1])  # <colorN>
                    int(data[n][2])  # <votesN>
            int(data["total"])  # <total>
            if data["tri"] is not None:
                int(data["tri"])  # <colorT>
        except ValueError as v:
            raise ValueError("Invalid data given. MSG: {0}".format(v))

        # Verify total votes >= votes1 + votes2 + ... + votesN ------------------------- #
        summation = 0
        for n in range(0, len(data)-2):
            summation += int(data[n][2])
        if summation > data["total"]:
            raise ValueError("All candidate votes are greater than total votes given in <data>.")

        # TODO : Verify integers as colors ------------------------- #

        # Purge all non-default bar elements and reset default elements ------------------------- #
        tree = ET.parse(self.map)
        root = tree.getroot()
        barlist = MapperUS._parse_tag(root, self._cfg["ID_BAR"])[0]

        for element in barlist.findall(".//"):  # Prevent 'skipping' over iteration
            # Purge non-default elements
            if element.attrib["id"] not in ["blank-bar", "triup", "tridown"]:
                barlist.remove(element)
            # Reset triangles if needed
            if (element.attrib["id"] in ["triup", "tridown"]) & (data["tri"] is not None):
                if int(data["tri"]) < 0:
                    element.attrib["fill"] = "#{c}".format(c=self._cfg["bar_c"])
        tree.write(self.map)

        # Create candidate list ------------------------- #
        cand_list = []
        for n in range(0, len(data)-2):
            cand_list.append(
                # <nameN>, <colorN>, <votesN>
                _CandidateInfo(name=data[n][0], color=data[n][1], votes=data[n][2])
            )
        if len(cand_list) > 2:  # Do not sort if list is 2 or less.
            cand_list = ElectionUS._sort_by_votes(ls=cand_list, reverse=True)

        # Calculate variables ------------------------- #
        total = data["total"]
        rect_tot_h = int(self._cfg["bar_h"])  # Height for all bars
        rect_tot_w = int(self._cfg["bar_w"])  # Width of total bar
        for candidate in cand_list:
            votesN = candidate.votes
            if votesN < 0:
                votesN = 0
            percent = votesN / total
            candidate.bar = int(rect_tot_w * percent)

        # Add new elements ------------------------- #
        # Add candidate colored bars
        tree = ET.parse(self.map)
        root = tree.getroot()
        barlist = MapperUS._parse_tag(root, self._cfg["ID_BAR"])[0]

        cur_x = 0  # current x-position to add new bar
        for candidate in cand_list:
            # Add new colored bar element
            ET.SubElement(
                barlist,
                "rect",
                attrib={
                    "id": candidate.name.lower() + "-bar",
                    "height": str(rect_tot_h),
                    "width": str(candidate.bar),
                    "fill": "#{:06x}".format(candidate.color),
                    "x": str(cur_x),
                    "y": "0",
                }
            )
            # Add new number element on top of bar element
            x_num_pos = int(cur_x + candidate.bar/2)  # Put center of rectangle
            y_num_pos = int(int(rect_tot_h / 2) + int(0.8 * self._cfg["bar_tsize"]) / 2)  # 0.8 = shift text up slightly
            e = ET.SubElement(
                barlist,
                "text",
                attrib={
                    "id": candidate.name.lower() + "-numb",
                    "x": str(x_num_pos),
                    "y": str(y_num_pos),
                    "font-family": self._cfg["bar_tfont"],
                    "font-size": str(self._cfg["bar_tsize"]),
                    "text-anchor": self._cfg["bar_tanch"],
                    "font-weight": self._cfg["bar_tlbs"],
                    "fill": "#{c}".format(c=self._cfg["bar_tc"])
                }
            )
            e.text = str(candidate.votes)
            cur_x += candidate.bar
        # TODO : Maybe add names too?

        # If triangle color should be changed...
        if (data["tri"] is not None) and (int(data["tri"]) >= 0):
            triangles = barlist.findall(".//{ns}polygon".format(ns="{" + self._cfg["NAMESPACE"] + "}"))
            for ele in triangles:
                ele.attrib["fill"] = "#{:06x}".format(data["tri"])

        # Write and return ------------------------- #
        tree.write(self.map)
        return

    @staticmethod
    def _sort_by_votes(ls, reverse=False):
        """
        Sorts a list of candidates w/ infos by votes.

        :param ls: unsorted list of candidates
        :type ls: list[_CandidateInfo]

        :param reverse: False = smallest to largest votes, True = vice versa
        :type reverse: bool

        :return: sorted list of candidates
        :rtype: list[_CandidateInfo]
        """
        # Selection sort
        n = len(ls)
        # a[j ... n-1]
        for j in range(0, n-1):
            iMin = j
            for i in range(j+1, n):
                if int(ls[i]) < int(ls[iMin]):
                    iMin = i
            if iMin != j:
                # swap(a,b)
                tmp = ls[j]
                ls[j] = ls[iMin]
                ls[iMin] = tmp

        # Return list
        if reverse:
            return ls[::-1]
        else:
            return ls


class _CandidateInfo:
    """
    Private utility class for ElectionUS class.
    """
    name = ""  # Name of candidate
    color = 0  # Color of candidate
    votes = 0  # Votes of candidate
    bar = 0    # Length of bar of candidate (set later)

    def __init__(self, name, color, votes):
        self.name = name  # type: str
        self.color = color  # type: int
        self.votes = votes  # type: int
        self.bar = 0  # type: int

    def __int__(self):
        return self.votes

# END OF FILE ////////////////////////////////////////////////////////////
