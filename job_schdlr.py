import schedule
import time
from importlib import import_module

# Import the job functions from the files
jobs = ["job1", "job2", "job3"]
for job_name in jobs:
    job_module = import_module(job_name)
    job_function = getattr(job_module, job_name)
    globals()[job_name] = job_function

# Schedule the jobs
schedule.every(3).seconds.do(job1)
schedule.every(6).seconds.do(job2)
schedule.every(7).seconds.do(job3)

# Function to keep the script running
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduler
if __name__ == "__main__":
    run_scheduler()

