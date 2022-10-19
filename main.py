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
random.seed()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin"  # Very safe I know
)


def startupCLI():

    print(firstprint)
    print("\n\n\n")


def userInput():
    try:
        userName = input("Voer uw naam in. In het geval dat u dit veld leeg laat blijft u anoniem: ")

        if userName is "":
            userName = "Anoniem"
        userMessage = input("Voer uw bericht in. Deze mag maximaal 140 karakters bevatten: ")

        if len(userMessage) > 140:
            print("Uw bericht was te lang, probeer het nog een keer.\n")
            userMessage = input("Voer uw bericht in. Deze mag maximaal 140 karakters bevatten: ")

        userInputList = [userMessage, userName]
        return userInputList
    except Exception as e:
        print(f"An error has occured: {e}, please try again.")

def parseData(userList):

    try:
        stationList = ["Amersfoort Centraal", "Utrecht Centraal", "'S-Hertogenbosch"]
        randStation = stationList[random.randint(0, 2)]

        currentDateTime = datetime.now()
        msgTime = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")
        filename = currentDateTime.strftime("%d%m%Y_%H%M%S")

        # Write to csv file
        with open(f'messages/{filename}.csv', 'w') as myFile:

            columns = ["Message", "DateTime", "Username", "Station"]
            rows = [userList[0], msgTime, userList[1], randStation]  # Message, Date and time, Username, Random train station

            writer = csv.writer(myFile)
            writer.writerow(columns)
            writer.writerow(rows)
            print("\n")
    except Exception as e:
        print(f"An error has occured: {e}, please try again.")


print(mydb)

# startupCLI()

# while True:
 #   message = userInput()
 #   parseData(message)
