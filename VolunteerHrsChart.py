import datetime

def help():
    print("    1. 'Report': Volunteer Hours Report")
    print("    2. 'Sum': Volunteer Hours Summary")
    print("    3. 'Append': Add Volunteer Hours")
    print("    4. 'Delete': Delete Volunteer Hours")
    print("    5. 'Change': Delete Volunteer Hours")
    print("    6. 'Quit': Exit the Program")
    print()


def report():
    #Set up list to sort dates
    stringList = []
    numList = []
    
    volFile = open(fileName,"r")
    maxDateSpace = 5
    maxNameSpace = 5
    maxHourSpace = 6

    for line in volFile:
        
        sep = line.split("  ")
        

        #Add to lists to sort by date
        try:
            dateSep = sep[0].split("/")
            date = datetime.date(int(dateSep[2]), int(dateSep[0]), int(dateSep[1]))     #set as datetime
            currentdate = datetime.date.today()     #Get current date
            numList.append([currentdate - date, sep[2], sep[0], sep[1], sep[3]])        #Append if its a valid year
        except (ValueError, IndexError):
            stringList.append([0, sep[2], sep[0], sep[1], sep[3]])      #Append if not a valid datetime

        #Finds the max length of all parts of the header
        if len(sep[0]) > maxDateSpace:      #Finds the max length of all the dates
            maxDateSpace = len(sep[0])
            
        if len(sep[1]) > maxNameSpace:      #Finds the max length of all the names
            maxNameSpace = len(sep[1])
            
        if len(sep[2]) > maxHourSpace:      #Finds the max length of all the hours
            maxHourSpace = len(sep[2])
    volFile.close()

    #Prints the Header
    print("Date:" + " "*(maxDateSpace - 2) + "Name:"+ " "*(maxNameSpace - 2) + "Hours:" + " "*(maxHourSpace - 3) + "Status:")      #Prints the header
    print("-"*(19 + maxDateSpace+ maxNameSpace + maxHourSpace))       #Prints dashses after the header

    #Sort by Dates
    numList.sort()
    numList.reverse()
    stringList.sort()
    stringList.reverse()
    finalList = stringList + numList

    #Print based on sorted date
    for num in range(len(finalList)):
        print(finalList[num][2].title() + " "*(3 + maxDateSpace - len(finalList[num][2])) + finalList[num][3].title() + " "*(maxNameSpace - len(finalList[num][3]) + 3) + finalList[num][1] + " "*(maxHourSpace - len(finalList[num][1]) + 3) + finalList[num][4][:-1].title())
    print()         


def sum():
    #Calculate the Summary
    volFile = open(fileName,"r")
    totalHrs = 0
    approvedHrs = 0
    unApprovedHrs = 0
#    pendingHrs = 0
    hoursLeft = 100
    for line in volFile:
        sep = line.split("  ")
        totalHrs += float(sep[2])       #Adds the total Hours
        if "approved" in sep[3].lower():
            approvedHrs += float(sep[2])        #Adds the Approved Hours
            
        elif "done" in sep[3].lower():
            unApprovedHrs += float(sep[2])        #Adds the Unapproved Hours
            
#        else:
#            pendingHrs += float(sep[2])        #Adds the Pending Hours
    volFile.close()

    if hoursLeft - totalHrs < 0:
        hoursLeft = 0
    else:
        hoursLeft -= totalHrs

    #Prints the Summary
    print("Total Hours:   %.2f" %totalHrs)
    print("Approved:      %.2f" %approvedHrs)
    print("Non-Approved:  %.2f" %unApprovedHrs)
#    print("Pending Hours: %.2f" %pendingHrs)
    print("Hours Left:    %.2f" %(hoursLeft))
    print()


def append():
    for append in range(1):
        #Print Options
        print(cancelOption)
        dateInput = ""
        #Take in Append Input
        dateInput = input("Date of the Volunteering (mm/dd/yyyy):   ")
        if "cancel" in dateInput.lower():       #Go back to the previous page
            print()
            break

        #Format the date
        try:
            dateInputSep = dateInput.split("/")     
            newDate = "%.2d" %int(dateInputSep[0]) + "/" + "%.2d" %int(dateInputSep[1]) + "/" + dateInputSep[2]
        except (ValueError, IndexError):
            newDate = dateInput
            
        nameInput = input("Name of the Volunteering:   ")
        if "cancel" in nameInput.lower():       #Go back to the previous page
            print()
            break
        
        hrsInput = input("Number of Hours:   ")
        if "cancel" in hrsInput.lower():       #Go back to the previous page
            print()
            break
        
