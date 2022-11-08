## User modules
# This module contains all of the
import random
import csv
from datetime import datetime
import mysql.connector
import os
import shutil
import openweather
random.seed()

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
# This function prints a welcome message in the console when using the CLI
def startupCLI():

    print(firstprint)
    print("\n")


# This function handles the choice between a user and moderator in CLI
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


# This function handles the choice flow of the user
def userFunctions():
    while True:
        newMessagePrompt = input("Do you want to enter a new message? (YES/NO): ")
        newMessagePrompt = newMessagePrompt.upper()

        if newMessagePrompt == 'YES' or newMessagePrompt == 'NO':
            if newMessagePrompt == 'YES':
                # Get user input and let parseData write it to file
                message = userInput()
                parseData(message)
                continue
            elif newMessagePrompt == 'NO':
                break
        else:
            # Make sure the user can only enter lower/uppercase YES or NO
            print("Please enter a valid answer (YES/NO)\n")
            continue


# This function handles the workflow of the moderator
def moderatorFunctions():
    # Get the details of the moderator
    modName = input('Please enter your moderator name: ')
    modMail = input('Please enter your moderator mail: ')

    # Stay in a loop to approve messages until the moderator wants to quit
    while True:
        moderatePrompt = input("Do you want to validate a new message? (YES/NO): ")
        moderatePrompt = moderatePrompt.upper()
        if moderatePrompt == 'YES' or moderatePrompt == 'NO':
            if moderatePrompt == 'YES':
                # Call the function that handles the message and the approval
                cli_moderateMessage(modName, modMail)
                continue
            elif moderatePrompt == 'NO':
                break
        else:
            print("Please enter a valid answer (YES/NO)\n")
            continue


# This function gets the details of the user and returns the result
def userInput():
    try:
        userName = input("Enter your name. In the case this field stays empty you will be anonymous: ")

        # Set username to Anoniem if no name was entered
        if userName is "":
            userName = "Anoniem"

        userMessage = input("Enter your message. The message can not contain more than 140 characters: ")

        # Check if the message conforms to the requirements, if input is wrong for a second time the program closes
        if len(userMessage) > 140:
            print("Your message was too long, please try again.\n")
            userMessage = input("Enter your message. The message can not contain more than 140 characters: ")
            if len(userMessage) > 140:
                print("Your message was too long again, please restart program.\n")
                quit()

        # Return a list with the user data we gathered
        userInputList = [userMessage, userName]
        return userInputList
    except Exception as e:
        print(f"An error has occured: {e}, please try again.")


# This function chooses a random station from an unchanging list and returns the result
def rand_station():
    stationList = ["Amersfoort", "Utrecht", "Den Bosch"]
    randStation = random.choice(stationList)
    return randStation


# This function takes the data from userList and the random station and writes this to a csv file along with date data
def parseData(userList, station):

    try:
        randStation = station

        # Get the current date and time, set the message data and file name accordingly
        currentDateTime = datetime.now()
        msgDate = currentDateTime.strftime("%Y-%m-%d")
        msgTime = currentDateTime.strftime("%H:%M:%S")
        filename = currentDateTime.strftime("%d%m%Y_%H%M%S")

        # Write to csv file
        with open(f'messages/{filename}.csv', 'w', newline='') as myFile:

            columns = ["Message", "Date", 'Time', "Username", "Station"]
            # rows order goes accordingly -> Message, Date, Time, Username, Random train station
            rows = [userList[0], msgDate, msgTime, userList[1], randStation]

            writer = csv.writer(myFile)
            writer.writerow(columns)
            writer.writerow(rows)
            print("\n")
    except Exception as e:
        print(f"An error has occured: {e}, please try again.")


# This function returns the oldest file of the messages directory and returns a string with the filename if valid
def getOldestFile():
    # Load all files in the directory into a list
    list_files = os.listdir('messages')

    # If there are no files in the directory let the function return False
    if len(list_files) == 0:
        return False
    # Fix pathnames of the files in directory so .py files in other directories in the project can find them if this function is used
    for i in range(len(list_files)):
        list_files[i] = f'messages/{list_files[i]}'

    # Set oldest file to the lowest creation time in the list
    oldest_file = min(list_files, key=os.path.getctime)
    return oldest_file


