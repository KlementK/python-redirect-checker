import asyncio
from enum import Enum
import httpx
from pydantic import HttpUrl


class CheckStatus(str, Enum):
    OK = "OK"
    FAIL = "FAIL"
    ERROR = "ERROR"


class CheckResult:
    def __init__(
        self, initial_url: HttpUrl, expected_redirect: HttpUrl, status: CheckStatus
    ):
        self.initial_url = initial_url
        self.expected_redirect = expected_redirect
        self.status = status


TIMEOUT = 10.0
DELAY_BETWEEN_REQUESTS = 0.75


async def check_redirect(
    client: httpx.AsyncClient, initial_url: HttpUrl, expected_redirect: HttpUrl
) -> CheckResult:
    try:
        response = await client.get(
            str(initial_url),
            follow_redirects=True,
            timeout=TIMEOUT,
        )

        final_url = str(response.url).rstrip("/")
        expected = str(expected_redirect).rstrip("/")

        status = CheckStatus.OK if final_url == expected else CheckStatus.FAIL

    except Exception:
        status = CheckStatus.ERROR

    return CheckResult(initial_url, expected_redirect, status)


async def check_all_redirects(checks: list) -> list[CheckResult]:
    results = []

    async with httpx.AsyncClient() as client:
        for check in checks:
            result = await check_redirect(
                client, check.initial_url, check.expected_redirect
            )
            results.append(result)
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)

    return results
