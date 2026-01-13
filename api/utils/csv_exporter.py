import csv
from datetime import datetime
from pathlib import Path

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)


def export_to_csv(records):
    filename = f"who_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = EXPORT_DIR / filename

    headers = [
        "cve_id",
        "published_date",
        "last_modified_date",
        "description",
        "vuln_status",
        "severity",
        "cvss_version",
        "cvss_score",
        "attack_vector",
        "access_complexity",
        "confidentiality_impact",
        "integrity_impact",
        "availability_impact",
        "source_identifier",
        "reference_urls",
        "created_at",
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for r in records:
            payload = r.raw_payload or {}
            cve = payload.get("cve", {})

            # Description
            descriptions = cve.get("descriptions", [])
            description = descriptions[0].get("value") if descriptions else ""

            # CVSS (V2 handling – as per your data)
            metrics = cve.get("metrics", {})
            cvss_list = metrics.get("cvssMetricV2", [])
            cvss = cvss_list[0] if cvss_list else {}
            cvss_data = cvss.get("cvssData", {})

            # References
            references = cve.get("references", [])
            reference_urls = ", ".join(ref.get("url", "") for ref in references)

            writer.writerow({
                "cve_id": r.cve_id,
                "published_date": r.published_date,
                "last_modified_date": r.last_modified_date,
                "description": description,
                "vuln_status": cve.get("vulnStatus"),
                "severity": cvss.get("baseSeverity"),
                "cvss_version": cvss_data.get("version"),
                "cvss_score": cvss_data.get("baseScore"),
                "attack_vector": cvss_data.get("accessVector"),
                "access_complexity": cvss_data.get("accessComplexity"),
                "confidentiality_impact": cvss_data.get("confidentialityImpact"),
                "integrity_impact": cvss_data.get("integrityImpact"),
                "availability_impact": cvss_data.get("availabilityImpact"),
                "source_identifier": cve.get("sourceIdentifier"),
                "reference_urls": reference_urls,
                "created_at": r.created_at,
            })

    return str(file_path)
