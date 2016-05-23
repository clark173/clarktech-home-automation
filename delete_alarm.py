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

dayofweek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
filename = "logs/delete_alarm_log.txt"
cron = CronTab(user="pi")
path = 'sudo python /home/pi/Alarm/alarm_main.py'

f = open(filename, 'a')
timeofday = time.strftime("%H:%M:%S")
date = time.strftime("%m/%d/%Y")

f.write("----------------------------------------\n")
f.write("[" + date + " - " + timeofday + "] Starting delete_alarm script...\n")

# Check the number of input arguments
if (len(sys.argv) < 3 ):
    f.write("Invalid number of arguments\n")
    f.write("Expected: >2 Received: " + str(len(sys.argv)))
    f.write("\nExiting script...\n")
    print("Usage: python delete_alarm.py \"time\" \"day(s)\"")
    sys.exit(1)

packet = sys.argv[1]

current_hour = time.strftime("%H")
current_min = time.strftime("%M")

for i in range(2, len(sys.argv)):
    packet += " " +  sys.argv[i]

data = packet.split(":")
hour = data[0]
data = data[1].split(" ")
minute = data[0][0:2]
ampm = data[0][2:]

if ampm == "PM" and hour != "12":
    hour = str(int(hour) + 12)

f.write("Selected hour is: " + hour)
f.write(" Selected minute is: " + minute)
f.write("\nSelected days are: ")

daylist = []

day = int(datetime.datetime.today().weekday())

if data[1] == "Once":
    if (int(hour) > int(current_hour) or ((int(hour) == int(current_hour)) and (int(minute) > (int(current_minute))))):
        daylist = [day + 1]
    else:
        daylist = [day + 2]
elif data[1] == "Weekends":
    daylist = [0,6]
elif data[1] == "Weekdays":
    daylist = [1,2,3,4,5]
elif data[1] == "Daily":
    daylist = [0,1,2,3,4,5,6]
else:
    for i in range(1,len(data)):
        f.write(data[i] + " ")
        if (data[i] in dayofweek):
            daylist.append(dayofweek.index(data[i]))

f.write("\n")

cron = CronTab(user='pi')
match = False

for existing_job in cron:
    if len(str(existing_job.minute)) < 3 and len(str(existing_job.hour)) < 3 and str(existing_job.hour) != '*':
        if (int(str(existing_job.minute)) == int(minute) and int(str(existing_job.hour)) == int(hour) and list(existing_job.dow) == daylist):
            cron.remove(existing_job)
            f.write("Alarm removed successfully.\n")
            match = True

cron.write()

if (match is False):
    f.write("No match found.\n")

f.write("Exiting script...\n")
