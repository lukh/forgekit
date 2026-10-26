# SPDX-License-Identifier: LGPL-2.1-or-later

"""Example FreeCAD Workbench."""

import FreeCAD as App
import FreeCADGui as Gui

translate = App.Qt.translate

from .resources import Resources
from .commands import ExampleCommand

class ForgeKitWorkbench(Gui.Workbench):

    MenuText: str = translate(
            "ForgeKit",
            "Example Workbench",
        )

    ToolTip: str = translate(
            "ForgeKit",
            "Example Workbench tooltip",
        )

    Icon: str = Resources.icon("ForgeKit-wb.svg")


    def Initialize(self) -> None:
        App.Console.PrintMessage("Example Workbench initialized\n")
        # Adding menus and toolbars when the Workbench is active (example)
        commands = [ExampleCommand.Name]
        self.appendToolbar("ForgeKit", commands)
        self.appendMenu("ForgeKit", commands)

    def Activated(self) -> None:
        App.Console.PrintMessage("Example Workbench activated\n")

    def Deactivated(self) -> None:
        App.Console.PrintMessage("Example Workbench deactivated\n")

    def ContextMenu(self, recipient: str) -> None:
        App.Console.PrintMessage("Example Workbench context menu\n")
        # Adding context menus when the Workbench is active (example)
        self.appendContextMenu("", [ExampleCommand.Name])

    @classmethod
    def Install(cls) -> None:
        Gui.addWorkbench(cls)
