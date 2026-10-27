# SPDX-License-Identifier: LGPL-2.1-or-later

"""Create a DrawingGroup"""

from typing import ClassVar

from PySide import QtGui

import FreeCAD as App
translate = App.Qt.translate

from ..resources import Resources


class CreateDrawingGroupCommand:
    """Create a DrawingGroup."""

    Name: ClassVar[str] = "ForgeKit_CreateDrawingGroupCommand"

    def __init__(self) -> None:
        pass

    def GetResources(self) -> dict[str, str]:
        return {
            "Pixmap": Resources.icon(
                "forgekit_drawinggroup.svg"
            ),
            "MenuText": translate(
                "ForgeKit",
                "Create a DrawingGroup",
            ),
            "ToolTip": translate(
                "ForgeKit",
                "Create a DrawingGroup, that hold several Pages",
            ),
        }

    def Activated(self) -> None:
        if App.GuiUp:
            from ..features import DrawingGroup
            doc = App.ActiveDocument or App.newDocument()

            sel = App.Gui.Selection.getSelection()
            
            src_item = sel[0] if sel else None
            name = "DrawingGroup"
            if src_item:
                name += "_" + src_item.Label

            # TODO should be a task ?
            (title, status) = QtGui.QInputDialog.getText(None, 'Title', 'Title for the Group Pages.')

            if status:
                DrawingGroup.create(name, doc, title=title, src_item=src_item)

    def IsActive(self) -> bool:
        return True

    @classmethod
    def Install(cls) -> None:
        # Optional utility method to register the command
        if App.GuiUp:
            App.Gui.addCommand(cls.Name, cls())
