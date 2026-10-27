# SPDX-License-Identifier: LGPL-2.1-or-later

"""Rename assembly joints"""

from typing import ClassVar

import FreeCAD as App
translate = App.Qt.translate

from ..resources import Resources


class RenameAssemblyJointsCommand:
    """Rename assembly joints"""

    Name: ClassVar[str] = "ForgeKit_RenameAssemblyJointsCommand"

    def __init__(self) -> None:
        pass

    def GetResources(self) -> dict[str, str]:
        return {
            "Pixmap": Resources.icon(
                "ForgeKit.svg"
            ),
            "MenuText": translate(
                "ForgeKit",
                "Example Command",
            ),
            "ToolTip": translate(
                "ForgeKit",
                "Runs the example command",
            ),
        }

    def Activated(self) -> None:
        if App.GuiUp:
            sel = App.Gui.Selection.getSelection()
            obj = sel[0]

            for j in obj.Joints:
                ref1_name = j.Reference1[0].Label
                ref2_name = j.Reference2[0].Label
                joint_type = j.JointType
                
                label = f"{joint_type} ({ref1_name}, {ref2_name})"
                print(label)
                
                j.Label = label

    def IsActive(self) -> bool:
        if App.GuiUp:
            sel = App.Gui.Selection.getSelection()
            if len(sel) == 1:
                obj = sel[0]
                return obj.TypeId == "Assembly::AssemblyObject"
        return False

    @classmethod
    def Install(cls) -> None:
        if App.GuiUp:
            App.Gui.addCommand(cls.Name, cls())
