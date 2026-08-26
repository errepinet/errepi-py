"""
Retry helper for gRPC calls: transient failures (connection unavailable,
deadline exceeded) are retried with exponential backoff before raising.
"""

from __future__ import annotations

import time
from typing import Callable, TypeVar

import grpc

T = TypeVar("T")

_RETRYABLE_CODES = {
    grpc.StatusCode.UNAVAILABLE,
    grpc.StatusCode.DEADLINE_EXCEEDED,
}


def call_with_retry(
    fn: Callable[[], T],
    retries: int = 3,
    delay: float = 1.0,
) -> T:
    """
    Call fn, retrying on transient gRPC failures with exponential backoff.

    Args:
        fn: Callable performing the gRPC call.
        retries: Number of retry attempts after the first failure.
        delay: Base delay in seconds between attempts (doubled each retry).

    Returns:
        The result of fn.

    Raises:
        grpc.RpcError: The last error once retries are exhausted, or any
            non-transient error immediately.
    """
    last_error: grpc.RpcError | None = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except grpc.RpcError as error:
            if error.code() not in _RETRYABLE_CODES:
                raise
            last_error = error
            if attempt < retries:
                time.sleep(delay * (2**attempt))
    assert last_error is not None
    raise last_error
