# SPDX-License-Identifier: LGPL-2.1-or-later

"""
Optional Variant Object. Allows to add, or not, a Link to a StdPart (or Assembly)
"""

from __future__ import annotations

import FreeCAD as App

class OptionalVariant:
    """
    Optional Variant Link
    """

    def __init__(self, obj: App.DocumentObject, src_obj: App.DocumentObject) -> None:
        obj.addProperty("App::PropertyBool", "Enable", "OptionalVariant", "").Enable = True
        obj.addProperty("App::PropertyLink", "Source", "OptionalVariant", "").Source = src_obj

        src_obj.ViewObject.Visibility = False

        obj.Proxy = self


    def onChanged(self, obj: App.DocumentObject, prop: str) -> None:
        pass

    def execute(self, obj: App.DocumentObject) -> None:
        if obj.Enable:
            obj.Shape = obj.Source.Shape
            obj.Placement = obj.Source.Placement

        else:
            obj.Shape = Part.Shape()

    @classmethod
    def create(cls, src_obj : App.DocumentObject, name: str | None = None, doc: App.Document | None = None) -> OptionalVariant:
        # Check valid document
        if not (doc := doc or App.ActiveDocument):
            raise ValueError("A FreeCAD document is required")

        name = name or f"{src_obj.Label}_Vt"

        obj = App.ActiveDocument.addObject("Part::FeaturePython", name)
        parent = src_obj.getParent()
        parent_group = src_obj.getParentGroup()
        if parent_group is not None:
            parent_group.addObject(obj)
            parent_group.removeObject(src_obj)
        elif parent is not None:
            parent.addObject(obj)


        # Bind the Python Proxy
        proxy = cls(obj, src_obj)

        # Manage Gui (ViewProvider) if available
        if App.GuiUp and hasattr(obj, "ViewObject"):
            from .optional_variant_vp import OptionalVariantViewProvider
            OptionalVariantViewProvider(obj.ViewObject)

        obj.recompute()
        return proxy