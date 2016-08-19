#!/usr/local/lib/python2.7/dist-packages

#########################################################
# This script retreives the alarms currently scheduled. #
# Output is displayed in an easy-to-read format that    #
# is printed on the command line and returned to the    #
# calling function.                                     #
#########################################################


from crontab import CronTab
import sys
import os
import time
import datetime


DAY_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
               "Saturday", "Sunday"]
FILENAME = "logs/delete_alarm_log.txt"
USAGE_ERROR = 1


def open_file():
    try:
        f = open(FILENAME, 'a')
    except IOError:
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        f = open(FILENAME, 'w')

    return f

def print_usage():
    print 'usage: ./delete_alarm.py "HH:MM<AM/PM>" day(s)'

def check_arguments(f):
    f.write('----------------------------------------\n')
    f.write('[%s - %s] Starting delete_alarm script...\n'\
            % (time.strftime('%H:%M:%S'), time.strftime('%m/%d/%Y')))

    if len(sys.argv) < 3:
        f.write('Invalid number of arguments\n')
        f.write('Expected: >2 Received: %s\n' % (len(sys.argv)))
        f.write('Exiting script...\n')
        print_usage()
        sys.exit(USAGE_ERROR)

def get_days(days, hour, minute):
    daylist = []
    day_written = False
    output = ''

    if days.strip() == 'Once':
        today = datetime.datetime.today()
        now = datetime.datetime.now()
        weekday = int(datetime.datetime.today().weekday())
        input_time = datetime.datetime(today.year, today.month, today.day,
                                       int(hour), int(minute))

        if input_time > now:
            daylist = [weekday + 1]
        else:
            daylist = [weekday + 2]
    elif days.strip() == 'Weekends':
        daylist = [0, 6]
    elif days.strip() == 'Weekdays':
        daylist = [1, 2, 3, 4, 5]
    elif days.strip() == 'Daily':
        daylist = [0, 1, 2, 3, 4, 5, 6]
    else:
        day_written = True
        days = days.split(',')

        for i in range(1, len(days)):
            if days[i] in DAY_OF_WEEK:
                output += '%s ' % (DAY_OF_WEEK.index(days[i]))
                daylist.append(DAY_OF_WEEK.index(days[i]))

    if not day_written:
        output = days

    return output.rstrip(), daylist

def get_arguments(f):
    days = ''
    hour = sys.argv[1].split(':')[0]
    minute = sys.argv[1].split(':')[1][0:2]
    ampm = sys.argv[1].split(':')[1][2:]

    for i in range(2, len(sys.argv)):
        days += '%s ' % (sys.argv[i])

    if ampm.lower() == 'pm' and hour != '12':
        hour = str(int(hour) + 12)

    f.write('Selected hour is: %s\n' % (hour))
    f.write('Selected minute is: %s\n' % (minute))

    days, daylist = get_days(days, hour, minute)

    f.write('Selected days are: %s\n' % (days))

    return daylist, hour, minute

def delete_job(f, daylist, hour, minute):
    cron = CronTab(user = 'cbt')
    match = False

    for existing_job in cron:
        if len(str(existing_job.minute)) < 3 and len(str(existing_job.hour)) < 3 and str(existing_job.hour) != '*':
            if int(str(existing_job.minute)) == int(minute) and int(str(existing_job.hour)) == int(hour) and list(existing_job.dow) == daylist:
                cron.remove(existing_job)
                f.write('Alarm removed successfully\n')

    cron.write()

    if not match:
        f.write('No match found\n')

    f.write('Exiting script...\n')

def main():
    f = open_file()
    check_arguments(f)
    daylist, hour, minute = get_arguments(f)
    delete_job(f, daylist, hour, minute)

if __name__ == "__main__":
    main()
