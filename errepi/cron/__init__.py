from .models import (
    AppInfo,
    ConfigurationEntry,
    ConfigurationEntrySet,
    HTTPJob,
    Job,
    JobCreateUpdate,
    JobExecutionResult,
    JobType,
    JobTypeHttp,
    Ref,
    RefCreateUpdate,
)


import requests


import os
from typing import List


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
