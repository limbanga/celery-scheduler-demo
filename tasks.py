from celery import Celery
from datetime import datetime

app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.beat_scheduler = 'celery.beat.PersistentScheduler'
app.conf.beat_schedule = {
    'print-greeting-every-30-seconds': {
        'task': 'tasks.print_greeting',
        'schedule': 30.0,  # chạy mỗi 30 giây
    },
}

@app.task
def print_greeting():
    print(f"At {datetime.now()}, chúc bạn một buổi tối thật đẹp, an lành và nhiều điều may mắn!")
