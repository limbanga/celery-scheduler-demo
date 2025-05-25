# Guide: Using Celery with Periodic Tasks

## 1. Purpose

* Create a task that runs every 30 seconds
* Print a greeting message to the terminal
* Use Celery with Redis as the message broker
* Use Celery Beat to schedule periodic tasks

---

## 2. Requirements

* Python (>=3.6)
* Redis server (latest version)
* Install the required Python libraries:

```bash
pip install celery redis
```

* Ensure Redis is running (on `localhost:6379` or adjust as needed)

---

## 3. `tasks.py` File

The content of the `tasks.py` file:

```python
from celery import Celery
from datetime import datetime

app = Celery('tasks', broker='redis://localhost:6379/0')

# Configure Celery Beat to use persistent scheduler
app.conf.beat_scheduler = 'celery.beat.PersistentScheduler'

# Define the periodic task schedule: run every 30 seconds
app.conf.beat_schedule = {
    'print-greeting-every-30-seconds': {
        'task': 'tasks.print_greeting',
        'schedule': 30.0,  # in seconds
    },
}

@app.task
def print_greeting():
    print(f"At {datetime.now()}, wishing you a peaceful, beautiful night full of good luck!")
```

---

## 4. How to Run

### 4.1 Start Redis server

If Redis is not already running, start it by running:

```bash
redis-server
```

### 4.2 In one terminal, run the Celery worker:

```bash
celery -A tasks worker --loglevel=info
```

### 4.3 In another terminal, run Celery Beat:

```bash
celery -A tasks beat --loglevel=info
```

---

## 5. Explanation

* **Worker**: Fetches and executes tasks from the message queue (Redis)
* **Beat**: Responsible for scheduling the periodic tasks based on the `beat_schedule`
* Every 30 seconds, the worker will execute the `print_greeting` task and print the message to the terminal where the worker is running.

---

## 6. Notes

* The first task execution will occur after 30 seconds.
* A file named `celerybeat-schedule` will be created in the current directory to persist the schedule (you don't need to commit this file to Git).
* If you want the task to run immediately once, you can trigger it manually like this:

```python
from tasks import print_greeting
print_greeting.delay()
```

* Or, you can create a separate script to run the task once before starting the worker and beat.

---

## 7. Extensions

* You can define additional tasks with different time intervals in the `app.conf.beat_schedule`.
* You can use `crontab` for more complex schedules (e.g., run at 10 PM every day).
* You can switch the broker from Redis to RabbitMQ or others if needed.

---

## 8. References

* Celery official docs: [https://docs.celeryproject.org/en/stable/](https://docs.celeryproject.org/en/stable/)
* Celery Beat documentation: [https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)
* Redis: [https://redis.io/](https://redis.io/)
