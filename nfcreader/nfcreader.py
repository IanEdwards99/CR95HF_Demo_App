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
def main():
    USBConnect()
    nfc.Select()
    nfc.SendReceive()



if __name__ == "__main__":
    main()