import random

from datetime import datetime, timedelta


def random_dd_mm_yyy(start_date, end_date: tuple[int, int, int] = None):
    if end_date is None:
        end_date = datetime.today()
    else:
        if len(end_date) == 3:
            end_date = datetime(year=end_date[2], month=end_date[1], day=end_date[0])
        else:
            raise ValueError
    start_date = datetime(year=start_date[2], month=start_date[1], day=start_date[0])
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    dd = int(str(random_date.strftime("%d")))
    mm = int(str(random_date.strftime("%m")))
    yyyy = int(str(random_date.strftime("%Y")))
    return dd, mm, yyyy
