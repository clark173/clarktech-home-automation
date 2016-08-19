#!/usr/local/lib/python2.7/dist-packages

#########################################################################
# This script takes input from the user via the Apache webserver on the #
# pi including the hour, minute and day(s) he/she desires to set the    #
# alarm. The script creates a new crontab job to schedule the alarm for #
# the desired time. The input command is all in a string format.        #
#                                                                       #
# NOTE!!! Must be called in the following format:                       #
# python change_alarm.py [hour] [minute] [day(s)]                       #
#########################################################################


from crontab import CronTab
import sys
import os
import time


INPUT_ERROR = 4
LOG = 'logs/change_alarm_log.txt'
PATH = 'sudo python /home/pi/Alarm/alarm_main.py'


def print_usage():
    print 'usage: ./change_alarm.py hour minute day(s)'
    print '    day(s) should be seperated by comma with no spaces'

def open_log_file():
    try:
        f = open(LOG, 'a')
    except IOError:
        if not os.path.isdir('logs'):
            os.makedirs('logs')
        f = open(LOG, 'w')

    return f

def check_inputs(f):
    f.write('----------------------------------------\n')
    f.write('[%s - %s] Starting change_alarm sequence...\n'\
            % (time.strftime('%s/%s/%Y'), time.strftime('%H:%M:%s')))

    if len(sys.argv) != 4:
        f.write('Error: Invalid number of input arguments')
        f.write('Found: %s Need 4' % (len(sys.argv)))
        f.write('Exiting script...\n')
        print_usage()
        sys.exit(INPUT_ERROR)

    f.write('Input Parameters: %s %s %s\n' % (sys.argv[1], sys.argv[2],
                                              sys.argv[3]))

def parse_arguments():
    hour = sys.argv[1]
    minute = sys.argv[2]
    day = map(int, sys.argv[3].split(','))
    return hour, minute, day

def set_cronjob(hour, minute, day):
    cron = CronTab(user = 'pi')
    job = cron.new(command = PATH)

    job.minute.on(minute)
    job.hour.on(hour)
    job.dow.on(*daylist)
    job.enable()

    cron.write()

def main():
    f = open_log_file()
    check_inputs(f)
    hour, minute, day = parse_arguments()
    f.write('Job added successfully\n')


if __name__ == "__main__":
    main()
