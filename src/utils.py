import csv
from pathlib import Path
from pydantic import BaseModel, HttpUrl


class RedirectCheck(BaseModel):
    initial_url: HttpUrl
    expected_redirect: HttpUrl


def read_csv(csv_path: Path) -> list[RedirectCheck]:
    checks = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            checks.append(
                RedirectCheck(
                    initial_url=row["INITIAL_URL"],
                    expected_redirect=row["EXPECTED_REDIRECT"],
                )
            )
    return checks


def format_url_for_display(url: str) -> str:
    return url.replace("https://", "").replace("http://", "")
