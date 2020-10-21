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

def main(): #Change how it starts... proper error check for USB error? Stop. etc.
    USBConnect()
    #nfc.SendReceive(b'02D202') #initiate
    print(nfc.Select())
    print(nfc.SendReceive()) #inventory command of tag.
    print("Welcome to NFC reader API demo!\n=========================================================")
    print("1) Read a block from the tag.")
    print("2) Write a block to the tag.")
    print("3) Enter Tag hunting mode.")
    print("4) Reset SPI connection (Reset).")
    print("5) Inventory command on tag.")
    print("6) Select 15693 protocol.")
    print("7) Exit.")
    print('=========================================================')
    while (input != '0'):
        option = input("Please select an option from the menu:\n")
        if (len(option) != 1 or not(option.isdigit())):
            print("Incorrect option selected! Please try again.\n")
        else:
            option = int(option)
            if (option == 1):
                location = input("Please enter a block location:\n")
                print(nfc.Read_Block(location))
            if (option == 2):
                location = input("Please enter a block location:\n")
                data = input("Please enter 8 digit hex data value:\n") #Make this decimal or string eventually...
                print(nfc.Write_Block(location, data))
            if (option == 3):
                #nfc.ResetSPI()
                #nfc.continuousTagScan()
                #print(nfc.taghunt())
                nfc.anothertaghunt()
            if (option == 4):
                print("SPI connection reset.")
                nfc.SendIRQPulse()
                Reset()
            if (option == 5):
                print(nfc.SendReceive())
            if (option == 6):
                print(nfc.Select())
            if (option == 7):
                print("Thank you for trying our API.")
                sys.exit()



if __name__ == "__main__":
    main()