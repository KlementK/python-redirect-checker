import asyncio
from pathlib import Path
from src.utils import read_csv, format_url_for_display
from src.engine import check_all_redirects


def main():
    csv_path = Path("data/urls.csv")

    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        return

    checks = read_csv(csv_path)
    results = asyncio.run(check_all_redirects(checks))

    for result in results:
        initial = format_url_for_display(str(result.initial_url))
        expected = format_url_for_display(str(result.expected_redirect))
        print(f"{initial} - {expected} - {result.status.value}")


if __name__ == "__main__":
    main()
