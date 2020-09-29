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

def Echo():
    output = nfc.Echo()
    print("Sending echo to CR95HF... Result: ", output)

def Select():
    output = nfc.Select()
    print(output[0], output[1], "success")

def SendReceive():
    output = nfc.SendReceive()
    print(output[0], output[1], "success")

def main():
    USBConnect()
    Echo()
    Select()
    SendReceive()



if __name__ == "__main__":
    main()