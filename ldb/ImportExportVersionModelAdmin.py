from import_export.admin import ImportMixin, ExportMixin
from reversion.admin import VersionAdmin


class ImportExportVersionModelAdmin(ImportMixin, ExportMixin, VersionAdmin):
    """
    Import, export and Version admin.
    Fixes missing link in change_list admin view
    """
    #: template for change_list view
    change_list_template = 'admin/change_list_import_export_version.html'

    # Might be needed if importing from windows created file
    from_encoding = "utf-8-sig"
