"""
errepi-py - Python bindings for Errepi Net microservices

Copyright © 2023-2025 Errepi Net S.R.L.
Author: Valerio Faiuolo <valerio.faiuolo@errepinet.it>

All rights reserved. This software is the property of Errepi Net S.R.L.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited without express written permission.
"""

from pydantic import BaseModel


class AppInfo(BaseModel):
    """
    Application information, version, and build details.

    Mirrors the AppInfo message of the service protos (cron_bridge.proto,
    generic_regs.proto).

    Attributes:
        build_date: Build date as a string.
        build_datetime: Build date and time as a string.
        build_time: Build time as a string.
        build_timestamp: Build timestamp as a string.
        git_branch: Git branch name.
        git_hash: Git commit hash.
        name: Application name.
        version: Application version.
    """

    build_date: str
    build_datetime: str
    build_time: str
    build_timestamp: str
    git_branch: str
    git_hash: str
    name: str
    version: str
