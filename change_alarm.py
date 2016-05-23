#!/usr/local/lib/python2.7/dist-packages

#########################################################################
# This script takes input from the user via the Apache webserver on the #
# pi including the hour, minute and day(s) he/she desires to set the    #
# alarm. The script creates a new crontab job to schedule the alarm for #
# the desired time. The input command is all in a string format.        #
#                                                                       #
# NOTE!!! Must be called in the following format:                       #
# python change_alarm.py "[hour] [minute] [day(s)]"                     #
#########################################################################

path = 'sudo python /home/pi/Alarm/alarm_main.py'
log = 'logs/change_alarm_log.txt'

from crontab import CronTab
import sys
import os
import time

f = open(log, 'a')
f.write("----------------------------------------\n")
f.write("[" + time.strftime("%m/%d/%Y") + " - " + time.strftime("%H:%M:%S") + "] Starting change_alarm sequence...\n")

# Make sure there are only 4 inputs, the script and the string
if (len(sys.argv) != 4):
    f.write("Error: Invalid number of input arguments.\n")
    f.write("Found: " + str(len(sys.argv)) + " Need 4\n")
    f.write("Exiting script...\n")
    sys.exit(4)

f.write("Input Parameters: " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + "\n")

# Retrieve the input from the webserver
inp_string = sys.argv[1]

# Retrieve the inputs from the user
hour_in = sys.argv[1]
minute_in = sys.argv[2]
day = sys.argv[3]
daylist = day.split(',')
daylist = map(int, daylist)

# Get the current cron file from the user
cron = CronTab(user='pi')
job = cron.new(command=path)

# Add the user's input to a new job
job.minute.on(minute_in)
job.hour.on(hour_in)
job.dow.on(*daylist)
job.enable()

# Write the job to the end of the crontab file
cron.write()

f.write("Job added successfully!\n")
sys.exit(0)
