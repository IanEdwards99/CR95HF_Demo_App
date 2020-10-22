#!/usr/bin/python
import ctypes
from ctypes import *
from datetime import datetime
import time
cr95hf = ctypes.CDLL('libCR95HF.so');

#testlib = ctypes.CDLL('./testlib.so');

#>>> Frame sent by the Host to CR95HF
#<<< Frame sent by the CR95HF to the Host

def USBConnect(): #Expect '0000'
	return cr95hf._Z20CR95HFlib_USBConnectv()

def Echo(): #Expected response of '5500'
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z14CR95HFlib_EchoPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def MCUrev():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z16CR95HFlib_MCUVerPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))
	
def getInterfacePinState():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z30CR95HFlib_getInterfacePinStatePc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))
	
def Idn(): #Get ID number of IC.
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z13CR95HFlib_IdnPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def Select(request = 'ISO15693'):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_char_p(b'010D')
	res=cr95hf._Z16CR95HFlib_SelectPcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("ASCII"))

def SendReceive(request= b'260100'):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_char_p(request)
	res=cr95hf._Z21CR95HFlib_SendReceivePcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def Read_Block(location='2', blocks = 1): #for now enter whole command... blocks is number of lines to read. Optional.
	location = (3-len(location))*'0' + location #Enter location 1? Add two '0' so it is 001.
	command = '022' + location #command 022001
	command = bytes(str(command), 'utf-8')
	answer = []
	answer = SendReceive(command)
	return (answer[0], answer[1])
    	
def Write_Block(location = '2',data = '00000000'): #remember to add check that data is not longer than 8 hex values long. And remember we need to convert data...
	location = (2-len(location))*'0' + location #Enter location 1? Add one '0' so it is 01.
	command = ''
	command = '0221' + location + data
	command = bytes(str(command), 'utf-8')
	answer = []
	answer = SendReceive(command)
	return (answer[0], answer[1])

def FieldOff():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z18CR95HFlib_FieldOffPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def ResetSPI():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z18CR95HFlib_ResetSPIPc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"));

def SendIRQPulse():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z22CR95HFlib_SendIRQPulsePc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"));

def SendNSSPulse():
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	res=cr95hf._Z22CR95HFlib_SendNSSPulsePc(strAnswer)
	return (res,strAnswer.value.decode("utf-8"));

def STCmd(request=b'010803620100'): #default do protocol select
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_char_p(request)
	res=cr95hf._Z15CR95HFlib_STCmdPcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def Initiate():
	return SendReceive(b'02D202') #initiate: 800D00FF3F748841CE5902E00D4D00

def ResetToReady():
    return SendReceive(b'0226') #expect: 80040078F000

def GetSysInfo():
    return SendReceive(b'022B') #expect: 8012000F3F748841CE5902E0FF007F035A107000

# def continuousTagScan():
# 	result = []
# 	tagDetected = False
# 	try:
# 		while (tagDetected == False): #loop forever until tag found
# 			result = STCmd(b'01070E0A21007901180020606064743F08') #wake up event due to tag presence. Not found? FD102 returned
# 			if (result[1] == '000102'):
# 				if (lookForTag() == True): #Scan specifically on 15693 protocol.
# 					tagDetected = True
# 					return tagDetected #return tag found, end loop.
				
# 	except KeyboardInterrupt:
# 		print("Scanning cancelled.")
# 		return False #tag not found.

# def lookForTag(): #look for generic tag - no specific protocol...
# 	#Assign constants to hex values later...
# 	#Also maybe check responses from each command from IC?
# 	t0 = time.time()
# 	found = False
# 	while (found == False):
# 		pollVal = [] #Clear pointers passed into commands.
# 		ReceiveVal = []

# 		if (time.time() - t0 > 5): #Timeout after 5 seconds of detecting generic tag.
# 			break

# 		echo = Echo() #Establish contact with CR95HF IC.
# 		STCmd(b'01090468010710') #Reset HF2RF
# 		STCmd(b'01090468010700') #Set HF2RF
# 		pollVal = STCmd(b'01070E0B21007901180020606000FF3F01') #CR95HF enters low consumption Wait for Event mode (Hibernate, sleep, tag detection etc)
# 		#pollVal = STCmd(b'01070E0A21007901180020606064743F08') software's generic idle state till woken up by tag or IRQ pin
# 		time.sleep(0.005)
# 		Select(b'010D')
# 		time.sleep(0.005)
# 		STCmd(b'02A00126')
# 		time.sleep(0.005)
# 		ReceiveVal = SendReceive(b'0226') #Reset to ready. If response of 8700, no tag.
		
