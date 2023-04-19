from apscheduler.schedulers.background import BackgroundScheduler

def set_scheduler(time_period: int, timer_enabled: bool):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print, trigger='interval', seconds=3)
    scheduler.start()

set_scheduler(1, True)