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
        self,
        initial_url: HttpUrl,
        expected_redirect: HttpUrl,
        status: CheckStatus,
        actual_redirect: str | None = None,
    ):
        self.initial_url = initial_url
        self.expected_redirect = expected_redirect
        self.status = status
        self.actual_redirect = actual_redirect


TIMEOUT = 30.0
DELAY_BETWEEN_REQUESTS = 0.75
MAX_CONCURRENT_REQUESTS = 3


async def check_redirect(
    client: httpx.AsyncClient, initial_url: HttpUrl, expected_redirect: HttpUrl
) -> CheckResult:
    try:
        response = await client.get(
            str(initial_url),
            follow_redirects=True,
            timeout=TIMEOUT,
        )

        final_url = (
            str(response.url).rstrip("/").replace("https://", "").replace("http://", "")
        )
        expected = (
            str(expected_redirect)
            .rstrip("/")
            .replace("https://", "")
            .replace("http://", "")
        )

        if final_url == expected:
            status = CheckStatus.OK
            actual_redirect = None
        else:
            status = CheckStatus.FAIL
            actual_redirect = final_url

    except Exception:
        status = CheckStatus.ERROR
        actual_redirect = None

    return CheckResult(initial_url, expected_redirect, status, actual_redirect)


async def check_all_redirects(checks: list) -> list[CheckResult]:
    results = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async def check_with_semaphore(check):
        async with semaphore:
            result = await check_redirect(
                client, check.initial_url, check.expected_redirect
            )
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
            return result

    async with httpx.AsyncClient() as client:
        tasks = [check_with_semaphore(check) for check in checks]
        results = await asyncio.gather(*tasks)

    return results