# This function displays the message to approve and handles the response of the moderator
def cli_moderateMessage(modName, modMail):
    to_moderate = getOldestFile()
    plainMessage = ''

    # Get the oldest message and print it to the console
    with open(to_moderate, 'r', newline='') as file:
        csvRead = csv.DictReader(file)
        for row in csvRead:
            plainMessage = row['Message']
    print(f'\nThe message to approve:\n{plainMessage}\n')

    # Get a yes or no as approval status.
    while True:
        getApproval = input("Do you want to approve this message? (YES/NO): ")
        getApproval = getApproval.upper()

        # Set Yes to 1 and No to 0 or let the user try again
        if getApproval == 'YES':
            getApproval = '1'
            break
        elif getApproval == 'NO':
            getApproval = '0'
            break
        else:
            print("Please enter a valid answer (YES/NO)\n")
            continue

    # Get date data to pass with message data
    currentDateTime = datetime.now()
    approveTime = currentDateTime.strftime("%H:%M")
    approveDate = currentDateTime.strftime("%Y-%m/%d")

    writeDatabase(to_moderate, getApproval, approveTime, approveDate, modName, modMail)


# This function takes approval status and writes it to the database
def gui_moderateMessage(file, modName, modMail, approval):
    # Get date data to pass with message data
    currentDateTime = datetime.now()
    approveTime = currentDateTime.strftime("%H:%M")
    approveDate = currentDateTime.strftime("%Y-%m/%d")
    writeDatabase(file, approval, approveTime, approveDate, modName, modMail)


# This function writes the incoming data to the connected database
def writeDatabase(file, approval, approveTime, approveDate, modName, modMail):
    # Get login data
    db_login = database_login()

    # Setup connection with database
    mydb = mysql.connector.connect(
        host=db_login[0],
        user=db_login[1],
        password=db_login[2],
        database=db_login[3]
    )

    # Read data from incoming file
    with open(file) as f:
        csvReader = csv.DictReader(f)
        for row in csvReader:
            csvMessage = row['Message']
            csvDate = row['Date']
            csvTime = row['Time']
            csvUsername = row['Username']
            csvStation = row['Station']

    # Setup query
    myCursor = mydb.cursor()
    sql = 'INSERT INTO bericht VALUES (default, %s, %s, %s, %s, %s, ' \
          '%s, %s, %s, %s, %s)'
    myValues = (csvMessage, csvDate, csvTime, csvUsername, csvStation, approval, approveDate, approveTime, modName, modMail)

    # Execute query
    myCursor.execute(sql, myValues)
    mydb.commit()

    # Move file to another folder
    moderated = file.split('/')
    shutil.move(file, f'mod_messages/{moderated[1]}')

    # Close database connection and cursor
    mydb.close()
    myCursor.close()


# This function reads facility data from the database for a certain city and returns the result
def readDatabaseStation(service, city):
    # Get login data
    db_login = database_login()

    # Setup connection with database
    mydb = mysql.connector.connect(
        host=db_login[0],
        user=db_login[1],
        password=db_login[2],
        database=db_login[3]
    )

    # Setup query
    myCursor = mydb.cursor(buffered=True)
    sql = f'SELECT {service} FROM station_service WHERE station_city = %s'
    myValues = (city, )

    # Execute query
    myCursor.execute(sql, myValues)
    mydb.commit()

    # Save query result
    records = myCursor.fetchall()

    # Close connection and query
    mydb.close()
    myCursor.close()

    # Return query result
    return records


# This function reads the 5 most recent approved messages from the connected database and returns them in a list
def getMessages():
    # Get login data
    db_login = database_login()

    # Setup connection with database
    mydb = mysql.connector.connect(
        host=db_login[0],
        user=db_login[1],
        password=db_login[2],
        database=db_login[3]
    )

    # Setup query
    myCursor = mydb.cursor(buffered=True)
    sql = f'select * from bericht where goedkeuring = %s order by datum desc, tijd desc limit 5;'
    myValues = ('1',)

    # Execute query
    myCursor.execute(sql, myValues)
    mydb.commit()

    # Save query result
    records = myCursor.fetchall()

    # Close connection and query
    mydb.close()
    myCursor.close()

    # Return query result
    return records


# This function reads the file database_login.txt for the database inlog data
def database_login():
    # Read file
    with open('database_login.txt') as f:
        contents = f.readlines()

        # Remove trailing \n
        strip_contents = []
        for line in contents:
            strip_contents.append(line.replace('\n', ''))
    # Return the login data in a list
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
