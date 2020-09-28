#!/usr/bin/python
import pylibCR95HF.CR95HF as nfc

print nfc.USBConnect()
print nfc.Echo()
print nfc.MCUrev()
print nfc.getInterfacePinState()
print nfc.Idn()
print nfc.Select()
print nfc.SendReceive()
print nfc.Read_Block(0)
print nfc.Write_Block(0,{0x00,0x11,0x22,0x33})
print nfc.ResetSPI()
print nfc.SendIRQPulse()
print nfc.SendNSSPulse()
#print FieldOff()
print nfc.STCmd()
