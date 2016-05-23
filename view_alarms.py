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

curhour = time.strftime("%H")
curmin = time.strftime("%M")
today = datetime.datetime.now()
dow = today.strftime("%w")
tomorrow = int(dow) + 1

dayofweek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

cron = CronTab(user="pi")
set_alarms_am = []
set_alarms_pm = []

for job in cron:
    job_string = str(job)

    # Eliminate any jobs that are commented out and hence not active
    if (job_string[0] is not "#") and (str(job[4]) is not "*"):
        minute = str(job[0])
        hour = str(job[1])
        ampm = "AM"        

        if int(hour) > 12:
            hour = str(int(hour) - 12)
            ampm = "PM"
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

        # Get the final output for the alarms that are set
        alarmout = hour + ":" + minute + ampm

        if str(job.comment) == 'Once':
            alarmout += " Once"
        elif day_ints == [1,2,3,4,5]:
            alarmout += " Weekdays"
        elif day_ints == [0,6]:
            alarmout += " Weekends"
        elif day_ints == [0,1,2,3,4,5,6]:
            alarmout += " Daily"
        else:
            lcv = 0
            for day in day_ints:
                lcv += 1
                if lcv < len(day_ints):
                    alarmout += " " + dayofweek[day]
                else:
                    if len(day_ints) > 1:
                        alarmout += " and "
                    alarmout += " " + dayofweek[day]

        if ampm == "PM":        
            set_alarms_pm.append(alarmout)
        else:
            set_alarms_am.append(alarmout)

set_alarms_am.sort()
set_alarms_pm.sort()

for alarm in set_alarms_am:
    print(alarm)

for alarm in set_alarms_pm:
    print(alarm)
