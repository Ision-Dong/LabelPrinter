import datetime
import time


def adjust_time(date, timezone):
    t = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(t))
    dt = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)
    dt8 = dt.astimezone(datetime.timezone(datetime.timedelta(hours=timezone)))
    date = dt8.strftime("%Y-%m-%d %H:%M:%S")

    return date


