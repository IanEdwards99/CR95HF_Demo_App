#!/usr/bin/python
import ctypes
from ctypes import *
cr95hf = ctypes.CDLL('libCR95HF.so');
#testlib = ctypes.CDLL('./testlib.so');

#print cr95hf.CR95HFlib_USBConnect()
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
	return (res,strAnswer.value.decode("utf-8"))

def SendReceive(request= b'260100'):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_char_p(request)
	res=cr95hf._Z21CR95HFlib_SendReceivePcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def Read_Block(block=0):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_uint(block)
	res=cr95hf._Z20CR95HFlib_Read_BlockiPh(strRequest,strAnswer)
	return (res,strAnswer.value.decode("utf-8"))

def Write_Block(block, data):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strData= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_uint(block)
	res=cr95hf._Z21CR95HFlib_Write_BlockiPhS_(strRequest,strAnswer,strData)
	return (res,strAnswer.value.decode("utf-8"))


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


def STCmd(request=b'010202010D'):
	strAnswer= ctypes.create_string_buffer(b'\000',50)
	strRequest=c_char_p(request)
	res=cr95hf._Z15CR95HFlib_STCmdPcS_(strRequest,strAnswer)
	return (res,strAnswer.value.decode("utf-8"))
	
