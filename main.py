firstprint = '''

 _______  _______  _______  _______  ___  _______  __    _  _______  _______  __   __  ___  ___
|       ||       ||   _   ||       ||   ||       ||  |  | ||       ||       ||  | |  ||   ||   |
|  _____||_     _||  |_|  ||_     _||   ||   _   ||   |_| ||  _____||____   ||  | |  ||   ||   |
| |_____   |   |  |       |  |   |  |   ||  | |  ||       || |_____  ____|  ||  |_|  ||   ||   |
|_____  |  |   |  |       |  |   |  |   ||  |_|  ||  _    ||_____  || ______||       ||   ||   |___
 _____| |  |   |  |   _   |  |   |  |   ||       || | |   | _____| || |_____ |       ||   ||       |
|_______|  |___|  |__| |__|  |___|  |___||_______||_|  |__||_______||_______||_______||___||_______|

This project was assigned by Hogeschool Utrecht. All code has been written by Joriam van Slooten unless specifially stated otherwise.
Spreading this code without permission is not allowed.

Email: joriam.vanslooten@student.hu.nl
Github:https://github.com/JoriamVS/Stationszuil
'''

import random
import csv
from datetime import datetime
import mysql.connector
import os
import shutil
import openweather
random.seed()


def startupCLI():

    print(firstprint)
    print("\n")


def userOrMod():
    while True:
        questionPrompt = input("Are you a user or a moderator? (USER/MOD): ")
        questionPrompt = questionPrompt.upper()
        if questionPrompt == 'USER' or questionPrompt == 'MOD':
            if questionPrompt == 'USER':
                return 1  # 1 is User
            elif questionPrompt == 'MOD':
                return 2  # 2 is Moderator
        else:
            print("Please enter a valid answer (USER/MOD)\n")
            continue


def userFunctions():
    while True:
        newMessagePrompt = input("Do you want to enter a new message? (YES/NO): ")
        newMessagePrompt = newMessagePrompt.upper()
        if newMessagePrompt == 'YES' or newMessagePrompt == 'NO':
            if newMessagePrompt == 'YES':
                message = userInput()
                parseData(message)
                continue
            elif newMessagePrompt == 'NO':
                break
        else:
            print("Please enter a valid answer (YES/NO)\n")
            continue


def moderatorFunctions():
    modName = input('Please enter your moderator name: ')
    modMail = input('Please enter your moderator mail: ')
    while True:
        moderatePrompt = input("Do you want to validate a new message? (YES/NO): ")
        moderatePrompt = moderatePrompt.upper()
        if moderatePrompt == 'YES' or moderatePrompt == 'NO':
            if moderatePrompt == 'YES':
                moderateMessage(modName, modMail)
                continue
            elif moderatePrompt == 'NO':
                break
        else:
            print("Please enter a valid answer (YES/NO)\n")
            continue


def userInput():
    try:
        userName = input("Enter your name. In the case this field stays empty you will be anonymous: ")

        if userName is "":
            userName = "Anoniem"
        userMessage = input("Enter your message. The message can not contain more than 140 characters: ")

        if len(userMessage) > 140:
            print("Your message was too long, please try again.\n")
            userMessage = input("Enter your message. The message can not contain more than 140 characters: ")

        userInputList = [userMessage, userName]
        return userInputList
    except Exception as e:
        print(f"An error has occured: {e}, please try again.")


def parseData(userList):

    try:
        stationList = ["Amersfoort", "Utrecht", "'S-Hertogenbosch"]
        randStation = stationList[random.randint(0, 2)]

        currentDateTime = datetime.now()
        msgDate = currentDateTime.strftime("%Y-%m-%d")
        msgTime = currentDateTime.strftime("%H:%M:%S")
        filename = currentDateTime.strftime("%d%m%Y_%H%M%S")

        # Write to csv file
        with open(f'messages/{filename}.csv', 'w', newline='') as myFile:

            columns = ["Message", "Date", 'Time', "Username", "Station"]
            rows = [userList[0], msgDate, msgTime, userList[1], randStation]  # Message, Date and time, Username, Random train station

            writer = csv.writer(myFile)
            writer.writerow(columns)
            writer.writerow(rows)
            print("\n")
    except Exception as e:
        print(f"An error has occured: {e}, please try again.")


def getOldestFile():
    list_files = os.listdir('messages')

    for i in range(len(list_files)):
        list_files[i] = f'messages/{list_files[i]}'

    oldest_file = min(list_files, key=os.path.getctime)
    return oldest_file


def moderateMessage(modName, modMail):
    to_moderate = getOldestFile()
    plainMessage = ''

    with open(to_moderate, 'r', newline='') as file:
        csvRead = csv.DictReader(file)
        for row in csvRead:
            plainMessage = row['Message']
    print(f'\nThe message to approve:\n{plainMessage}\n')

    while True:
        getApproval = input("Do you want to approve this message? (YES/NO): ")
        getApproval = getApproval.upper()

        if getApproval == 'YES' or getApproval == 'NO':
            break
        else:
            print("Please enter a valid answer (YES/NO)\n")
            continue

    currentDateTime = datetime.now()
    approveTime = currentDateTime.strftime("%H:%M")
    approveDate = currentDateTime.strftime("%Y-%m/%d")
    writeDatabase(to_moderate, getApproval, approveTime, approveDate, modName, modMail)




def writeDatabase(file, approval, approveTime, approveDate, modName, modMail):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",  # Very safe I know
        database="stationszuil"
    )

    with open(file) as f:
        csvReader = csv.DictReader(f)
        for row in csvReader:
            csvMessage = row['Message']
            csvDate = row['Date']
            csvTime = row['Time']
            csvUsername = row['Username']
            csvStation = row['Station']
    myCursor = mydb.cursor()
    sql = 'INSERT INTO bericht VALUES (default, %s, %s, %s, %s, %s, ' \
          '%s, %s, %s, %s, %s)'

    myValues = (csvMessage, csvDate, csvTime, csvUsername, csvStation, approval, approveDate, approveTime, modName, modMail)
    myCursor.execute(sql, myValues)
    mydb.commit()
    moderated = file.split('/')
    shutil.move(file, f'mod_messages/{moderated[1]}')


startupCLI()

getMode = userOrMod()
if getMode == 1:
    userFunctions()
elif getMode == 2:
    moderatorFunctions()


a = openweather.getWeather('utrecht')