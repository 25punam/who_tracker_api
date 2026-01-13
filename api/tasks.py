from celery import shared_task
from .services.who_client import fetch_first_100
from .utils.csv_exporter import export_to_csv
from .models import CVERecord
import time

@shared_task(bind=True)
def fetch_who_data_task(self):
    data = fetch_first_100()
    items = data.get("vulnerabilities", [])

    records = []

    for item in items:
        cve = item.get("cve", {})

        record = CVERecord.objects.create(
            cve_id=cve.get("id"),
            published_date=cve.get("published"),
            last_modified_date=cve.get("lastModified"),
            raw_payload=item
        )
        records.append(record)

        time.sleep(0.1)  # simulate long task

    csv_file = export_to_csv(records)

    return {
        "records_saved": len(records),
        "csv_file": csv_file
    }

