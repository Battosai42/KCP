
import pcbnew
import os
import math
from .json_import.parse_json import *
import numpy as np
#from .kcp_utils import *
import pathlib
import time


class KCPAction(pcbnew.ActionPlugin):
    """
    A script for automated placement of key-switches, leds and diodes from a keyboard-layout-editor.com
    layout (from JSON export)
    """

    def defaults(self):
        """
        Default settings
        """
        self.name = "KCP - Keyboard Component Placement"
        self.category = "PCBNEW plugin"
        self.description = "KiCad Action plugin to automatically place keyboard switches, diodes and leds according to" \
                           "a keyboard layout generated from http://www.keyboard-layout-editor.com/#/"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'docs/logo.png')
        self.show_toolbar_button = True

    def Run(self):
        """
        The entry function of the plugin that is executed on user action
        """

        config_file = os.path.join(os.path.dirname(__file__), 'example/ergochoc.json')

        self.pcb = pcbnew.GetBoard()
        test = load(config_file)
        keys = test.get_key_locations()
        key_spacing = 19.05
        x_bezel = 5
        y_bezel = 5

        #modules = pcb.board.GetModules()

        for k in range(len(keys)):
            x, y, rotation, name, profile = keys[k]
            x = key_spacing * x + x_bezel
            y = key_spacing * y - y_bezel
            row, col = str(profile).replace(".", ",").split(',')
            print(row, col)
            id = int(row)*100 + int(col)

            try:
                # place switch
                self.place_component(ref="SW{}".format(id), x=x, y=-y, angle=-rotation)

                # place diode
                xd, yd = self.rotate(origin=(0, 0), point=(0, -8.5), angle=-rotation)
                self.place_component(ref="D{}".format(id), x=x+xd, y=-y-yd, angle=-rotation)

                # place led
                xd, yd = self.rotate(origin=(0, 0), point=(0, 5), angle=-rotation)
                self.place_component(ref="LED{}".format(id), x=x + xd, y=-y - yd, angle=-rotation)
            except Exception:
                pass

    def place_component(self, ref: str, x: float, y: float, angle: float) -> None:
        """
        find and place a footprint to a given location and rotate it.

        :param ref: reference of the footprint
        :param x: x-coordinate
        :param y: y-coordinate
        :param angle: rotation angle in degrees
        """
        key = self.pcb.FindFootprintByReference(ref)
        key.SetPosition(pcbnew.wxPointMM(x, y))
        key.SetOrientationDegrees(angle)
        pcbnew.Refresh()

    def rotate(self, origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point
        angle = angle/180*np.pi

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

        # Load the board
        #pcb = pcbnew.LoadBoard("take2.kicad_pcb")

        # Find the component
        #c = pcb.FindModuleByReference("D1")

        # Place it somewhere
        #c.SetPosition(pcbnew.wxPointMM(100, 100))

        # Rotate it (angle in 1/10 degree)
        #c.SetOrientation(45 * 10)

        # and save the file under a different name
        #pcb.Save("take2_mod.kicad_pcb")

#KCPAction().register()