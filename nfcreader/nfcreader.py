#!/usr/bin/python
# Overview: API for CR95HF NFC Reader module.
#Authors: Ian Edwards and Agoritsa Spirakis
#MIT License
import ctypes
from ctypes import *
from datetime import datetime
import time
cr95hf = ctypes.CDLL('libCR95HF.so');

ADDRESSES = 128
protocol_selected = 1 #ISO15693 = 1, ISO14443-A = 2, ISO14443-B = 3, ISO18092 = 4
#testlib = ctypes.CDLL('./testlib.so');

# Establish a USBConnection to NFCReader module.
def USBConnect(): #Expect '0'
	return cr95hf._Z20CR95HFlib_USBConnectv()

# Send an echo to the MCU aboard the NFC Reader.
def Echo(): #Expected response of '5500'
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z14CR95HFlib_EchoPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

# Request the revision number of the MCU aboard the NFC reader.
def MCUrev():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z16CR95HFlib_MCUVerPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

# Get interface pin state from nfc reader.	
def getInterfacePinState():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z30CR95HFlib_getInterfacePinStatePc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

# Get ID number of IC.
def Idn(): 
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z13CR95HFlib_IdnPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

# Select command for NFC reader to select which NFC protocol standard to use.
def Select(request = 'ISO15693'):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	val = ''
	if request == 'ISO15693':
		val = b'010D'
		protocol_selected = 1
	elif request == 'ISO14443-A':
		val = b'0200'
		protocol_selected = 2
	elif request == 'ISO14443-B':
		val = b'0301'
		protocol_selected = 3
	elif request == 'ISO18092':
		val = b'0451'
		protocol_selected = 4
	strRequest=c_char_p(val)
	res=cr95hf._Z16CR95HFlib_SelectPcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("ASCII"))

# SendReceive function to send generic requests to MCU, such as reads, writes, IDn or inventory requests.
def SendReceive(request= b'260100'):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_char_p(request)
	res=cr95hf._Z21CR95HFlib_SendReceivePcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

# Function to read a block from a numerically specified address location on a tag.
def Read_Block(location='2'): 
	if location.isdigit():
		location = decToHex(location)
		if protocol_selected == 1:
			location = (3-len(location))*'0' + location #Enter location 1? Add two '0' so it is 001.
			command = '022' + location #command 022001
		else:
			location = (2-len(location))*'0' + location #Enter location 1? Add one '0' so it is 01.
			if protocol_selected == 2:
				command = '30' + location + '28'
			elif protocol_selected == 3:
				command = '08' + location
			else:
				return ('4','ISO18092 not supported by API.') #Haven't included this yet.
		command = bytes(str(command), 'utf-8')
		answer = []
		answer = SendReceive(command)
		return (answer[0], answer[1])
	else:
		return ('9', 'Please enter an integer value!')

# Function to write a byte of data to a tag after specifying the address location.		
def Write_Block(location = '2',data = '00000000'): #remember to add check that data is not longer than 8 hex values long. And remember we need to convert data...
	if (location.isdigit()):
		location = decToHex(location)
		command = ''
		if protocol_selected == 1:
			location = (2-len(location))*'0' + location #Enter location 1? Add one '0' so it is 01.
			command = '0221' + location + data
		elif protocol_selected == 2:
			command = 'A2' + location + data + '28'
		elif protocol_selected == 3:
			command = '09' + location + data
		elif protocol_selected == 4:
			return ('04', 'ISO18092 not supported by API.')
		command = bytes(str(command), 'utf-8')
		answer = []
		answer = SendReceive(command)
		return (answer[0], answer[1])
	else:
		return ('9', 'Check location format. Integers only!')

# Turn off field to save power on NFC Reader.
def FieldOff():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z18CR95HFlib_FieldOffPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

#R Reset SPI connection to NFC reader module.
def ResetSPI():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z18CR95HFlib_ResetSPIPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"));

