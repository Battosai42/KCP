
import pcbnew
import os
from .json_import.parse_json import *
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

        pcb = pcbnew.GetBoard()
        test = load(config_file)
        keys = test.get_key_locations()
        key_spacing = 19.05
        x_bezel = 5
        y_bezel = 5

        #modules = pcb.board.GetModules()

        for k in range(len(keys)):
            x, y, rotation, name = keys[k]
            x = key_spacing * x + x_bezel
            y = key_spacing * y - y_bezel

            try:
                key = pcb.FindFootprintByReference("SW{}".format(k+1))
                key.SetPosition(pcbnew.wxPointMM(x, -y))
                key.SetOrientationDegrees(-rotation)
                pcbnew.Refresh()
                #time.sleep(0.5)
            except Exception:
                pass


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