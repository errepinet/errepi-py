from .models import (
    AppInfo,
    CronClientConfiguration,
    CronConfiguration,
    HTTPJob,
    Job,
    JobCreateUpdate,
    JobExecutionResult,
    JobType,
    JobTypeHttp,
    Ref,
    RefCreateUpdate,
)


import grpc
from typing import List, Optional

from errepi.gen import cron_bridge_pb2 as pb
from errepi.gen import cron_bridge_pb2_grpc as pb_grpc

from . import conversions


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
    Client for interacting with the Errepi Net Cron microservice (CronBridgeService).

    This class provides methods to retrieve application info, manage job
    configurations, refs and scheduled jobs over gRPC.

    The interface mirrors the RPCs of protos/cron_bridge.proto: every
    operation takes the tenant_id and namespace of the resource.
    """

    def __init__(self, config: Optional[CronClientConfiguration] = None) -> None:
        """
        Initialize the CronConfigurator client.

        Args:
            config (Optional[CronClientConfiguration]): Connection configuration
                (host and port). Defaults to 'localhost:50051'.
        """
        if config is None:
            config = CronClientConfiguration()
        self.config = config
        self.target = f"{config.host}:{config.port}"
        self._channel = grpc.insecure_channel(self.target)
        self._stub = pb_grpc.CronBridgeServiceStub(self._channel)

    def app_info(self) -> AppInfo:
        """
        Retrieve application build and version information (GetAppInfo).

        Returns:
            AppInfo: Application information object.
        """
        return conversions.app_info_from_pb(self._stub.GetAppInfo(pb.Empty()))

    def get_configuration(self, tenant_id: str, namespace: str, name: str) -> CronConfiguration:
        """
        Get a job configuration entry by namespace and name (CronConfigurationGet).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The configuration namespace.
            name (str): The configuration name.

        Returns:
            CronConfiguration: The configuration entry object.
        """
        response = self._stub.CronConfigurationGet(
            pb.CronConfigurationGetRequest(
                tenant_id=tenant_id, namespace=namespace, name=name
            )
        )
        return conversions.configuration_from_pb(response)

    def set_configuration(
        self,
        tenant_id: str,
        namespace: str,
        name: str,
        config: CronConfiguration,
    ) -> CronConfiguration:
        """
        Set or update a job configuration entry (CronConfigurationSet).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The configuration namespace.
            name (str): The configuration name.
            config (CronConfiguration): The configuration values to set.

        Returns:
            CronConfiguration: The updated configuration entry.
        """
        response = self._stub.CronConfigurationSet(
            pb.CronConfigurationSetRequest(
                tenant_id=tenant_id,
                namespace=namespace,
                name=name,
                configuration=conversions.configuration_set_to_pb(config),
            )
        )
        return conversions.configuration_from_pb(response)

    def unset_configuration(self, tenant_id: str, namespace: str, name: str) -> None:
        """
        Remove a job configuration entry (CronConfigurationUnset).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The configuration namespace.
            name (str): The configuration name.
        """
        self._stub.CronConfigurationUnset(
            pb.CronConfigurationUnsetRequest(
                tenant_id=tenant_id, namespace=namespace, name=name
            )
        )
        return None

    def list_jobs(self, tenant_id: str, namespace: str) -> List[Job]:
        """
        List all jobs in a given namespace (CronJobsList).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The namespace to list jobs from.

        Returns:
            List[Job]: List of job objects.
        """
        response = self._stub.CronJobsList(
            pb.CronJobsListRequest(tenant_id=tenant_id, namespace=namespace)
        )
        return [conversions.job_from_pb(job) for job in response.jobs]

    def create_job(
        self, tenant_id: str, namespace: str, job: JobCreateUpdate
    ) -> Job:
        """
        Create a new scheduled job in the given namespace (CronJobCreate).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The namespace for the job.
            job (JobCreateUpdate): The job creation payload.

        Returns:
            Job: The created job object.
        """
        response = self._stub.CronJobCreate(
            pb.CronJobCreateRequest(
                tenant_id=tenant_id,
                namespace=namespace,
                job=conversions.job_create_update_to_pb(job),
            )
        )
        return conversions.job_from_pb(response)

    def update_job(
        self, tenant_id: str, namespace: str, job_id: str, job: JobCreateUpdate
    ) -> Job:
        """
        Update an existing job by ID in the given namespace (CronJobUpdate).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The namespace of the job.
            job_id (str): The job ID.
            job (JobCreateUpdate): The job update payload.

        Returns:
            Job: The updated job object.
        """
        response = self._stub.CronJobUpdate(
            pb.CronJobUpdateRequest(
                tenant_id=tenant_id,
                namespace=namespace,
                job_id=job_id,
                job=conversions.job_create_update_to_pb(job),
            )
        )
        return conversions.job_from_pb(response)

    def delete_job(self, tenant_id: str, namespace: str, job_id: str) -> None:
        """
        Delete a job by ID in the given namespace (CronJobDelete).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The namespace of the job.
            job_id (str): The job ID.
        """
        self._stub.CronJobDelete(
            pb.CronJobDeleteRequest(
                tenant_id=tenant_id, namespace=namespace, job_id=job_id
            )
        )
        return None

    def get_job(self, tenant_id: str, namespace: str, job_id: str) -> Job:
        """
        Retrieve a single job by its ID (CronJobGet).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The namespace of the job.
            job_id (str): The job ID.

        Returns:
            Job: The job object.
        """
        response = self._stub.CronJobGet(
            pb.CronJobGetRequest(
                tenant_id=tenant_id, namespace=namespace, job_id=job_id
            )
        )
        return conversions.job_from_pb(response)

    def job_results(
        self, tenant_id: str, namespace: str, job_id: str
    ) -> List[JobExecutionResult]:
        """
        Get the execution results for a single job by its ID (CronJobResults).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The namespace of the job.
            job_id (str): The job ID.

        Returns:
            List[JobExecutionResult]: List of job execution result objects.
        """
        response = self._stub.CronJobResults(
            pb.CronJobResultsRequest(
                tenant_id=tenant_id, namespace=namespace, job_id=job_id
            )
        )
        return [conversions.job_execution_result_from_pb(r) for r in response.results]

    def get_ref(self, tenant_id: str, namespace: str, key: str) -> Ref:
        """
        Retrieve a reference value by namespace and key (CronRefGet).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The reference namespace.
            key (str): The reference key.

        Returns:
            Ref: The reference object.
        """
        response = self._stub.CronRefGet(
            pb.CronRefGetRequest(
                tenant_id=tenant_id, namespace=namespace, key=key
            )
        )
        return conversions.ref_from_pb(response)

    def set_ref(
        self, tenant_id: str, namespace: str, key: str, ref: RefCreateUpdate
    ) -> Ref:
        """
        Set or update a reference value (CronRefSet).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The reference namespace.
            key (str): The reference key.
            ref (RefCreateUpdate): The reference value to set.

        Returns:
            Ref: The updated reference object.
        """
        response = self._stub.CronRefSet(
            pb.CronRefSetRequest(
                tenant_id=tenant_id,
                namespace=namespace,
                key=key,
                ref=conversions.ref_create_update_to_pb(ref),
            )
        )
        return conversions.ref_from_pb(response)

    def unset_ref(self, tenant_id: str, namespace: str, key: str) -> None:
        """
        Remove a reference value by namespace and key (CronRefUnset).

        Args:
            tenant_id (str): The tenant ID.
            namespace (str): The reference namespace.
            key (str): The reference key.
        """
        self._stub.CronRefUnset(
            pb.CronRefUnsetRequest(
                tenant_id=tenant_id, namespace=namespace, key=key
            )
        )
        return None
