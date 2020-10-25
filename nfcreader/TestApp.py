"""Main module."""
import sys
sys.path.insert(1, './src/')
import nfcreader as nfc
from datetime import datetime
import time
import hardware as output
import RPi.GPIO as GPIO

protocols = ['ISO15693', 'ISO14443-A', 'ISO14443-B', 'ISO18092']

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
                data = nfc.extractPayload(response[1])
                dec = nfc.hexToDec(data)
                print(dec)
                output.lcd.clear()
                output.lcd.write_string(u'Tag found!\n\rData: ' + str(dec))
                #Check if ID of that card is in dictionary, and if it is, if its last stored time is longer than 5 seconds
                if (data in dict):
                    if ((datetime.now() - dict[data]).total_seconds() > 5):
                        dict[data] = datetime.now()
                        print("Data:", dec, "\nTime:", datetime.now().time())
                else:
                    dict[data] = datetime.now()
                    print("Data:", dec, "\nTime:", datetime.now().time())
                readAlready = True
                output.buzz_green(0.2)
                time.sleep(2)
                
    except KeyboardInterrupt:
        print("\nScanning cancelled.")

def DisplayMenu():
    print("=========================================================\nWelcome to NFC reader API demo!\n=========================================================")
    print("1) Select ISO protocol.")
    print("2) Inventory command on tag.")
    print("3) Enter Tag hunting mode.")
    print("4) Read a block from the tag.")
    print("5) Write a block to the tag.")
    print("6) Scan and log tags.")
    print("7) Scan till written to tag.")
    print("8) Print stored records.")
    print("9) Read entire tag contents.")
    print("C) Clean tag.")
    print("R) Reset SPI connection (Reset).")
    print("0) Exit.")
    print('=========================================================')

