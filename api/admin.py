from django.contrib import admin
from .models import CVERecord
from django_celery_results.models import TaskResult

@admin.register(CVERecord)
class CVERecordAdmin(admin.ModelAdmin):
    # Ye fields admin list view me dikhenge
    list_display = (
        "cve_id",
        "published_date",
        "last_modified_date",
        "created_at",
    )

    # Ye fields search ke liye use honge
    search_fields = ("cve_id", "description", "source_identifier")

    # Ye filter sidebar me dikhega
    list_filter = ("published_date", "last_modified_date")

    # Optional: datetime formatting
    readonly_fields = ("created_at",)

