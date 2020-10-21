#!/usr/bin/python
import ctypes
from ctypes import *
cr95hf = ctypes.CDLL('libCR95HF.so');
import time
#testlib = ctypes.CDLL('./testlib.so');

#>>> Frame sent by the Host to CR95HF
#<<< Frame sent by the CR95HF to the Host

def USBConnect():
	return cr95hf._Z20CR95HFlib_USBConnectv()

def Echo():
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
	
def Idn():
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
    
    

# def Read_Block(block=0):
# 	strAnswer= ctypes.create_string_buffer(b'\000',50)
# 	strRequest=c_uint(block)
# 	res=cr95hf._Z20CR95HFlib_Read_BlockiPh(strRequest,strAnswer)
# 	return (res,strAnswer.value)

# def Write_Block(block, data):
# 	strAnswer= ctypes.create_string_buffer(b'\000',50)
# 	strData= ctypes.create_string_buffer(b'\000',50)
# 	strRequest=c_uint(block)
# 	res=cr95hf._Z21CR95HFlib_Write_BlockiPhS_(strRequest,strAnswer,strData)
# 	return (res,strAnswer.value.decode("utf-8"))


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

def taghunt(): #taghunting just using command from software in CR95HF commands tab.
		found = False
		pollVal = STCmd(b'01070E0A21007901180020606064743F08')
		return pollVal

def anothertaghunt():
	found = False
	t0 = time.time()
	while not(found):
		if (time.time() - t0 > 5): #Timeout after 5 seconds of detecting generic tag.
			break
		response = SendReceive()
		if (response[0] == 0):
			found = True
	if (found):
		print("Found a tag!")
	else:
		print("No tag found.")

def elapsedTime(t0):
	t1 = time.time()
	return t1 - t0
