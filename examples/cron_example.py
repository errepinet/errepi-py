"""
Examples of using the CronConfigurator class to interact with the Errepi Net
Cron microservice over gRPC (CronBridgeService).
"""

from errepi.cron import (
    CronConfigurator,
    http_job_type,
)

from errepi.cron.models import (
    JobFrequencyMinute,
    JobHttpMethod,
    JobFrequency,
    JobBodyType,
    JobCreateUpdate,
    CronConfiguration,
    CronClientConfiguration,
    HTTPJob,
    RefCreateUpdate,
)

import json
from datetime import datetime, timedelta, timezone

# Instantiate with a connection configuration (host and port) or use the default
cron = CronConfigurator(CronClientConfiguration(host="localhost", port=50051))

tenant_id = "my-tenant"
namespace = "default"

# 1. Get application info
info = cron.app_info()
print("App info:", info)

# 2. Set a configuration
config_set = CronConfiguration(job_max_retries=3, job_retry_delay_secs=60)
config_entry = cron.set_configuration(tenant_id, namespace, "main", config_set)
print("Set configuration:", config_entry)

# 3. Get a configuration
config = cron.get_configuration(tenant_id, namespace, "main")
print("Get configuration:", config)

# 4. Unset a configuration
cron.unset_configuration(tenant_id, namespace, "main")
print("Configuration unset.")

job_type = http_job_type(
    HTTPJob(
        body=json.dumps({"key": "test"}),
        body_type=JobBodyType.Json,
        headers={"Authorization": "Bearer token"},
        method=JobHttpMethod.POST,
        url="https://example.com/api",
    )
)


# 5. Create a job
job_create = JobCreateUpdate(
    description="Test job",
    enabled=True,
    frequency=None,
    job_type=job_type,  # Replace with a valid JobType instance as needed
    next_execution_dt=datetime.now(timezone.utc) + timedelta(hours=1),  # Use ALWAYS UTC
)

job = cron.create_job(tenant_id, namespace, job_create)
print("Created job:", job)

# 6. List jobs
jobs = cron.list_jobs(tenant_id, namespace)
print("Jobs:", jobs)

# 7. Update a job (requires a valid job_id)
job_id: str = job.id

job_update = JobCreateUpdate(
    description="Test job updated",
    enabled=True,
    frequency=JobFrequency(JobFrequencyMinute(Minute=5)),
    job_type=job_type,  # Replace with a valid JobType instance as needed
    next_execution_dt=datetime.now(timezone.utc)
    + timedelta(hours=2),  # Use *ALWAYS* UTC
)

updated_job = cron.update_job(tenant_id, namespace, job_id, job_update)
print("Updated job:", updated_job)

# 8. Get a single job (requires a valid job_id)
single = cron.get_job(tenant_id, namespace, job_id)
print("Single job:", single)

# 9. Get job execution results (requires a valid job_id)
results = cron.job_results(tenant_id, namespace, job_id)
print("Job execution results:", results)

# 10. Delete a job (requires a valid job_id)
cron.delete_job(tenant_id, namespace, job_id)
print("Job deleted.")

# 11. Set a reference
ref = RefCreateUpdate(value="my_value")
set_ref = cron.set_ref(tenant_id, namespace, "myref", ref)
print("Set ref:", set_ref)

# 12. Get a reference
got_ref = cron.get_ref(tenant_id, namespace, "myref")
print("Got ref:", got_ref)

# 13. Unset a reference
cron.unset_ref(tenant_id, namespace, "myref")
print("Reference unset.")
