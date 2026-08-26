"""
Conversion helpers between pydantic models and generated protobuf messages.

Mappings follow the messages of protos/cron_bridge.proto (AppInfo included).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp

from errepi.gen import cron_bridge_pb2 as pb
from errepi.models import AppInfo

from .models import (
    CronConfiguration,
    HTTPJob,
    Job,
    JobBodyType,
    JobCreateUpdate,
    JobExecutionResult,
    JobFrequency,
    JobFrequencyDay,
    JobFrequencyHour,
    JobFrequencyMinute,
    JobFrequencyMonth,
    JobFrequencyWeek,
    JobHttpMethod,
    JobStatus,
    JobType,
    JobTypeHttp,
    Ref,
    RefCreateUpdate,
)

_JOB_STATUS_TO_MODEL = {
    "SCHEDULED": JobStatus.Scheduled,
    "RESCHEDULED": JobStatus.Rescheduled,
    "RETRY_SCHEDULED": JobStatus.RetryScheduled,
    "OK": JobStatus.Ok,
    "FAILED": JobStatus.Failed,
}
_JOB_STATUS_TO_PB = {
    JobStatus.Scheduled: "SCHEDULED",
    JobStatus.Rescheduled: "RESCHEDULED",
    JobStatus.RetryScheduled: "RETRY_SCHEDULED",
    JobStatus.Ok: "OK",
    JobStatus.Failed: "FAILED",
}

_JOB_BODY_TYPE_TO_MODEL = {
    "JSON": JobBodyType.Json,
    "TEXT": JobBodyType.Text,
}
_JOB_BODY_TYPE_TO_PB = {
    JobBodyType.Json: "JSON",
    JobBodyType.Text: "TEXT",
}

_JOB_METHOD_TO_MODEL = {
    "GET": JobHttpMethod.GET,
    "POST": JobHttpMethod.POST,
    "PATCH": JobHttpMethod.PATCH,
    "PUT": JobHttpMethod.PUT,
    "DELETE": JobHttpMethod.DELETE,
}
_JOB_METHOD_TO_PB = {
    JobHttpMethod.GET: "GET",
    JobHttpMethod.POST: "POST",
    JobHttpMethod.PATCH: "PATCH",
    JobHttpMethod.PUT: "PUT",
    JobHttpMethod.DELETE: "DELETE",
}


def _to_timestamp(dt: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def _from_timestamp(ts: Timestamp) -> datetime:
    return ts.ToDatetime().replace(tzinfo=timezone.utc)


def app_info_to_pb(info: AppInfo) -> pb.AppInfo:
    return pb.AppInfo(
        name=info.name,
        version=info.version,
        build_timestamp=info.build_timestamp,
        build_date=info.build_date,
        build_time=info.build_time,
        build_datetime=info.build_datetime,
        git_hash=info.git_hash,
        git_branch=info.git_branch,
    )


def app_info_from_pb(info: pb.AppInfo) -> AppInfo:
    return AppInfo(
        name=info.name,
        version=info.version,
        build_timestamp=info.build_timestamp,
        build_date=info.build_date,
        build_time=info.build_time,
        build_datetime=info.build_datetime,
        git_hash=info.git_hash,
        git_branch=info.git_branch,
    )


def configuration_to_pb(
    config: CronConfiguration,
) -> pb.CronConfigurationEntry:
    pb_config = pb.CronConfigurationEntry(
        job_max_retries=config.job_max_retries,
        job_retry_delay_secs=config.job_retry_delay_secs,
    )
    if config.set_at is not None:
        pb_config.set_at.CopyFrom(_to_timestamp(config.set_at))
    return pb_config


def configuration_from_pb(
    entry: pb.CronConfigurationEntry,
) -> CronConfiguration:
    return CronConfiguration(
        job_max_retries=entry.job_max_retries,
        job_retry_delay_secs=entry.job_retry_delay_secs,
        set_at=_from_timestamp(entry.set_at),
    )


def configuration_set_to_pb(
    config: CronConfiguration,
) -> pb.CronConfigurationEntrySet:
    return pb.CronConfigurationEntrySet(
        job_max_retries=config.job_max_retries,
        job_retry_delay_secs=config.job_retry_delay_secs,
    )


def ref_to_pb(ref: Ref) -> pb.CronRef:
    return pb.CronRef(
        value=ref.value,
        setted_at=_to_timestamp(ref.setted_at),
    )


def ref_from_pb(ref: pb.CronRef) -> Ref:
    return Ref(
        value=ref.value,
        setted_at=_from_timestamp(ref.setted_at),
    )


def ref_create_update_to_pb(ref: RefCreateUpdate) -> pb.CronRefCreateUpdate:
    return pb.CronRefCreateUpdate(value=ref.value)


def job_frequency_to_pb(
    frequency: JobFrequency,
) -> pb.CronJobFrequency:
    freq = frequency.root
    pb_freq = pb.CronJobFrequency()
    if isinstance(freq, JobFrequencyHour):
        pb_freq.hour = freq.Hour
    elif isinstance(freq, JobFrequencyDay):
        pb_freq.day = freq.Day
    elif isinstance(freq, JobFrequencyWeek):
        pb_freq.week = freq.Week
    elif isinstance(freq, JobFrequencyMonth):
        pb_freq.month = freq.Month
    elif isinstance(freq, JobFrequencyMinute):
        pb_freq.minute = freq.Minute
    return pb_freq


def job_frequency_from_pb(
    frequency: Optional[pb.CronJobFrequency],
) -> Optional[JobFrequency]:
    if frequency is None:
        return None
    which = frequency.WhichOneof("frequency")
    if which is None:
        return None
    value = getattr(frequency, which)
    model_cls = {
        "hour": JobFrequencyHour,
        "day": JobFrequencyDay,
        "week": JobFrequencyWeek,
        "month": JobFrequencyMonth,
        "minute": JobFrequencyMinute,
    }[which]
    return JobFrequency(model_cls(**{which.capitalize(): value}))


def http_job_to_pb(job: HTTPJob) -> pb.CronHttpJob:
    return pb.CronHttpJob(
        url=job.url,
        method=pb.CronJobHttpMethod.Value(_JOB_METHOD_TO_PB[job.method]),
        headers=job.headers or {},
        body=job.body,
        body_type=(
            pb.CronJobBodyType.Value(_JOB_BODY_TYPE_TO_PB[job.body_type])
            if job.body_type is not None
            else None
        ),
        timeout_seconds=job.timeout_seconds,
        user_agent=job.user_agent,
        valid_http_codes=list(job.valid_http_codes or []),
    )


def http_job_from_pb(job: pb.CronHttpJob) -> HTTPJob:
    return HTTPJob(
        url=job.url,
        method=_JOB_METHOD_TO_MODEL[pb.CronJobHttpMethod.Name(job.method)],
        headers=dict(job.headers) or None,
        body=job.body if job.HasField("body") else None,
        body_type=(
            _JOB_BODY_TYPE_TO_MODEL[pb.CronJobBodyType.Name(job.body_type)]
            if job.HasField("body_type")
            else None
        ),
        timeout_seconds=(
            job.timeout_seconds if job.HasField("timeout_seconds") else None
        ),
        user_agent=job.user_agent if job.HasField("user_agent") else None,
        valid_http_codes=list(job.valid_http_codes) or None,
    )


def job_type_to_pb(job_type: JobType) -> pb.CronJobType:
    return pb.CronJobType(http=http_job_to_pb(job_type.root.Http))


def job_type_from_pb(job_type: pb.CronJobType) -> JobType:
    which = job_type.WhichOneof("job_type")
    if which is None:
        raise ValueError(f"unsupported job type oneof: {which}")
    if which != "http":
        raise ValueError(f"unsupported job type oneof: {which}")
    return JobType(JobTypeHttp(Http=http_job_from_pb(job_type.http)))


def job_create_update_to_pb(
    job: JobCreateUpdate,
) -> pb.CronJobCreateUpdate:
    return pb.CronJobCreateUpdate(
        description=job.description,
        frequency=job_frequency_to_pb(job.frequency) if job.frequency else None,
        enabled=job.enabled,
        job_type=job_type_to_pb(job.job_type),
        next_execution_dt=_to_timestamp(job.next_execution_dt),
        use_configuration=job.use_configuration,
    )


def job_to_pb(job: Job) -> pb.CronJob:
    return pb.CronJob(
        id=job.id,
        description=job.description,
        frequency=job_frequency_to_pb(job.frequency) if job.frequency else None,
        created=_to_timestamp(job.created),
        updated=_to_timestamp(job.updated) if job.updated else None,
        last_execution_dt=(
            _to_timestamp(job.last_execution_dt) if job.last_execution_dt else None
        ),
        next_execution_dt=_to_timestamp(job.next_execution_dt),
        enabled=job.enabled,
        job_type=job_type_to_pb(job.job_type),
        job_status=pb.CronJobStatus.Value(_JOB_STATUS_TO_PB[job.job_status]),
        configuration=configuration_to_pb(job.configuration),
        curr_retries=job.curr_retries,
    )


def job_from_pb(job: pb.CronJob) -> Job:
    return Job(
        id=job.id if job.HasField("id") else None,
        description=job.description if job.HasField("description") else None,
        frequency=job_frequency_from_pb(job.frequency) if job.HasField("frequency") else None,
        created=_from_timestamp(job.created),
        updated=_from_timestamp(job.updated) if job.HasField("updated") else None,
        last_execution_dt=(
            _from_timestamp(job.last_execution_dt)
            if job.HasField("last_execution_dt")
            else None
        ),
        next_execution_dt=_from_timestamp(job.next_execution_dt),
        enabled=job.enabled,
        job_type=job_type_from_pb(job.job_type),
        job_status=_JOB_STATUS_TO_MODEL[
            pb.CronJobStatus.Name(job.job_status)
        ],
        configuration=configuration_from_pb(job.configuration),
        curr_retries=job.curr_retries,
    )


def job_execution_result_from_pb(
    result: pb.CronJobExecutionResult,
) -> JobExecutionResult:
    return JobExecutionResult(
        job_id=result.job_id,
        date_time=_from_timestamp(result.date_time),
        detail=result.detail,
        is_success=result.is_success,
        namespace=result.namespace,
    )
