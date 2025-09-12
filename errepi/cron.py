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
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, conint, RootModel
import requests


class AppInfo(BaseModel):
    """
    Application information, version, and build details.

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


class ConfigurationEntry(BaseModel):
    """
    Job configuration entry, including max retries and retry delay.

    Attributes:
        job_max_retries: Maximum number of retries for a job.
        job_retry_delay_secs: Delay in seconds between retries.
        set_at: Datetime when the configuration was set.
    """

    job_max_retries: conint(ge=0)  # type: ignore
    job_retry_delay_secs: conint(ge=0)  # type: ignore
    set_at: datetime


class ConfigurationEntrySet(BaseModel):
    """
    Set of job configuration values (without timestamp).

    Attributes:
        job_max_retries: Maximum number of retries for a job.
        job_retry_delay_secs: Delay in seconds between retries.
    """

    job_max_retries: conint(ge=0)  # type: ignore
    job_retry_delay_secs: conint(ge=0)  # type: ignore


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
    """

    date_time: datetime
    detail: str
    is_success: bool
    job_id: str


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

    configuration: ConfigurationEntry
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


def http_job_type(http_job: HTTPJob) -> JobType:
    """
    Create a JobType instance encapsulating the given HTTPJob.

    Args:
        http_job (HTTPJob): The HTTP job definition.

    Returns:
        JobType: The JobType instance containing the HTTP job.
    """
    return JobType(JobTypeHttp(Http=http_job))


