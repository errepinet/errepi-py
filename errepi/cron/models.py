"""
errepi-py - Python bindings for Errepi Net microservices

Copyright © 2023-2025 Errepi Net S.R.L.
Author: Valerio Faiuolo <valerio.faiuolo@errepinet.it>

All rights reserved. This software is the property of Errepi Net S.R.L.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited without express written permission.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, conint, RootModel

from errepi.models import AppInfo


class CronConfiguration(BaseModel):
    """
    Job configuration, including max retries and retry delay.

    Attributes:
        job_max_retries: Maximum number of retries for a job.
        job_retry_delay_secs: Delay in seconds between retries.
        set_at: Datetime when the configuration was set (absent on set payloads).
    """

    job_max_retries: conint(ge=0)  # type: ignore
    job_retry_delay_secs: conint(ge=0)  # type: ignore
    set_at: Optional[datetime] = None


class CornettiError(BaseModel):
    """
    Generic error returned by the Cornetti system.

    Attributes:
        detail: Error detail message.
        status: Error status code.
    """

    detail: str
    status: conint(ge=0)  # type: ignore


class JobBodyType(str, Enum):
    """
    Type of HTTP job body (Json or Text).
    """

    Json = "Json"
    Text = "Text"


class JobExecutionResult(BaseModel):
    """
    Result of a job execution.

    Attributes:
        date_time: Datetime of the execution.
        detail: Execution detail message.
        is_success: Whether the execution was successful.
        job_id: ID of the executed job.
        namespace: Namespace of the executed job.
    """

    date_time: datetime
    detail: str
    is_success: bool
    job_id: str
    namespace: str


class JobFrequencyHour(BaseModel):
    """
    Job execution frequency by hour.

    Attributes:
        Hour: The hour value for frequency.
    """

    Hour: conint(ge=0)  # type: ignore


class JobFrequencyDay(BaseModel):
    """
    Job execution frequency by day.

    Attributes:
        Day: The day value for frequency.
    """

    Day: conint(ge=0)  # type: ignore


class JobFrequencyWeek(BaseModel):
    """
    Job execution frequency by week.

    Attributes:
        Week: The week value for frequency.
    """

    Week: conint(ge=0)  # type: ignore


class JobFrequencyMonth(BaseModel):
    """
    Job execution frequency by month.

    Attributes:
        Month: The month value for frequency.
    """

    Month: conint(ge=0)  # type: ignore


class JobFrequencyMinute(BaseModel):
    """
    Job execution frequency by minute.

    Attributes:
        Minute: The minute value for frequency.
    """

    Minute: conint(ge=0)  # type: ignore


class JobFrequency(RootModel):
    """
    Job execution frequency (hourly, daily, weekly, monthly, or by minute).

    Attributes:
        root: One of the frequency types (hour, day, week, month, minute).
    """

    root: Union[
        JobFrequencyHour,
        JobFrequencyDay,
        JobFrequencyWeek,
        JobFrequencyMonth,
        JobFrequencyMinute,
    ]


class JobHttpMethod(str, Enum):
    """
    Supported HTTP methods for jobs.
    """

    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"


class JobStatus(str, Enum):
    """
    Job status values.
    """

    Scheduled = "Scheduled"
    Rescheduled = "Rescheduled"
    RetryScheduled = "RetryScheduled"
    Ok = "Ok"
    Failed = "Failed"


class Ref(BaseModel):
    """
    Reference to a configuration or value with timestamp.

    Attributes:
        setted_at: Datetime when the value was set.
        value: The referenced value.
    """

    setted_at: datetime
    value: str


class RefCreateUpdate(BaseModel):
    """
    Payload for creating or updating a reference.

    Attributes:
        value: The value to set or update.
    """

    value: str


class HTTPJob(BaseModel):
    """
    Definition of an HTTP job, with parameters such as URL, method, body, and headers.

    Attributes:
        body: Optional request body as a string.
        body_type: Optional type of the request body (Json or Text).
        headers: Optional dictionary of HTTP headers.
        method: HTTP method to use for the job.
        timeout_seconds: Optional timeout in seconds for the request.
        url: Target URL for the HTTP request.
        user_agent: Optional user agent string.
        valid_http_codes: Optional list of valid HTTP status codes.
    """

    body: Optional[str] = None
    body_type: Optional[JobBodyType] = None
    headers: Optional[Dict[str, str]] = None
    method: JobHttpMethod
    timeout_seconds: Optional[conint(ge=0)] = None  # type: ignore
    url: str
    user_agent: Optional[str] = None
    valid_http_codes: Optional[List[conint(ge=0)]] = None  # type: ignore


class JobTypeHttp(BaseModel):
    """
    HTTP job type, encapsulates an HTTPJob object.

    Attributes:
        Http: The HTTPJob instance.
    """

    Http: HTTPJob


class JobType(RootModel):
    """
    Generic job type, currently only HTTP is supported.

    Attributes:
        root: The job type (JobTypeHttp).
    """

    root: JobTypeHttp


class Job(BaseModel):
    """
    Represents a scheduled job, with configuration, status, type, and frequency.

    Attributes:
        configuration: Job configuration entry.
        created: Datetime when the job was created.
        curr_retries: Current number of retries.
        description: Optional job description.
        enabled: Whether the job is enabled.
        frequency: Optional job execution frequency.
        id: Autogenerated job ID.
        job_status: Current status of the job.
        job_type: Type of the job.
        last_execution_dt: Datetime of the last execution.
        next_execution_dt: Datetime of the next scheduled execution.
        updated: Datetime of the last update.
    """

    configuration: CronConfiguration
    created: datetime
    curr_retries: conint(ge=0)  # type: ignore
    description: Optional[str] = None
    enabled: bool
    frequency: Optional[JobFrequency] = None
    id: str
    job_status: JobStatus
    job_type: JobType
    last_execution_dt: Optional[datetime] = None
    next_execution_dt: datetime
    updated: Optional[datetime] = None


class JobCreateUpdate(BaseModel):
    """
    Payload for creating or updating a job.

    Attributes:
        description: Optional job description.
        enabled: Whether the job is enabled.
        frequency: Optional job execution frequency.
        job_type: Type of the job.
        next_execution_dt: Datetime in UTC of the next scheduled execution.
        use_configuration: Optional configuration ID to use.
    """

    description: Optional[str] = None
    enabled: bool
    frequency: Optional[JobFrequency] = None
    job_type: JobType
    next_execution_dt: datetime
    use_configuration: Optional[str] = None