# 		if (pollVal[1] == '000102' and ReceiveVal[0] != 4):
# 			found = True;

# 	if (found):
# 		print(ReceiveVal, "\nFound tag with protocol 15693.")
# 		STCmd(b'01090468010710')
# 		ResetSPI()
# 		Select(b'010D')
# 		return True
# 	else: #unnecessary else?
# 		#print("No tag found.")
# 		return False

def continuousTagScan(): #attempt nr 2
	found = False
	t0 = time.time()
	print("|", end = '')
	while (found == False):
		pollVal = [] #Clear pointers passed into commands.
		ReceiveVal = []

		if (time.time() - t0 > 5): #Timeout after 5 seconds of detecting generic tag.
			print("|")
			break

		if (int(time.time()) > t0):
			print("=", end = '', flush = True)
		echo = Echo() #Establish contact with CR95HF IC.
		STCmd(b'01090468010710') #Reset HF2RF
		STCmd(b'01090468010700') #Set HF2RF
		pollVal = STCmd(b'01070E0B21007901180020606000FF3F01') #CR95HF enters low consumption Wait for Event mode (Hibernate, sleep, tag detection etc)
		#pollVal = STCmd(b'01070E0A21007901180020606064743F08') software's generic idle state till woken up by tag or IRQ pin
		time.sleep(0.005)
		Select(b'010D')
		time.sleep(0.005)
		STCmd(b'02A00126')
		time.sleep(0.005)
		ReceiveVal = SendReceive(b'0226') #Reset to ready. If response of 8700, no tag.
		
		if (pollVal[1] == '000102' and ReceiveVal[0] != 4):
			found = True;
			print("|")

	if (found):
		print("Found a flipping tag.")
		return True
	else:
		print("big oof. No tag.")
		return False

def idleForTag(): #taghunting just using command from software in CR95HF commands tab.
		found = False
		pollVal = STCmd(b'01070E0A21007901180020606064743F08')
		return pollVal

def tagHunting(): #Loop for 5 seconds looking for tag. Field off before and after?
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

def elapsedTime(t0):
	t1 = time.time()
	return t1 - t0

def autoScanAndLog(dict, block = '2'): #Stores readings into dictionary with time of read. Optional: Specify location to read.
    #Start scanning for tags, and read if found. Uses toggle boolean to see if its been found, must only read when it has been found AGAIN.
	readAlready = False
	try:
		while True: #maybe add SendReceive first, then when its time to load, Read_Block (Double check)
			response = Read_Block(block) #ping tag by just trying to read - throws error code if cannot read ie not in range.
			if (response[0] != 0): #If no response from tag ie. not found (error code of 4 for bad communication)
				readAlready = False
			if (response[0] == 0 and readAlready == False): #If tag found
				data = extractPayload(response[1])
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

def ScanAndWrite(block = '2', data = '00000000'): #Can specify what to write and to where.
    #scan continuously for tag writing to, and loop until successful write.
	found = False
	written = False
	try:
		while (written == False):
			response = SendReceive() #ping tag by just trying to read - throws error code if cannot read ie not in range.
			if (response[0] == 0):
				attempt = Write_Block(block, data)
				if (attempt[0] == 0):
					written = True
					response = Read_Block(block)
					#print("Successful write: ", response[1])
					return response
	except KeyboardInterrupt:
		print("\nScanning cancelled.")

def extractPayload(reading): #80080000000005DA9801 OR 80080069696969297A00 position 6 to 13 has payload
	return reading[6:14]

def cleanRegisters():
	for i in range(128):
		val = decToHex(i)
		response = ScanAndWrite(val)
		if (response[0] != 0):
			print("Error cleaning register", val)
	print("Completed.")

def decToHex(dec):
	# Dec to Hex => hex(dec) ==> 0x001 ==> prepHex(hex(dec)) = 001
	return str(hex(int(dec)))[2:] #cut off front two values, return string form.

def prepWrite(dec):
	val = str(decToHex(dec))
	length = 8 - len(val)
	return length * '0' + val.upper() #Can also use z.fill(8)

def hexToDec(hex): #Convert a hex value either 0x0000 or just 0000 (base 16) to decimal (base 10) read in as string
    return int(hex, 16)

def stringToHex(string):
	# ASCII to hex ==> prepHex(hex(ord(ASCII)))
	return hex(string)[2:] #cut off front two values

def hexToString(hex): #Assumes input is string
    return hex.decode("hex")


    	
    
