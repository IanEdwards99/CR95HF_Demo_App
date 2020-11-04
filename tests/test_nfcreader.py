#!/usr/bin/env python
# Authors: Ian Edwards and Agoritsa Spirakis
# MIT License
# PyTests for nfcreader API for CR95HF module.
"""Tests for `nfcreader` package."""

import pytest
import sys

from nfcreader import nfcreader as nfc

def test_USBConnect():
    x = nfc.USBConnect()
    assert x == 1, "Error with USBConnect."

def test_Echo():
    """Test Echo function"""
    x= nfc.Echo()
    assert x[0] == 5, "Echo test failed, MCU response: " + str(x[0])

def test_MCUrev():
    x = nfc.MCUrev()
    assert x[0] == 5, "MCUrev test failed, response: " + str(x[0])

def test_getInterfacePinState():
    x = nfc.getInterfacePinState()
    assert x[0] == 5, "InterefacePinState fetch test failed, response: " + str(x[0])

def test_ReadBlock():
    x = nfc.Read_Block("a")
    assert x[0] == "9", "ReadBlock fetch test failed, response: " + str(x[0])

def test_SendReceive():
    x = nfc.SendReceive()
    assert x[0] == 5, "SendReceive fetch test failed, response: " + str(x[0])

def test_Select():
    x = nfc.Select()
    assert x[0] == 5, "Select fetch test failed, response: " + str(x[0])

def test_Write_Block():
    x = nfc.Write_Block("a")
    assert x[0] == "9", "Write_Block fetch test failed, response: " + str(x[0])

def test_Idn():
    x = nfc.Idn()
    assert x[0] == 5, "Idn test failed, response: " + str(x[0])

def test_FieldOff():
    x = nfc.FieldOff()
    assert x[0] == 5, "FieldOff test failed, response: " + str(x[0])

def test_ResetSPI():
    x = nfc.ResetSPI()
    assert x[0] == 5, "ResetSPI test failed, response: " + str(x[0])
    
def test_SendIRQPulse():
    x = nfc.SendIRQPulse()
    assert x[0] == 5, "SendIRQPulse test failed, response: " + str(x[0])
    
def test_SendNSSPulse():
    x = nfc.SendNSSPulse()
    assert x[0] == 5, "NSSPulse test failed, response: " + str(x[0])

def test_STCmd():
    x = nfc.STCmd()
    assert x[0] == 5, "STCmd test failed, response: " + str(x[0])
    
def test_initiate():
    x = nfc.initiate()
    assert x[0] == 5, "initiate test failed, response: " + str(x[0])

def test_ResetToReady():
    x = nfc.ResetToReady()
    assert x[0] == 5, "ResetToReady test failed, response: " + str(x[0])

def test_GetSysInfo():
    x = nfc.GetSysInfo()
    assert x[0] == 5, "GetSysInfo test failed, response: " + str(x[0])
    
def test_idleForTag():
    x = nfc.idleForTag()
    assert x[0] == 5, "idleForTag test failed, response: " + str(x[0])

def test_tagHunting():
    x = nfc.tagHunting()
    assert x == False, "tagHunting test failed, response: " + str(x)

def test_extractPayload():
    x = nfc.extractPayload("80080000000005DA9801")
    assert x == "00000005", "extractPayload test failed, response: " + x

def test_dec2Hex():
    x = nfc.decToHex("400")
    assert x == "190", "Dec to Hex test failed, response: " + x

def test_hexToDec():
    x = nfc.hexToDec("190")
    assert x == 400, "hexToDec test failed, response: " + str(x)
    






