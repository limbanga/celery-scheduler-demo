# Hướng dẫn sử dụng Celery với task định kỳ 

## 1. Mục đích

* Tạo một task chạy định kỳ mỗi 30 giây
* In lời chúc lên màn hình terminal
* Sử dụng Celery với Redis làm message broker
* Sử dụng Celery Beat để lên lịch chạy task định kỳ

---

## 2. Môi trường chuẩn bị

* Python (>=3.6)
* Redis server (phiên bản mới nhất)
* Cài đặt thư viện Python:

```bash
pip install celery redis
```

* Redis server phải đang chạy (ở localhost:6379 hoặc thay đổi phù hợp)

---

## 3. File `tasks.py`

Nội dung file `tasks.py` như sau:

```python
from celery import Celery
from datetime import datetime

app = Celery('tasks', broker='redis://localhost:6379/0')

# Cấu hình Celery Beat để dùng bộ lập lịch dạng persistent (lưu trạng thái)
app.conf.beat_scheduler = 'celery.beat.PersistentScheduler'

# Định nghĩa lịch chạy task: mỗi 30 giây chạy một lần task 'print_greeting'
app.conf.beat_schedule = {
    'print-greeting-every-30-seconds': {
        'task': 'tasks.print_greeting',
        'schedule': 30.0,  # đơn vị: giây
    },
}

@app.task
def print_greeting():
    print(f"At {datetime.now()}, chúc bạn một buổi tối thật đẹp, an lành và nhiều điều may mắn!")
```

---

## 4. Cách chạy

### 4.1 Khởi động Redis server

Nếu chưa chạy Redis, mở terminal và chạy:

```bash
redis-server
```

### 4.2 Mở terminal chạy worker Celery

```bash
celery -A tasks worker --loglevel=info
```

### 4.3 Mở terminal khác chạy Celery Beat

```bash
celery -A tasks beat --loglevel=info
```

---

## 5. Giải thích

* **Worker**: sẽ nhận và thực thi các task từ hàng đợi (queue) của broker Redis
* **Beat**: chịu trách nhiệm lập lịch chạy task định kỳ theo cấu hình `beat_schedule`
* Lúc này, cứ mỗi 30 giây, worker sẽ chạy task `print_greeting` và in lời chúc ra màn hình terminal nơi worker đang chạy.

---

## 6. Lưu ý

* Lần đầu tiên Celery Beat sẽ đợi đủ 30 giây mới chạy task lần đầu.
* File `celerybeat-schedule` sẽ được tạo ra trong thư mục hiện hành để lưu trạng thái lịch trình (không cần commit file này vào git).
* Muốn chạy task ngay khi khởi động, bạn có thể gọi thủ công task bằng cách chạy:

```python
from tasks import print_greeting
print_greeting.delay()
```

* Hoặc tạo script gọi task 1 lần trước khi chạy worker & beat.

---

## 7. Mở rộng

* Bạn có thể thêm nhiều task khác với các khoảng thời gian khác nhau trong `app.conf.beat_schedule`.
* Có thể sử dụng `crontab` schedule cho lịch chạy phức tạp (ví dụ chạy lúc 22h mỗi ngày).
* Thay broker Redis bằng RabbitMQ hoặc các broker khác nếu muốn.

---

## 8. Tài liệu tham khảo

* Celery official docs: [https://docs.celeryproject.org/en/stable/](https://docs.celeryproject.org/en/stable/)
* Celery Beat: [https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)
* Redis: [https://redis.io/](https://redis.io/)
