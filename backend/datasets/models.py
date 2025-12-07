import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def upload_csv_path(instance, filename):
    return f'uploads/{instance.id}.csv'


def report_path(instance, filename):
    return f'reports/{instance.id}.pdf'
def clean_csv_path(instance, filename):
    # stored under media/clean/<uuid>.csv
    return f'clean/{instance.id}.csv'


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # allow null temporarily so migrations can be created safely for existing DBs
    filename = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    csv_file = models.FileField(upload_to=upload_csv_path, null=True, blank=True)
    cleaned_csv = models.FileField(upload_to=clean_csv_path, null=True, blank=True)

    total_rows = models.IntegerField(null=True, blank=True)
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    type_distribution = models.JSONField(null=True, blank=True)

    summary_pdf = models.FileField(upload_to=report_path, null=True, blank=True)
    analytics = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Dataset {self.filename} ({self.id})"
