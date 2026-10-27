# SPDX-License-Identifier: LGPL-2.1-or-later

"""Export all drawings in the file"""

from typing import ClassVar
import re
import os
import tempfile

import pypdf # TODO

from PySide import QtGui

import FreeCAD as App
import TechDrawGui

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
        def traverse_for_drawings(objs, rel_path=[]):
            for o in objs:
                if o.TypeId == "TechDraw::DrawPage" or (o.TypeId == "App::DocumentObjectGroupPython" and hasattr(o, "MainSourceItem")):
                    yield (rel_path, sanitize(o.Label), o)
                    
                elif o.TypeId == "App::DocumentObjectGroup":
                    yield from traverse_for_drawings(o.Group, rel_path=rel_path + [sanitize(o.Label)])

        doc = App.ActiveDocument

        if App.GuiUp:
            # Output directory
            if doc.FileName:
                bdir = os.path.dirname(doc.FileName)
            else:
                bdir = FreeCAD.getUserAppDataDir()

            out_dir = QtGui.QFileDialog.getExistingDirectory(None, "Export folder", bdir)
            

            root_objs = doc.RootObjectsIgnoreLinks

            sanitize = lambda x : re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", x)
                        
            for rp, filename, obj in traverse_for_drawings(root_objs):
                directory_path = os.path.join(out_dir, *rp)
                os.makedirs(directory_path, exist_ok=True)

                pdf_path = os.path.join(directory_path, filename+".pdf")

                if obj.TypeId == "TechDraw::DrawPage":
                    TechDrawGui.exportPageAsPdf(obj, pdf_path)
                    
                elif obj.TypeId == "App::DocumentObjectGroupPython" and hasattr(obj, "MainSourceItem"):
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        pages = [p for p in obj.Group if p.TypeId == "TechDraw::DrawPage"]
                        merger = pypdf.PdfWriter()

                        for idx, p in enumerate(pages):
                            pdf = os.path.join(tmpdirname, f'P{idx}.pdf')
                            TechDrawGui.exportPageAsPdf(p, pdf)

                            merger.append(pdf)

                        merger.write(pdf_path)


    def IsActive(self) -> bool:
        return App.ActiveDocument is not None

    @classmethod
    def Install(cls) -> None:
        if App.GuiUp:
            App.Gui.addCommand(cls.Name, cls())
