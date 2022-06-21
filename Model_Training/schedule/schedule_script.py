from pytz import timezone
from datetime import datetime
import schedule
import time
from script import sayHello


def main():
    time_format = '%Y-%m%d %H:%M:%S %Z%z'
    # switch to current time zone
    default_now = datetime.now()
    formatted_now = datetime.now().strftime(time_format)


    schedule.every(2).seconds.do(sayHello)

    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__=="__main__":
    main()