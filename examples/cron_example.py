"""
Examples of using the CronConfigurator class to interact with the Errepi Net Cron microservice API.
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
    ConfigurationEntrySet,
    HTTPJob,
    RefCreateUpdate,
)

import json
from datetime import datetime, timedelta, timezone

# Instantiate from environment variable or default
cron = CronConfigurator.from_env()

# 1. Get application info
info = cron.app_info()
print("App info:", info)

# 2. Set a configuration
config_set = ConfigurationEntrySet(job_max_retries=3, job_retry_delay_secs=60)
config_entry = cron.set_configuration("default", "main", config_set)
print("Set configuration:", config_entry)

# 3. Get a configuration
config = cron.get_configuration("default", "main")
print("Get configuration:", config)

# 4. Unset a configuration
cron.unset_configuration("default", "main")
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

job = cron.create_job("default", job_create)
print("Created job:", job)

# 6. List jobs
jobs = cron.list_jobs("default")
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

updated_job = cron.update_job("default", job_id, job_update)
print("Updated job:", updated_job)

# 8. Get a single job (requires a valid job_id)
single = cron.single_job(job_id)
print("Single job:", single)

# 9. Get job execution results (requires a valid job_id)
results = cron.single_job_execution_results(job_id)
print("Job execution results:", results)

# 10. Delete a job (requires a valid job_id)
cron.delete_job("default", job_id)
print("Job deleted.")

# 11. Set a reference
ref = RefCreateUpdate(value="my_value")
set_ref = cron.set_ref("default", "myref", ref)
print("Set ref:", set_ref)

# 12. Get a reference
got_ref = cron.get_ref("default", "myref")
print("Got ref:", got_ref)

# 13. Unset a reference
cron.unset_ref("default", "myref")
print("Reference unset.")