class CronConfigurator:
    """
    Client for interacting with the Errepi Net Cron microservice API.

    This class provides methods to retrieve application info, manage job configurations,
    and create, update, list, or delete scheduled jobs via HTTP requests.

    Methods:
        - from_env(): Instantiate from environment variable or default URL.
        - app_info(): Get application build and version info.
        - get_configuration(): Retrieve a job configuration entry.
        - set_configuration(): Set or update a job configuration.
        - unset_configuration(): Remove a job configuration.
        - list_jobs(): List all jobs in a namespace.
        - create_job(): Create a new scheduled job.
        - update_job(): Update an existing job.
        - delete_job(): Delete a job by ID.
        - single_job(): Retrieve a single job by ID.
        - single_job_execution_results(): Get execution results for a job.
        - get_ref(): Retrieve a reference value.
        - set_ref(): Set or update a reference value.
        - unset_ref(): Remove a reference value.
    """

    def __init__(self, URL) -> None:
        """
        Initialize the CronConfigurator client.

        Args:
            URL (str): Base URL of the Cron microservice API.
        """
        self.URL = URL

    @staticmethod
    def from_env() -> "CronConfigurator":
        """
        Create a CronConfigurator instance using the ERREPI_CRON_CONF_URL environment variable.
        If the variable is not set, defaults to 'http://localhost:8080'.

        Returns:
            CronConfigurator: Configurator instance with the resolved URL.
        """
        import os

        url = os.getenv("ERREPI_CRON_CONF_URL", "http://localhost:8080")
        return CronConfigurator(URL=url)

    def app_info(self) -> AppInfo:
        """
        Retrieve application build and version information from the API.

        Returns:
            AppInfo: Application information object.
        """
        response = requests.get(f"{self.URL}/")
        response.raise_for_status()
        return AppInfo(**response.json())

    def get_configuration(self, namespace: str, name: str) -> ConfigurationEntry:
        """
        Get a job configuration entry by namespace and name.

        Args:
            namespace (str): The configuration namespace.
            name (str): The configuration name.

        Returns:
            ConfigurationEntry: The configuration entry object.
        """
        response = requests.get(f"{self.URL}/configurations/{namespace}/{name}")
        response.raise_for_status()
        return ConfigurationEntry(**response.json())

    def set_configuration(
        self, namespace: str, name: str, config: ConfigurationEntrySet
    ) -> ConfigurationEntry:
        """
        Set or update a job configuration entry.

        Args:
            namespace (str): The configuration namespace.
            name (str): The configuration name.
            config (ConfigurationEntrySet): The configuration values to set.

        Returns:
            ConfigurationEntry: The updated configuration entry.
        """
        response = requests.post(
            f"{self.URL}/configurations/{namespace}/{name}",
            json=config.model_dump(mode="json"),
        )
        response.raise_for_status()
        return ConfigurationEntry(**response.json())

    def unset_configuration(self, namespace: str, name: str) -> None:
        """
        Remove a job configuration entry by namespace and name.

        Args:
            namespace (str): The configuration namespace.
            name (str): The configuration name.
        """
        response = requests.delete(f"{self.URL}/configurations/{namespace}/{name}")
        response.raise_for_status()
        return None

    def list_jobs(self, namespace: str) -> List[Job]:
        """
        List all jobs in a given namespace.

        Args:
            namespace (str): The namespace to list jobs from.

        Returns:
            List[Job]: List of job objects.
        """
        response = requests.get(f"{self.URL}/jobs/{namespace}")

        response.raise_for_status()
        jobs = response.json()
        return [Job(**job) for job in jobs]

    def create_job(self, namespace: str, job: JobCreateUpdate) -> Job:
        """
        Create a new scheduled job in the given namespace.

        Args:
            namespace (str): The namespace for the job.
            job (JobCreateUpdate): The job creation payload.

        Returns:
            Job: The created job object.
        """
        response = requests.post(
            f"{self.URL}/jobs/{namespace}",
            json=job.model_dump(mode="json"),
        )
        response.raise_for_status()
        return Job(**response.json())

    def update_job(self, namespace: str, job_id: str, job: JobCreateUpdate) -> Job:
        """
        Update an existing job by ID in the given namespace.

        Args:
            namespace (str): The namespace of the job.
            job_id (str): The job ID.
            job (JobCreateUpdate): The job update payload.

        Returns:
            Job: The updated job object.
        """
        response = requests.put(
            f"{self.URL}/jobs/{namespace}/{job_id}",
            json=job.model_dump(mode="json"),
        )

        response.raise_for_status()
        return Job(**response.json())

    def delete_job(self, namespace: str, job_id: str) -> None:
        """
        Delete a job by ID in the given namespace.

        Args:
            namespace (str): The namespace of the job.
            job_id (str): The job ID.
        """
        response = requests.delete(f"{self.URL}/jobs/{namespace}/{job_id}")
        response.raise_for_status()
        return None

    def single_job(self, job_id: str) -> Job:
        """
        Retrieve a single job by its ID.

        Args:
            job_id (str): The job ID.

        Returns:
            Job: The job object.
        """
        response = requests.get(f"{self.URL}/jobs/single/{job_id}")
        response.raise_for_status()
        return Job(**response.json())

    def single_job_execution_results(self, job_id: str) -> List[JobExecutionResult]:
        """
        Get the execution results for a single job by its ID.

        Args:
            job_id (str): The job ID.

        Returns:
            List[JobExecutionResult]: List of job execution result objects.
        """
        response = requests.get(f"{self.URL}/jobs/single/{job_id}/results")
        response.raise_for_status()
        results = response.json()
        return [JobExecutionResult(**result) for result in results]

    def get_ref(self, namespace: str, name: str) -> Ref:
        """
        Retrieve a reference value by namespace and name.

        Args:
            namespace (str): The reference namespace.
            name (str): The reference name.

        Returns:
            Ref: The reference object.
        """
        response = requests.get(f"{self.URL}/refs/{namespace}/{name}")
        response.raise_for_status()
        return Ref(**response.json())

    def set_ref(self, namespace: str, name: str, ref: RefCreateUpdate) -> Ref:
        """
        Set or update a reference value.

        Args:
            namespace (str): The reference namespace.
            name (str): The reference name.
            ref (RefCreateUpdate): The reference value to set.

        Returns:
            Ref: The updated reference object.
        """
        response = requests.post(
            f"{self.URL}/refs/{namespace}/{name}",
            json=ref.model_dump(mode="json"),
        )
        response.raise_for_status()
        return Ref(**response.json())

    def unset_ref(self, namespace: str, name: str) -> None:
        """
        Remove a reference value by namespace and name.

        Args:
            namespace (str): The reference namespace.
            name (str): The reference name.
        """
        response = requests.delete(f"{self.URL}/refs/{namespace}/{name}")
        response.raise_for_status()
        return None
