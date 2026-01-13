from django.db import models

class CVERecord(models.Model):
    cve_id = models.CharField(max_length=50)
    event_name = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    raw_payload = models.JSONField()


    def __str__(self):
        return self.cve_id



class CeleryTaskTracker(models.Model):
    task_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        default="PENDING"
    )  # Optional: store last known status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_id} ({self.status})"
