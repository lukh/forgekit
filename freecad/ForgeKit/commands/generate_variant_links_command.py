# SPDX-License-Identifier: LGPL-2.1-or-later

"""Generate Variant Links Command."""

from typing import ClassVar

import  itertools
from PySide import QtGui

import FreeCAD as App
translate = App.Qt.translate

from ..resources import Resources


class GenerateVariantLinksCommand:
    """Generate Variants Links from a list of property names (that should be created via a configuration table)."""

    # Good practice (optional): set a constant for your command name, it is used in several places.
    Name: ClassVar[str] = "ForgeKit_GenerateVariantLinksCommand"

    def __init__(self) -> None:
        pass

    def GetResources(self) -> dict[str, str]:
        # Returns a dictionary that defines how the command appears in the UI.
        # - Pixmap: path to the icon file (relative to FreeCAD's icon search paths or absolute path)
        # - MenuText: text shown in menus (use translate for translation support)
        # - ToolTip: text shown when hovering over the button/menu item
        # - Accel: optional keyboard shortcut (e.g., "Ctrl+A")
        return {
            "Pixmap": Resources.icon(
                "ForgeKit.svg"
            ),
            "MenuText": translate(
                "ForgeKit",
                "Generate Variants Links",
            ),
            "ToolTip": translate(
                "ForgeKit",
                "Generate Variants Links from a list of property names (that should be created via a configuration table).",
            ),
        }

    def Activated(self) -> None:
        if App.GuiUp:
            sel = App.Gui.Selection.getSelection()

            obj = sel[0]

            App.Console.PrintMessage('Object Name: ' + obj.Label)

            (text, status) = QtGui.QInputDialog.getText(None, 'Properties', 'List the properties that will be scanned, separated by a comma')

            if status:
                props = [t.strip() for t in text.split(',')]
                
                comb = []

                for prop in props:
                    comb.append(obj.getEnumerationsOfProperty(prop))
                    
                configs = list(itertools.product(*comb))

                for idx, c in enumerate(configs):
                    label = obj.Label + '_' + '_'.join(c)
                    
                    l = App.ActiveDocument.addObject('App::Link', label)
                    l.LinkedObject = obj
                    l.LinkCopyOnChange = "Enabled"
                    l.Placement.Base.x += 20*idx
                    l.recompute()

                    for i, prop in enumerate(props):
                        setattr(l, prop, c[i])
                        
                    if hasattr(obj, 'PlumeIPN'):
                        #l.setEditorMode('PlumeIPN', 0)
                        exp = f"<<{obj.PlumeIPN}_>> + {'+<<_>>+'.join([''+p+'.String' for p in props])}"
                        l.setExpression('PlumeIPN', exp)
                        
                        #l.setEditorMode('PlumeIPN', 1)

    def IsActive(self) -> bool:
        return True

    @classmethod
    def Install(cls) -> None:
        if App.GuiUp:
            App.Gui.addCommand(cls.Name, cls())
