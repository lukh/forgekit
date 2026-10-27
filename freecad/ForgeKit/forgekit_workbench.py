# SPDX-License-Identifier: LGPL-2.1-or-later

"""Example FreeCAD Workbench."""

import FreeCAD as App
import FreeCADGui as Gui

translate = App.Qt.translate

from .resources import Resources
from .commands import CreateDrawingGroupCommand, CreateTDPageFromSpreadsheetCommand, ExportTechDrawCommand, GenerateVariantLinksCommand, CreateOptionalVariantCommand, RenameAssemblyJointsCommand



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
        commands = [CreateDrawingGroupCommand.Name, CreateTDPageFromSpreadsheetCommand.Name, ExportTechDrawCommand.Name, GenerateVariantLinksCommand.Name, CreateOptionalVariantCommand.Name, RenameAssemblyJointsCommand.Name]
        
        self.appendToolbar("ForgeKit", commands)
        self.appendMenu("ForgeKit", commands)

    def Activated(self) -> None:
        pass

    def Deactivated(self) -> None:
        pass

    def ContextMenu(self, recipient: str) -> None:
        # Adding context menus when the Workbench is active (example)
        # self.appendContextMenu("", [ExampleCommand.Name])
        pass

    @classmethod
    def Install(cls) -> None:
        Gui.addWorkbench(cls)
