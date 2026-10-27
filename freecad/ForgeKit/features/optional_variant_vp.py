# SPDX-License-Identifier: LGPL-2.1-or-later

"""
Basic ViewProvider example.

see: https://wiki.freecad.org/Scripted_objects
"""

from __future__ import annotations
from ..resources import Resources

import FreeCADGui as Gui


class OptionalVariantViewProvider:
    """
    Basic ViewProvider with custom Icon.
    """

    def __init__(self, obj: Gui.ViewProviderDocumentObject) -> None:
        obj.Proxy = self

    def attach(self, vobj):
        self.Object = vobj.Object

    def getIcon(self) -> str:
        return Resources.icon("forgekit_optionalvariant.svg")

    def claimChildren(self):
        return [self.Object.Source]