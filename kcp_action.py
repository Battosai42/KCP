import pcbnew

class KCPAction(pcbnew.ActionPlugin)
    def defaults(self):
        self.name = "KCP - Keyboard Component Placement"
        self.category = "PCBNEW plugin"
        self.description "KiCad Action plugin to automatically place keyboard switches, diodes and leds according to a keyboard layout generated from http://www.keyboard-layout-editor.com/#/"

    def Run(self):
        # The entry function of the plugin that is executed on user action
        print("Hello World")