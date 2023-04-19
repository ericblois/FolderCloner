from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from Cloner import clone_dirs
from typing import Callable

def test():
    print("test")

last_run = 0

def update_last_run(time: int):
    global last_run
    last_run = time

def __scheduled_func(sources: list[str], dest: str, update_func: Callable):
    #clone_dirs(sources, dest)
    test()
    update_func(int(time.mktime(datetime.now().timetuple())))

__scheduler = BackgroundScheduler()

def start_scheduler(time_period: int, run_now: bool, sources: list[str], dest: str, update_func: Callable):
    if __scheduler.running:
        stop_scheduler()
    global last_run
    if run_now:
        __scheduled_func(sources, dest, update_func)
    #__scheduler.add_job(func=test, trigger="cron", second="0-59", id="test")
    if time_period == 0:
        dt = datetime.now()
        weekday = dt.weekday()
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest, update_func), trigger="cron", day_of_week=f"{weekday}", id="test")
    elif time_period == 1:
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest, update_func), trigger="cron", day="1-31", id="test")
    elif time_period == 2:
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest, update_func), trigger="cron", hour="0-23", id="test")
    elif time_period == 3:
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest, update_func), trigger="cron", minute="0-59", id="test")
    __scheduler.start()

def stop_scheduler():
    __scheduler.shutdown(True)
    __scheduler.remove_all_jobs()

'''start_scheduler(0, True, [], "")

pass

stop_scheduler()

pass'''