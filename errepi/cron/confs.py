"""
errepi-py - Python bindings for Errepi Net microservices

Copyright © 2023-2025 Errepi Net S.R.L.
Author: Valerio Faiuolo <valerio.faiuolo@errepinet.it>

All rights reserved. This software is the property of Errepi Net S.R.L.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited without express written permission.
"""

from pydantic import BaseModel


class CronClientConfiguration(BaseModel):
    """
    Connection configuration for the cron client.

    Attributes:
        host: Host of the cron microservice.
        port: Port of the cron microservice.
    """

    host: str = "localhost"
    port: int = 50051