def main(): #Change how it starts... proper error check for USB error? Stop. etc.
    try:
        output.setup()
        records = {} #Create dictionary to store read values.
        USBConnect()
        output.flash(1)
        nfc.initiate()
        print(nfc.Select())
        print(nfc.SendReceive()) #inventory command of tag.
        DisplayMenu()
        output.lcd.write_string(u'NFC reader\n\rinitialized.')
        while (input != '0'):
            output.toggle_buzzer(False)
            option = input("Please select an option from the menu:\n(If you wish to redisplay the menu, please enter 'M')\n")
            if (len(option) != 1):
                output.lcd.clear()
                output.lcd.write_string(u'Incorrect option\n\rselected!')
                print("Incorrect option selected! Please try again.\n")

            elif (option == 'M'):
                DisplayMenu()

            elif (option == "C"):
                output.lcd.clear()
                output.lcd.write_string(u'Place tag on reader.')
                status = nfc.cleanRegisters()
                if status:
                    print("Completed cleaning registers.")
                    output.lcd.clear()
                    output.lcd.write_string(u'Tag wiped.')
                    output.flash(2)
                else:
                    print("Error cleaning registers.")
                    output.lcd.clear()
                    output.lcd.write_string(u'Error\n\rcleaning.')
                    output.failure(2)

            elif (option == "R"):
                output.lcd.clear()
                output.lcd.write_string(u'Connection reset.')
                print("SPI connection reset.")
                nfc.SendIRQPulse()
                nfc.ResetSPI()
                nfc.Select() #After SPI reset need to reSelect protocol...
                output.flash(1)

            else:
                option = int(option)
                if (option == 1):
                    choice = input("Select ISO protocol:\n1) ISO15693\n2) ISO14443-A\n3) ISO14443-B\n4) ISO18092")
                    if ((len(choice) != 1) or not(choice.isdigit())):
                        print("Error: Incorrect selection.")
                        output.lcd.clear()
                        output.lcd.write_string(u'Incorrect\n\rselection.')
                    else:
                        if (choice != 0):
                            choice = int(choice)
                            string = protocols[choice-1]
                            val = nfc.Select(string)
                            if val[0] == 0:
                                print(string, "protocol selected.")
                                output.lcd.clear()
                                output.lcd.write_string(u'Protocol\n\rselected!')
                                output.toggle_green(True)
                            else:
                                print("Failed to select", string, ". Try again.")
                                output.lcd.clear()
                                output.lcd.write_string(u'Protocol select\n\rfailed.')

                if (option == 2):
                    val = nfc.SendReceive()
                    if val[0] == 0:
                        print(val)
                        output.lcd.clear()
                        output.lcd.write_string("Inventory\n\rsuccessful!")
                        output.buzz_green(0.4)
                    else:
                        print(val[1])
                        output.lcd.clear()
                        output.lcd.write_string(u'Inventory\n\rfailed.')
                        output.failure(2)

                if (option == 3):
                    output.lcd.clear()
                    output.lcd.write_string(u'Looking for tag...')
                    if nfc.tagHunting():
                        print("Tag found.")
                        output.lcd.clear()
                        output.lcd.write_string(u'Tag found!')
                        output.buzz_green(0.4)
                    else:
                        print("No tag found.")
                        output.lcd.clear()
                        output.lcd.write_string(u'No tag found.')
                        output.failure(3)

                if (option == 4):
                    output.lcd.clear()
                    output.lcd.write_string(u'Place your tag\n\ron the reader.')
                    location = input("Please enter a block location:\n")
                    val = nfc.Read_Block(location) #Add error checks...
                    if (val[0] != 0): #failed read
                        print(val[1])
                        output.lcd.clear()
                        output.lcd.write_string("Error:\n\rRead failed.")
                        output.failure(2)
                    else:
                        #print(nfc.Read_Block(location)) #prints out full response after read.
                        print("Data read (hex):", nfc.extractPayload(val[1])) #prints out just the payload read.
                        string = nfc.hexToDec(nfc.extractPayload(val[1]))
                        print("Decimal value:", string)
                        output.lcd.clear()
                        output.lcd.write_string("Value read:\n\r" + str(string))
                        output.buzz_green(0.4)
                    
                if (option == 5):
                    output.lcd.clear()
                    output.lcd.write_string(u'Place your tag\n\ron the reader.')
                    location = input("Please enter a block location:\n")
                    data = input("Please enter a decimal data value:\n") #Max 10 digits
                    if data.isdigit():
                        data = nfc.prepWrite(data)
                        val = nfc.Write_Block(location, data)
                        if (val[0] != 0): #Failed write
                            print(val[1])
                            output.lcd.clear()
                            output.lcd.write_string("Error:\n\rWrite failed.")
                            output.failure(2)
                        else:
                            #print(nfc.Write_Block(location, data)) #print full response after write.
                            readVal = nfc.extractPayload(nfc.Read_Block(location)[1])
                            print("Data written (hex):", readVal, "\nDecimal:", nfc.hexToDec(readVal))
                            output.lcd.clear()
                            output.lcd.write_string("Value written:\n\r" + str(nfc.hexToDec(readVal)))
                            output.buzz_green(0.4)
                    else:
                        print("Please enter an integer for the data.")

                if (option == 6):
                    print("Press Ctrl + C to cancel scanning.")
                    output.lcd.clear()
                    output.lcd.write_string(u'Scanning\n\rfor tags...')
                    autoScanAndLog(records)

                if (option == 7):
                    block = input("Please enter a block location to write to:\n")
                    data = input("Please enter a 10 digit decimal value to write:\n")
                    if data.isdigit():
                        data = nfc.prepWrite(data) #Convert decimal input to hex input.
                        output.lcd.clear()
                        output.lcd.write_string(u'Scanning\n\rto write...')
                        status = nfc.ScanAndWrite(block, data)
                        if status[0] == 0:
                            data_out = nfc.extractPayload(status[1])
                            output.lcd.clear()
                            output.lcd.write_string(u'Wrote:\n\r' + str(data_out))
                            output.buzz_green(0.4)
                            print("Completed successfully! Wrote:", data_out)
                        else:
                            print(status[1])
                            output.lcd.clear()
                            output.lcd.write_string(u'Incorrect\n\rinput!')
                    else:
                        print("Incorrect data format! Integers only!")
                        output.lcd.clear()
                        output.lcd.write_string(u'Incorrect\n\rinput!')

                if (option == 8):
                    output.lcd.clear()
                    output.lcd.write_string(u'Records sent\n\rto terminal.')
                    print(records)

                if (option == 9):
                    output.lcd.clear()
                    output.lcd.write_string(u'Place tag\n\ron reader.')
                    val = nfc.readAll()
                    print("Address:\t", "Data:")
                    for i in range(0, 128):
                        data = nfc.hexToDec(nfc.extractPayload(val[i]))
                        if data != 0:
                            print(i, "\t\t", data)

                if (option == 0):
                    output.lcd.clear()
                    output.lcd.write_string(u'Thank you for\n\rtrying our API.')
                    print("Thank you for trying our API.")
                    sys.exit()
            

    finally:
        GPIO.cleanup() # cleanup all GPIO 



if __name__ == "__main__":
    main()