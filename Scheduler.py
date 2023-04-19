from apscheduler.schedulers.background import BackgroundScheduler

def test():
    print("test")

def set_scheduler(time_period: int, timer_enabled: bool):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=test, minute="0-59")
    scheduler.start()

set_scheduler(1, True)

pass