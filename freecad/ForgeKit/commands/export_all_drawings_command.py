# SPDX-License-Identifier: LGPL-2.1-or-later

"""Export all drawings in the file"""

from typing import ClassVar

import FreeCAD as App
translate = App.Qt.translate

from ..resources import Resources


class ExportTechDrawCommand:
    """Export all drawings in the file."""

    Name: ClassVar[str] = "ForgeKit_ExportTechDrawCommand"

    def __init__(self) -> None:
        pass

    def GetResources(self) -> dict[str, str]:
        return {
            "Pixmap": Resources.icon(
                "forgekit_export_all_drawings.svg"
            ),
            "MenuText": translate(
                "ForgeKit",
                "Export all drawings",
            ),
            "ToolTip": translate(
                "ForgeKit",
                "Exports all pages and drawings",
            ),
        }

    def Activated(self) -> None:
        pass

    def IsActive(self) -> bool:
        return True

    @classmethod
    def Install(cls) -> None:
        if App.GuiUp:
            App.Gui.addCommand(cls.Name, cls())
