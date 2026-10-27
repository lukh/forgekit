
import datetime

class DrawingGroup:
    def __init__(self, obj: App.DocumentObject, title: str = "", src_item: App.DocumentObject=None) -> None:
        doc = App.ActiveDocument

        obj.addProperty("App::PropertyBool", "IncludeParentTitles", "Drawing", "").IncludeParentTitles = False
        obj.addProperty("App::PropertyString", "Title", "Drawing", "").Title = title
        obj.addProperty("App::PropertyString", "AuthorName", "Drawing", "").AuthorName = doc.CreatedBy
        obj.addProperty("App::PropertyString", "SupervisorName", "Drawing", "").SupervisorName = doc.CreatedBy
        obj.addProperty("App::PropertyString", "CompanyName", "Drawing", "").CompanyName = doc.Company
        obj.addProperty("App::PropertyString", "Copyright", "Drawing", "").Copyright = doc.License
        obj.addProperty("App::PropertyString", "CreationDate", "Drawing", "").CreationDate = datetime.datetime.strftime(datetime.datetime.today(), "%d/%m/%y")
        obj.addProperty("App::PropertyString", "CheckDate", "Drawing", "").CheckDate = ""
        obj.addProperty("App::PropertyString", "Version", "Drawing", "").Version = ""

        obj.addProperty("App::PropertyLink", "MainSourceItem", "Drawing", "Main source item for version/revision").MainSourceItem = src_item

        toc = doc.addObject("Spreadsheet::Sheet", f"{obj.Label}_TOC")
        obj.addProperty("App::PropertyLink", "ToC", "Drawing", "Table of Content").ToC = toc
        obj.addObject(toc)

        obj.Proxy = self

    def execute(self, obj: App.DocumentObject) -> None:
        toc = obj.ToC
        toc.clearAll()
        toc.set('A1', "Sheet Number")
        toc.set('B1', "Subtitle")


        pages = [p for p in obj.Group if p.TypeId == "TechDraw::DrawPage"]
        page_count = len(pages)


        title = obj.Title
        if obj.IncludeParentTitles:
            def get_parents(o):
                if o.getParent():
                    yield o.getParent()

                    yield from get_parents(o.getParent())

            for p in get_parents(obj):
                title = getattr(p, "Title", p.Label) + " / " + title


        version = ""
        if hasattr(obj.MainSourceItem, obj.Version):
            version = getattr(obj.MainSourceItem, obj.Version)
        elif hasattr(obj.MainSourceItem, "PlVersion") and hasattr(obj.MainSourceItem, "PlRevision"):
            version = f"{obj.MainSourceItem.PlVersion}.{obj.MainSourceItem.PlRevision}"
        else:
            version = obj.Version

        for idx, page in enumerate(pages):
            template = page.Template

            fields = template.EditableTexts.copy()

            toc.set(f'A{idx+2}', f'{idx + 1}')
            toc.set(f'B{idx+2}', fields.get('SUBTITLE'))

            new_fields = fields.copy()
            new_fields.update({
                'COPYRIGHT': obj.Copyright,
                'TITLE': title,
                'VERSION': version,
                'AUTHOR_NAME': obj.AuthorName,
                'SUPERVISOR_NAME': obj.SupervisorName,
                'COMPANY_NAME': obj.CompanyName,
                'CREATION_DATE': obj.CreationDate,
                'CHECK_DATE': obj.CheckDate,
                'SHEET': f'{idx + 1} / {page_count}',
            })

            if new_fields != fields:
                template.EditableTexts = new_fields

        # TODO recomputing stuff is documented as a bad idea in the wiki,
        # but  it does works so...
        toc.recompute()
        toc.purgeTouched()

    @classmethod
    def create(cls, name: str | None = None, doc: App.Document | None = None, title: str = "", src_item: App.DocumentObject=None) -> DrawingGroup:
        """Optional utility method to create instances of this feature"""

        # Check valid document
        if not (doc := doc or App.ActiveDocument):
            raise ValueError("A FreeCAD document is required")

        # Create the c++ DocumentObject
        # see: https://wiki.freecad.org/App_FeaturePython
        obj = doc.addObject("App::DocumentObjectGroupPython", name or "DrawingGroup")

        # Bind the Python Proxy
        proxy = cls(obj, title=title, src_item=src_item)

        # Manage Gui (ViewProvider) if available
        if App.GuiUp and hasattr(obj, "ViewObject"):
            from .drawing_group_vp import DrawingGroupViewProvider
            DrawingGroupViewProvider(obj.ViewObject)

        obj.recompute()
        return proxy