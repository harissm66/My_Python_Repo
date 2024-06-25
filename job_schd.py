import schedule
import time
import random

# Sample job 1: Print a message every minute
def job1():
    print("Job 1 is running...")

# Sample job 2: Generate a random number every 5 seconds
def job2():
    print(f"Job 2 is running... Random number: {random.randint(1, 100)}")

# Sample job 3: Simulate a data processing task every 10 seconds
def job3():
    print("Job 3 is running... Simulating data processing...")
    # Simulate processing time
    time.sleep(2)
    print("Data processing complete.")

# Schedule the jobs
schedule.every().minute.do(job1)
schedule.every(5).seconds.do(job2)
schedule.every(10).seconds.do(job3)

# Function to keep the script running
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduler
if __name__ == "__main__":
    run_scheduler()