#        statusInput = input('''Status of the Hours:
#    1. Approved
#    2. Done
#    3. Pending
#''' )
        statusInput = input('''Status of the Hours:
    1. Approved
    2. Done
''' )
        if "cancel" in statusInput.lower():       #Go back to the previous page
            print()
            break
        print()

        #Add hour to the txt file
        volFile = open(fileName,"a")
        volFile.write(newDate.title() + "  " + nameInput.title() + "  " + "%.2f" %float(hrsInput) + "  " + statusInput.title()+"\n")
        volFile.close()


def delete():
    for delete in range(1):
        #Print Options
        print(cancelOption)

        #Take the Delete Input
        dateInput = input("Date of the Volunteering:   ")
        if "cancel" in dateInput.lower():       #Go back to the previous page
            print()
            break
        dateInputSep = dateInput.split("/")     #For the vague date finding
        
        nameInput = input("Name of the Volunteering:   ")
        if "cancel" in nameInput.lower():       #Go back to the previous page
            print()
            break
        
        hrsInput = input("Number of Hours:   ")
        if "cancel" in hrsInput.lower():       #Go back to the previous page
            print()
            break
        
        statusInput = input("Status of the Hours:   ")
        if "cancel" in statusInput.lower():       #Go back to the previous page
            print()
            break
        
        print()

        #Find the Hour
        Hrslists = []
        volFile = open(fileName,"r")
        found = False
        for line in volFile:
            sep = line.split("  ")
            dateSep = sep[0].split("/")     #For the vague date finding

            #Checking for the Date Match
            dateMatch = checkDate(dateInputSep, dateSep)
            
            #If Hour is found
            if found == False and nameInput.lower() in sep[1].lower() and float(sep[2]) == float(hrsInput) and statusInput.lower() in sep[3][:-1].lower() and dateMatch == True:
                desicion = confirm("delete", sep)
                    
                if "yes" in desicion.lower():       #Avoid adding if Hour confirmed
                    found = True        
                        
                else:
                    Hrslists.append([sep[0], sep[1], float(sep[2]), sep[3]])        #Add Hour if not confirmed
                        
            else:
                Hrslists.append([sep[0], sep[1], float(sep[2]), sep[3]])        #Add Hour if it doesn't match inputs
                    
        volFile.close()

        #If no Hour was found
        if found == False:
            print("ERROR: No Such Hours Exists!")
            print()

        #Overwrite the txt file
        overwrite(Hrslists)

def confirm(name,sep):
    maxDateSpace = max(5, len(sep[0]))
    maxNameSpace = max(5, len(sep[1]))
    maxHourSpace = max(6, len(sep[2]))

    #Print Header
    print("Date:" + " "*(maxDateSpace - 2) + "Name:"+ " "*(maxNameSpace - 2) + "Hours:" + " "*(maxHourSpace - 3) + "Status:")
    print("-"*(19 + maxNameSpace + maxHourSpace + maxDateSpace))

    #Print the Found Hour
    print(sep[0].title() + " "*(maxDateSpace - len(sep[0]) + 3) + sep[1].title() + " "*(maxNameSpace - len(sep[1]) + 3) + sep[2] + " "*(maxHourSpace - len(sep[2]) + 3) + sep[3].title())

    #Confirm the find
    desicion = input("Do you want to " + name + ''' this?
    1. Yes
    2. No
''')
    print()

    return desicion

def checkDate(dateInputSep, dateSep):
    #Checking for the Date Match
    dateMatch = True
    if len(dateInputSep) != len(dateSep):
        dateMatch = False
    else:
        for length in range(len(dateInputSep)):
            if dateInputSep[length].isdigit() == dateSep[length].isdigit() == True:
                if int(dateInputSep[length]) != int(dateSep[length]):
                    dateMatch = False
                    break

            else:
                if dateInputSep[length].lower() != dateSep[length].lower():
                    dateMatch = False
                    break
    
    return dateMatch

def overwrite(Hrslists):
#Overwrite the txt file
    volFile = open(fileName, "w")
    for hrs in Hrslists:
        volFile.write(hrs[0] + "  " + hrs[1] + "  " + "%.2f" %hrs[2] + "  " + hrs[3])
        
    volFile.close()