# Send an IRQ to NFC Reader.
def SendIRQPulse():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z22CR95HFlib_SendIRQPulsePc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"));

# Send NSS pulse to NFC Reader.
def SendNSSPulse():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z22CR95HFlib_SendNSSPulsePc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"));

# Interact directly with MCU aboard the NFC reader by sending commands in the required format to it.
def STCmd(request=b'010803620100'): #default do protocol select ISO15693
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_char_p(request)
	res=cr95hf._Z15CR95HFlib_STCmdPcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def ResetToReady():
	return SendReceive(b'0226') #expect: 80040078F000

def GetSysInfo():
	return SendReceive(b'022B') #expect: 8012000F3F748841CE5902E0FF007F035A107000

#taghunting just using command from STM software in CR95HF commands tab.
def idleForTag(): 
		found = False
		pollVal = STCmd(b'01070E0A21007901180020606064743F08')
		return pollVal

# Loop for 5 seconds looking for tag.
def tagHunting(): 
	found = False
	t0 = time.time()
	while not(found):
		if (time.time() - t0 > 5): #Timeout after 5 seconds of detecting generic tag.
			break
		response = SendReceive()
		if (response[0] == 0):
			found = True
	if (found):
		return True
	else:
		return False

def initiate():
	return SendReceive(b'0226')

# Calculate elapsed time.
def elapsedTime(t0):
	t1 = time.time()
	return t1 - t0

# Continuously scans for a tag in the vicinity, and only when it is within range, does it write the entered data.
def ScanAndWrite(block = '2', data = '00000000'): #Can specify what to write and to where.
	#scan continuously for tag writing to, and loop until successful write.
	found = False
	written = False
	try:
		while (written == False): #scan continuously for tag writing to, and loop until successful write.
			response = SendReceive() #ping tag by just trying to read - throws error code if cannot read ie not in range.
			if (response[0] == 0):
				attempt = Write_Block(block, data)
				if (attempt[0] == 0):
					written = True
					response = Read_Block(block)
					#print("Successful write: ", response[1])
					return response
				elif (attempt[0] == '9'):
					return attempt
	except KeyboardInterrupt:
		print("\nScanning cancelled.")

# Reads entire tags contents.
def readAll():
	found = False
	finishedreading = False
	index = 0
	data = []
	try:
		while (finishedreading == False):
			response = SendReceive() #ping tag by just trying to read - throws error code if cannot read ie not in range.
			if (response[0] == 0):
				block = str(index)
				response = Read_Block(block)
				if response[0] == 0:
					data.append(response[1])
				index += 1
				if index == 128:
					finishedreading = True
		return data
				
	except KeyboardInterrupt:
		print("\nScanning cancelled.")

def extractPayload(reading): #80080000000005DA9801 position 6 to 13 has payload, note this is for ISO15693
	return reading[6:14]

# Function to loop through all the registers on the tag and clean the registers.
def cleanRegisters():
	for i in range(ADDRESSES):
		response = ScanAndWrite(str(i))
		if (response[0] != 0):
			print("Error cleaning register", i)
			return False
	return True

# Function to return a hex value in string, from a decimal input.
def decToHex(dec):
	# Dec to Hex => hex(dec) ==> 0x001 ==> prepHex(hex(dec)) = 001
	return str(hex(int(dec)))[2:] #cut off front two values, return string form.

 #Prepares an integer input to be written (converts to hex)
def prepWrite(dec):
	val = str(decToHex(dec))
	length = 8 - len(val)
	return length * '0' + val.upper() #Can also use z.fill(8)

#Convert a hex value either 0x0000 or just 0000 (base 16) to decimal (base 10) read in as string
def hexToDec(hex): 
	return int(hex, 16)

#Function to convert String to hex value.
def stringToHex(string):
	# ASCII to hex ==> prepHex(hex(ord(ASCII)))
	return hex(string)[2:] #cut off front two values

#Function to convert hex value to String.
def hexToString(hex): #Assumes input is string
	return hex.decode("hex")


		
	
