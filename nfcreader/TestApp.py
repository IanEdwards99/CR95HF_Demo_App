"""Main module."""
import sys
sys.path.insert(1, './src/')
import nfcreader as nfc
from datetime import datetime
import time
import hardware as output
import RPi.GPIO as GPIO

def USBConnect():
    output = nfc.USBConnect()
    if (output == 0):
        print("Connected!")
    else:
        print("Error! NFC Reader not detected!")
        sys.exit(0)

def autoScanAndLog(dict, block = '2'): #Stores readings into dictionary with time of read. Optional: Specify location to read.
    #Start scanning for tags, and read if found. Uses toggle boolean to see if its been found, must only read when it has been found AGAIN.
    readAlready = False
    try:
        while True: #maybe add SendReceive first, then when its time to load, Read_Block (Double check)
            response = nfc.Read_Block(block) #ping tag by just trying to read - throws error code if cannot read ie not in range.
            if (response[0] != 0): #If no response from tag ie. not found (error code of 4 for bad communication)
                readAlready = False
                output.failure(2)
            if (response[0] == 0 and readAlready == False): #If tag found
                output.buzz_green(0.2)
                data = nfc.extractPayload(response[1])
                print(response[1])
                #Check if ID of that card is in dictionary, and if it is, if its last stored time is longer than 5 seconds
                if (data in dict):
                    if ((datetime.now() - dict[data]).total_seconds() > 5):
                        dict[data] = datetime.now()
                        print(dict)
                else:
                    dict[data] = datetime.now()
                    print(dict)

                time.sleep(2)
                readAlready = True
    except KeyboardInterrupt:
        print("\nScanning cancelled.")

def DisplayMenu():
    print("=========================================================\nWelcome to NFC reader API demo!\n=========================================================")
    print("1) Read a block from the tag.")
    print("2) Write a block to the tag.")
    print("3) Enter Tag hunting mode.")
    print("4) Reset SPI connection (Reset).")
    print("5) Inventory command on tag.")
    print("6) Select 15693 protocol.")
    print("7) Scan and log tags.")
    print("8) Scan till written to tag.")
    print("9) Print records.")
    print("C) Clean tag.")
    print("0) Exit.")
    print('=========================================================')

def main(): #Change how it starts... proper error check for USB error? Stop. etc.
    try:
        output.setup()
        records = {} #Create dictionary to store read values.
        USBConnect()
        print(nfc.Select())
        print(nfc.SendReceive()) #inventory command of tag.
        DisplayMenu()
        while (input != '0'):
            option = input("Please select an option from the menu:\n(If you wish to redisplay the menu, please enter 'M')\n")
            if (len(option) != 1):
                print("Incorrect option selected! Please try again.\n")
            elif (option == 'M'):
                DisplayMenu()
            elif (option == "C"):
                nfc.cleanRegisters()
                output.flash(3)
            else:
                option = int(option)
                if (option == 1):
                    location = input("Please enter a block location:\n")
                    val = nfc.Read_Block(location) #Add error checks...
                    if (val[0] != 0): #failed read
                        print(val[1])
                        output.failure(3)
                    else:
                        #print(nfc.Read_Block(location)) #prints out full response after read.
                        print("Data read (hex):", nfc.extractPayload(val[1])) #prints out just the payload read.
                        print("Decimal value:", nfc.hexToDec(nfc.extractPayload(val[1])))
                        output.buzz_green(0.4)

                if (option == 2):
                    location = input("Please enter a block location:\n")
                    data = input("Please enter a decimal data value:\n") #Max 10 digits
                    data = nfc.prepWrite(data) #Convert decimal input to hex input.
                    val = nfc.Write_Block(location, data)
                    if (val[0] != 0): #Failed write
                        print(val[1])
                        output.failure(3)
                    else:
                        #print(nfc.Write_Block(location, data)) #print full response after write.
                        readVal = nfc.extractPayload(nfc.Read_Block(location)[1])
                        print("Data written (hex):", readVal, "\nDecimal:", nfc.hexToDec(readVal))
                        output.buzz_green(0.4)

                if (option == 3):
                    if nfc.tagHunting():
                        print("Tag found")
                        output.buzz_green(0.4)
                    else:
                        print("No tag found")
                        output.failure(3)
                    # #Short syntax for if else, like ternary operator.
                if (option == 4):
                    print("SPI connection reset.")
                    nfc.SendIRQPulse()
                    nfc.ResetSPI()
                    nfc.Select() #After SPI reset need to reSelect protocol...
                    output.flash(3)
                    
                if (option == 5): #add error checking
                    val = nfc.SendReceive()
                    if val[0] == 0:
                        print(nfc.SendReceive())
                        output.buzz_green(0.4)
                    else:
                        output.failure(2)
                if (option == 6):
                    print(nfc.Select())
                    output.toggle_green(True)
                if (option == 7):
                    print("Press Ctrl + C to cancel scanning.")
                    autoScanAndLog(records)
                if (option == 8):
                    block = input("Please enter a block location to write to:\n")
                    data = input("Please enter a 10 digit decimal value to write:\n")
                    data = nfc.prepWrite(data) #Convert decimal input to hex input.
                    status = nfc.ScanAndWrite(block, data)
                    if status[0] == 0:
                        output.buzz_green(0.4)
                        print("Completed successfully! Wrote:", nfc.extractPayload(status[1]))
                if (option == 9):
                    print(records)
                if (option == 0):
                    print("Thank you for trying our API.")
                    sys.exit()
            

    finally:
        GPIO.cleanup() # cleanup all GPIO 



if __name__ == "__main__":
    main()