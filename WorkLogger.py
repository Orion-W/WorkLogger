#!/usr/bin/env python3.11.5
"""
Created on Fri May 19 16:40:27 2023

@author: Orion Arthur Warawa
"""
import datetime
monthNum = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

def toDate(date):
    date1 = date.split(",")
    date2 = date1[1].split(" ")
    month = monthNum[date2[0]]
    return (int(date1[0]), month, int(date2[1]))

def assign_day_of_week(year, month, day):
    date = datetime.datetime(year, month, day)
    day_of_week = date.strftime("%A")
    return day_of_week

def totalCalculator (filename,companyName):
    file = open(filename,"r")
    lines = file.readlines()
    totalHours = 0
    totalMoney = 0
    for line in lines:
        if ("Total" not in line) and ("Date" not in line) and (companyName not in line):
            dayInfo = line.split("\t")
            dayInfo[2] = dayInfo[2].replace("\n","")
            dayInfo[2] = dayInfo[2].replace("$","")
            totalHours = totalHours + float(dayInfo[1])
            totalMoney = totalMoney + float(dayInfo[2])
    return [totalHours,totalMoney]

def hourFinder(startEnd):
    error = False
    morningStart = True
    afternoonEnd = True
    startStop = startEnd.split(" ")
    if "pm" in startStop[0]:
        morningStart = False
    if "am" in startStop[2]:
        afternoonEnd = False
    if morningStart:
        startStop[0] = startStop[0].replace("am","")
    else:
        startStop[0] = startStop[0].replace("pm","") 
    if afternoonEnd:
        startStop[2] = startStop[2].replace("pm","")
    else:
        startStop[2] = startStop[2].replace("am","")
    startTime = startStop[0].split(":")
    endTime = startStop[2].split(":")
    if morningStart:
        startHours = (int(startTime[0]) + (int(startTime[1])/60))
    else:
        startHours = 12 + (int(startTime[0]) + (int(startTime[1])/60))
    if afternoonEnd:
        endHours = 12 + (int(endTime[0]) + (int(endTime[1])/60))
    else:
        endHours = (int(endTime[0]) + (int(endTime[1])/60))
    if (startTime[0] == "12") and (morningStart):
        startHours = (int(startTime[1])/60)
    elif (startTime[0] == "12") and (not(morningStart)):
        startHours = (int(startTime[0]) + (int(startTime[1])/60))
    if (endTime[0] == "12") and afternoonEnd:
        endHours = (int(endTime[0]) + (int(endTime[1])/60))
    elif (endTime[0] == "12") and (not(afternoonEnd)):
        endHours = 12 + (int(endTime[0]) + (int(endTime[1])/60))
    hours = endHours - startHours
    return hours

exist = input("do you have a file?: (no/yes)\t")
filename = input("What is the name of your log file?:\t")
hourlyWage =""
overTime = ""
companyName = ""
if exist == "no":
    file = open(filename,"w")
    hourlyWage = input("what do you make per hour? (no $):\t")
    companyName = input("what is the name of your company?:\t")
    overTime = input("do you get over time? (no/yes):\t")
    file.write(companyName + "\tHourly Wage: $" + hourlyWage +"\t" + "Over Time?: " + overTime+"\n"+
               "Date\t\t\tTime\t\tHours\t$ Made\n")
else:
    file = open(filename,"r")
    firstLine = file.readline()
    companyInfo = firstLine.split("\t")
    companyName = companyInfo[0]
    hourlyWage = companyInfo[1]
    overTime = companyInfo[2]
    hourlyWage = hourlyWage.replace("Hourly Wage: ","")
    hourlyWage = hourlyWage.replace("$","")
    overTime = overTime.replace("Over Time?: ","")
    overTime = overTime.replace("\n","")
file = open(filename,"r+")
lines = file.readlines()
number = 0
for line in lines:
    if "Total" in line:
        number = len(line)
file.seek(0)
file.read()
file.seek(file.tell()-number)
file.truncate()
while True:
    date = input("What is the Date of your entry?:\t")
    startEnd = input("When did you start and end? (#:##am - #:##pm):\t")
    if (date == "stop") or (startEnd == "stop"):
        break
    hours = hourFinder(startEnd)
    daysMoney = hours*int(hourlyWage)
    file = open(filename,"a")
    date1 = toDate(date)
    dayOfWeek = assign_day_of_week(date1[0],date1[1],date1[2])
    file.write(date+", "+dayOfWeek+": "+startEnd+"\t"+str(round(hours,2))+"\t $"+str(round(daysMoney,2))+"\n")
file = open(filename,"a")
totals = totalCalculator(filename,companyName)
file.write("Total Hours: "+str(round(totals[0],2))+"\tTotal Money Earned: $"+str(round(totals[1],2)))
#make thing that tells how many days till next paycheck or if the data entered should be in the next paycheck
file.close()
