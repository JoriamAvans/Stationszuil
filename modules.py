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
                cli_moderateMessage(modName, modMail)
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

def rand_station():
    stationList = ["Amersfoort", "Utrecht", "Den Bosch"]
    randStation = random.choice(stationList)
    return randStation


def parseData(userList, station):

    try:
        randStation = station

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
    if len(list_files) == 0:
        return False
    for i in range(len(list_files)):
        list_files[i] = f'messages/{list_files[i]}'

    oldest_file = min(list_files, key=os.path.getctime)
    return oldest_file


def cli_moderateMessage(modName, modMail):
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


def gui_moderateMessage(file, modName, modMail, approval):
    print("Approval status: ", approval)
    currentDateTime = datetime.now()
    approveTime = currentDateTime.strftime("%H:%M")
    approveDate = currentDateTime.strftime("%Y-%m/%d")
    writeDatabase(file, approval, approveTime, approveDate, modName, modMail)


def writeDatabase(file, approval, approveTime, approveDate, modName, modMail):
    db_login = database_login()
    mydb = mysql.connector.connect(
        host=db_login[0],
        user=db_login[1],
        password=db_login[2],
        database=db_login[3]
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
    mydb.close()
    myCursor.close()


def readDatabaseStation(service, city):
    db_login = database_login()
    mydb = mysql.connector.connect(
        host=db_login[0],
        user=db_login[1],
        password=db_login[2],
        database=db_login[3]
    )

    myCursor = mydb.cursor(buffered=True)
    sql = f'SELECT {service} FROM station_service WHERE station_city = %s'
    myValues = (city, )
    myCursor.execute(sql, myValues)

    mydb.commit()
    records = myCursor.fetchall()

    mydb.close()
    myCursor.close()

    return records


def getMessages():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",  # Very safe I know
        database="stationszuil"
    )

    myCursor = mydb.cursor(buffered=True)
    sql = f'select * from bericht where goedkeuring = %s order by datum desc, tijd desc limit 5;'
    myValues = ('1',)
    myCursor.execute(sql, myValues)

    mydb.commit()
    records = myCursor.fetchall()

    mydb.close()
    myCursor.close()

    return records

def database_login():
    with open('database_login.txt') as f:
        contents = f.readlines()
        strip_contents = []
        for line in contents:
            strip_contents.append(line.replace('\n', ''))
    return strip_contents

# To use the CLI instead of the gui remove the comment around the following block of code
'''
startupCLI()

getMode = userOrMod()
if getMode == 1:
    userFunctions()
elif getMode == 2:
    moderatorFunctions()
'''
