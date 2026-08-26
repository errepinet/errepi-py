"""
errepi-py - Python bindings for Errepi Net microservices

Copyright © 2023-2025 Errepi Net S.R.L.
Author: Valerio Faiuolo <valerio.faiuolo@errepinet.it>

All rights reserved. This software is the property of Errepi Net S.R.L.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited without express written permission.
"""

from pydantic import BaseModel, conint


class RegsClientConfiguration(BaseModel):
    """
    Connection configuration for the generic registries client.

    Attributes:
        host: Host of the generic registries microservice.
        port: Port of the generic registries microservice.
        max_retries: Number of retry attempts on transient gRPC failures.
        retry_delay_secs: Base delay in seconds between retry attempts.
    """

    host: str = "localhost"
    port: int = 50051
    max_retries: conint(ge=0) = 3  # type: ignore
    retry_delay_secs: conint(ge=0) = 1  # type: ignore
