# SPDX-License-Identifier: LGPL-2.1-or-later

"""Command to shortcut the creation of a TD Page from a SpreadSheet."""

from typing import ClassVar

import FreeCAD as App
translate = App.Qt.translate

from ..resources import Resources


class CreateTDPageFromSpreadsheetCommand:
    """Create a page from a spreadsheet, setting the full range of the spreadsheet."""

    Name: ClassVar[str] = "ForgeKit_CreateTDPageFromSpreadsheetCommand"

    def __init__(self) -> None:
        pass

    def GetResources(self) -> dict[str, str]:
        return {
            "Pixmap": Resources.icon(
                "forgekit_create_td_from_spreadsheet.svg"
            ),
            "MenuText": translate(
                "ForgeKit",
                "Create page from spreadsheet",
            ),
            "ToolTip": translate(
                "ForgeKit",
                "Create a page from a spreadsheet, setting the full range of the spreadsheet.",
            ),
        }

    def Activated(self) -> None:
        if App.GuiUp:
            doc = App.ActiveDocument

            sel = App.Gui.Selection.getSelection()
            spreadsheets = [o for o in sel if o.TypeId == "Spreadsheet::Sheet"]
            pages = [o for o in sel if o.TypeId == "TechDraw::DrawPage"]

            if len(pages) == 0:
                page = doc.addObject("TechDraw::DrawPage", "Page")
                page.KeepUpdated = True

                template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")

                params = App.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Files")
                default_template_path = params.GetString("TemplateFile", "")
                template.Template = default_template_path

                page.Template = template

                pages = [page]

            for p in pages:
                for s in spreadsheets:
                    view = doc.addObject("TechDraw::DrawViewSpreadsheet", "SheetView")
                    view.Source = s
                    
                    cs, ce = s.getNonEmptyRange()
                    view.CellStart = cs
                    view.CellEnd = ce
                
                    p.addView(view)



    def IsActive(self) -> bool:
        if App.GuiUp:
            sel = App.Gui.Selection.getSelection()
            if len(sel) > 0:
                return all([o.TypeId in ["Spreadsheet::Sheet", "TechDraw::DrawPage"] for o in sel])

        return False

    @classmethod
    def Install(cls) -> None:
        # Optional utility method to register the command
        if App.GuiUp:
            App.Gui.addCommand(cls.Name, cls())
