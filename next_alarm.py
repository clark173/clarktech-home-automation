#!/usr/local/lib/python2.7/dist-packages

#########################################################
# This script retreives the alarms currently scheduled. #
# Output is displayed in an easy-to-read format that    #
# is printed on the command line and returned to the    #
# calling function.                                     #
#########################################################


from crontab import CronTab
import datetime
import time
import re
import sys


DAY_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
               "Saturday", "Sunday"]

curhour = time.strftime("%H")
curmin = time.strftime("%M")
today = datetime.datetime.now()
dow = today.strftime("%w")
tomorrow = (int(dow) + 1) % 7
ampm = "AM"

cron = CronTab(user="pi")
next_alarms = []

for job in cron:
    job_string = str(job)

    # Eliminate any jobs that are commented out and hence not active
    if (job_string[0] is not "#") and (str(job[4]) is not "*"):
        minute = str(job[0])
        hour = str(job[1])
        newhour = hour

        if int(hour) > 12:
            ampm = "PM"
            newhour = int(hour) - 12
            newhour = str(newhour)
        elif int(hour) == 12:
            ampm = "PM"

        # Pad zero's as necessary
        if (len(minute) == 1):
            minute = "0" + minute

        # Get the days that the alarm is set for
        days = job[4]
        days_string = str(days)
        day_vals = days_string.split(',')

        # Change any days in a range to individual values
        ind = 0
        for item in day_vals:
            if (len(item) > 1):
                first = int(item[0])
                last = int(item[2])
                day_vals[ind] = item[0]

                for val in range(first + 1, last + 1):
                    day_vals.append(str(val))

            ind += 1

        day_ints = map(int, day_vals)

        min_day = 7

        # Generate a list of the next alarms for every job
        for val in day_ints:
            if val >= int(dow):
                if val == int(dow) and (int(hour) > int(curhour) or (int(hour) == int(curhour) and int(minute) > int(curmin))):
                    min_day = val
                elif val > int(dow) and min_day > val:
                    min_day = val

        # If min_day is 7, there are no more alarms set during this week, so wrap to the next week
        if min_day == 7:
            for val in day_ints:
                if val < min_day and (int(hour) > int(curhour) or (int(hour) == int(curhour) and int(minute) > int(curmin))):
                    min_day = val

        next_alarm = "{} {}:{}{}".format(min_day, newhour, minute, ampm)
        next_alarms.append(next_alarm)

if len(next_alarms) == 0:
    print("No alarms set")
    sys.exit(0)

next_day = int(min(next_alarms)[0])
next_time = min(next_alarms)[2:]
hour_list = re.findall("\d+:", next_time)
next_hour = hour_list[0][:-1]
next_ampm = next_time[-2:]

if next_day == int(tomorrow):
    next_day = "Tomorrow"
elif next_day == int(dow):
    if int(next_hour) >= 6 and next_ampm == "PM":
        next_day = "Tonight"
    else:
        next_day = "Today"
else:
    next_day = dayofweek[next_day]

print("{} at {}".format(next_day, next_time))
