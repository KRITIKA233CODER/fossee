from django.contrib import admin
import os
from .models import Dataset

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    # Use admin methods for display so missing model fields don't crash admin checks
    list_display = (
        'filename_display',
        'uploaded_at_display',
        'uploaded_by_display',
        'total_rows_display',
    )
    readonly_fields = ('uploaded_at_display',)

    def filename_display(self, obj):
        # Prefer a 'filename' attribute, otherwise try FileField 'csv_file' or 'cleaned_csv'
        if hasattr(obj, 'filename') and obj.filename:
            return obj.filename
        file_candidate = None
        for f in ('csv_file', 'cleaned_csv'):
            if hasattr(obj, f) and getattr(obj, f):
                file_candidate = getattr(obj, f)
                break
        if file_candidate:
            # file_candidate could be a FieldFile
            try:
                return os.path.basename(file_candidate.name)
            except Exception:
                return str(file_candidate)
        return '(no file)'
    filename_display.short_description = 'Filename'

    def uploaded_at_display(self, obj):
        # show uploaded_at if present else fallback to created/created_at
        for name in ('uploaded_at', 'created_at', 'timestamp', 'created'):
            if hasattr(obj, name):
                return getattr(obj, name)
        return '(no date)'
    uploaded_at_display.short_description = 'Uploaded At'

    def uploaded_by_display(self, obj):
        # show uploaded_by or uploader or user
        for name in ('uploaded_by', 'uploader', 'user', 'owner'):
            if hasattr(obj, name):
                return getattr(obj, name)
        return '(unknown)'
    uploaded_by_display.short_description = 'Uploaded By'

    def total_rows_display(self, obj):
        for name in ('total_rows', 'row_count', 'num_rows'):
            if hasattr(obj, name):
                return getattr(obj, name)
        # as fallback, try counting a stored CSV (expensive) but safe to omit
        return '(n/a)'
    total_rows_display.short_description = 'Total Rows'
