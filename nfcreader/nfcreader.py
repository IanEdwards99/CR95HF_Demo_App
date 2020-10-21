"""Main module."""
import sys
sys.path.insert(1, './pylibCR95HF-master/pylibCR95HF/')
import CR95HF as nfc

def USBConnect():
    output = nfc.USBConnect()
    if (output == 0):
        print("Connected!")
    else:
        print("Error! NFC Reader not detected!")
        sys.Exit()

def Echo():
    output = nfc.Echo()
    if (output != '5500'):
        Reset()
    print("Sending echo to CR95HF... Result: ", output)

def Select():
    output = nfc.Select()
    print(output[0], output[1], "success")

def SendReceive():
    output = nfc.SendReceive()
    print(output[0], output[1], "success")

def Reset():
    nfc.ResetSPI()

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
    print("0) Exit.")
    print('=========================================================')

def main(): #Change how it starts... proper error check for USB error? Stop. etc.
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
        else:
            option = int(option)
            if (option == 1):
                location = input("Please enter a block location:\n")
                val = nfc.Read_Block(location) #Add error checks...
                if (val[0] != 0):
                    print(val[1])
                else:
                    #print(nfc.Read_Block(location)) #prints out full response after read.
                    print("Data read (hex):", nfc.extractPayload(val[1])) #prints out just the payload read.
                    print("Decimal value:", nfc.hexToDec(nfc.extractPayload(val[1])))

            if (option == 2):
                location = input("Please enter a block location:\n")
                data = input("Please enter a decimal data value:\n") #Max 10 digits
                data = nfc.prepWrite(data) #Convert decimal input to hex input.
                val = nfc.Write_Block(location, data)
                if (val[0] != 0):
                    print(val[1])
                else:
                    #print(nfc.Write_Block(location, data)) #print full response after write.
                    readVal = nfc.extractPayload(nfc.Read_Block(location)[1])
                    print("Data written (hex):", readVal, "\nDecimal:", nfc.hexToDec(readVal))

            if (option == 3):
                print(nfc.tagHunting() and "Tag found." or "No tag found.") #Short syntax for if else, like ternary operator.
            if (option == 4):
                print("SPI connection reset.")
                nfc.SendIRQPulse()
                Reset()
                nfc.Select() #After SPI reset need to reSelect protocol...
            if (option == 5):
                print(nfc.SendReceive())
            if (option == 6):
                print(nfc.Select())
            if (option == 7):
                print("Press Ctrl + C to cancel scanning.")
                nfc.autoScanAndLog(records)
            if (option == 8):
                block = input("Please enter a block location to write to:\n")
                data = input("Please enter a 10 digit decimal value to write:\n")
                data = nfc.prepWrite(data) #Convert decimal input to hex input.
                nfc.ScanAndWrite(block, data)
            if (option == 9):
                print(records)
            if (option == 0):
                print("Thank you for trying our API.")
                sys.exit()



if __name__ == "__main__":
    main()