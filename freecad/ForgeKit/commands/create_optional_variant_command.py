# SPDX-License-Identifier: LGPL-2.1-or-later

"""Example FreeCAD command demonstrating the command structure."""

from typing import ClassVar

import FreeCAD as App
translate = App.Qt.translate

from ..resources import Resources


class CreateOptionalVariantCommand:
    """Create an Optional Variant."""

    # Good practice (optional): set a constant for your command name, it is used in several places.
    Name: ClassVar[str] = "ForgeKit_CreateOptionalVariantCommand"

    def __init__(self) -> None:
        pass

    def GetResources(self) -> dict[str, str]:
        return {
            "Pixmap": Resources.icon(
                "forgekit_optionalvariant.svg"
            ),
            "MenuText": translate(
                "ForgeKit",
                "Create Optional Variants",
            ),
            "ToolTip": translate(
                "ForgeKit",
                "Create Optional Variants",
            ),
        }

    def Activated(self) -> None:
        if App.GuiUp:
            from ..features import OptionalVariant
            for src_obj in App.Gui.Selection.getSelection():
                OptionalVariant.create(src_obj)

    def IsActive(self) -> bool:
        return bool(App.ActiveDocument) and bool(Gui.Selection.getSelection())

    @classmethod
    def Install(cls) -> None:
        if App.GuiUp:
            App.Gui.addCommand(cls.Name, cls())