def change():
    for change in range(1):
        #Print Options
        print(cancelOption)

        #Take Old Hour Inputs
        dateInput = input("Previous Date of the Volunteering:   ")
        if "cancel" in dateInput.lower():       #Go back to the previous page
            print()
            break
        dateInputSep = dateInput.split("/")     #For the vague date finding
        
        nameInput = input("Previous Name of the Volunteering:   ")
        if "cancel" in nameInput.lower():       #Go back to the previous page
            print()
            break
                
        hrsInput = input("Previous Number of Hours:   ")
        if "cancel" in hrsInput.lower():       #Go back to the previous page
            print()
            break
                
        statusInput = input("Previous Status of the Hours:   ")
        if "cancel" in statusInput.lower():       #Go back to the previous page
            print()
            break
        print() 


        #Find the Hour
        Hrslists = []
        volFile = open(fileName,"r")
        found = False
        cancelBool = False
        for line in volFile:
            sep = line.split("  ")
            dateSep = sep[0].split("/")     #For the vague date finding

            #Checking for the Date Match
            dateMatch = checkDate(dateInputSep, dateSep)
                        
            #If Hour is found
            if found == False and nameInput.lower() in sep[1].lower() and float(sep[2]) == float(hrsInput) and statusInput.lower() in sep[3][:-1].lower() and dateMatch == True:
                desicion = confirm("change", sep)
                    
                if "yes" in desicion.lower():
                    #Print Options
                    print(cancelOption +'''    2. 'Same': Same as Previous Input
''')
                    #Take New Hour Inputs
                    newDateInput = input("New Date of the Volunteering (mm/dd/yyyy):   ")
                    if "cancel" in newDateInput.lower():       #Go back to the previous page
                        print()
                        cancelBool = True
                        break
                    
                    elif "same" in newDateInput.lower():        #Copy the Old Hour Data
                        newDateInput = sep[0]

                    #Formats the date
                    try:
                        newDateInputSep = newDateInput.split("/")
                        finalNewDateInput = "%.2d" %int(newDateInputSep[0]) + "/" + "%.2d" %int(newDateInputSep[1]) + "/" + newDateInputSep[2]
                    except (ValueError, IndexError):
                        finalNewDateInput = newDateInput
                               
                    newNameInput = input("New Name of the Volunteering:   ")
                    if "cancel" in newNameInput.lower():       #Go back to the previous page
                        print()
                        cancelBool = True
                        break
                    
                    elif "same" in newNameInput.lower():        #Copy the Old Hour Data
                        newNameInput = sep[1]
                      
                    newHrsInput = input("New Number of Hours:   ")
                    if "cancel" in newHrsInput.lower():       #Go back to the previous page
                        print()
                        cancelBool = True
                        break
                    
                    elif "same" in newHrsInput.lower():        #Copy the Old Hour Data
                        newHrsInput = sep[2]
                                                
                    newStatusInput = input("New Status of the Hours:   ")
                    if "cancel" in newStatusInput.lower():       #Go back to the previous page
                        print()
                        cancelBool = True
                        break
                    
                    elif "same" in newStatusInput.lower():        #Copy the Old Hour Data
                        newStatusInput = sep[3]

                    else:
                        newStatusInput += "\n"      #To prevent error in the txt file
                    print()
                         
            
                    found = True        #Avoid adding if Hour confirmed
                    Hrslists.append([finalNewDateInput.title(), newNameInput.title(), float(newHrsInput), newStatusInput.title()])      #Add the Changed Hour
                        
                else:
                    Hrslists.append([sep[0], sep[1], float(sep[2]), sep[3]])        #Add Hour if not confirmed
                        
            else:
                Hrslists.append([sep[0], sep[1], float(sep[2]), sep[3]])        #Add Hour if it doesn't match inputs
                    
        volFile.close()

        #Break out of while loop if 'cancel'
        if cancelBool == True:
            break
        
        #If no Hour was found
        if found == False:
            print("ERROR: No Such Hours Exists!")
            print()
 
        #Overwrite the txt file
        overwrite(Hrslists)
    
fileName = "VolunteerHrs.txt"
cancelOption = '''Options:
    1. 'Cancel': Go Back to Main Menu
'''
def main():
    userInput = ""
    File = open(fileName, "a")
    File.close()

    while True:
        print("'Help': Options")
        #print("hey", end = "", flush = True)
        userInput = input(">>> ")
        
        if userInput.lower() == "help":
            help()
        
        elif userInput.lower() == "report":          #Gets a volunteer hours report
            report()
        
        elif userInput.lower() == "sum":           #Gets a summary of the hours
            sum()
   
        elif userInput.lower() == "append":
            append()

        elif userInput.lower() == "delete":
            delete()
            
        elif userInput.lower() == "change":
            change()

        elif userInput.lower() == "quit":
            break
        
        else:
            print()
main()
