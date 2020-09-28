/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************

* File Name        : HIDManager.cpp

* Author           : IMS Systems Lab & Technical Marketing

* Version          : 1.0

* Date             : 17th May, 2014

* Description      : HID support for CR95HF on Linux platform

********************************************************************************

* THE PRESENT SOFTWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS

* WITH PRODUCT CODING INFORMATION TO SAVE TIME.

* AS A RESULT, STMICROELECTRONICS SHALL NOT BE HELD LIABLE FOR ANY DIRECT,

* INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING FROM THE

* CONTENT OF THE SOFTWARE AND/OR THE USE MADE BY CUSTOMERS OF THE CODING

* INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.

* THIS SOURCE CODE IS PROTECTED BY A LICENSE AGREEMENT.

* FOR MORE INFORMATION PLEASE READ CAREFULLY THE LICENSE AGREEMENT FILE LOCATED

* IN THE ROOT DIRECTORY OF THIS SOFTWARE PACKAGE.

*******************************************************************************/


#include <libusb-1.0/libusb.h>
#include <string.h>
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <libusb-1.0/libusb.h>
#include "HIDManager.h"

using namespace std;

//productID and vendorID for customer's CR95HF board
const int VendorID = 0x0483;
const int ProductID =  0xd0d0;

const unsigned char OutEP=0x03;//OUT Endpoint for datatransfer
const unsigned char InEP=0x83;//IN Endpoint for datatransfer

const int timeoutValue=1000; //timeout (in millseconds) for that the transfer function should wait before giving up due to no response being received. For an unlimited timeout, use value 0.

const int MAX_DATA_SIZE=64;


bool Ccr95HIDManager::MakeDeviceReady()
{
	bool IsSuccess=true;;
	IsReadyforCommunication=false;	
	int r;//result

	//First open libusb session	 
	 r = libusb_init(&libusbSession); //initialize a library session
	 if(r<0)
	 {
		 //Issue in session creation
		 cout<<"Issue in libusb session creation"<<endl;
		 
		 return false;
	 }
	 //After successful session creation open device handle
    libusbDevHandle=libusb_open_device_with_vid_pid(libusbSession, VendorID, ProductID); //these are vendorID and productID
	if(libusbDevHandle == NULL)
	 {
		 cout<<"Cannot Open device, check the connection"<<endl;
		 return false;
	 }
	 libusb_set_debug(libusbSession, 3); //set verbosity level to 3, as suggested in the documentation

       //find out if kernel driver is attached with this particular HID device
	if(libusb_kernel_driver_active(libusbDevHandle, 1) == 1) 
	{ 
		
		libusb_detach_kernel_driver(libusbDevHandle, 1);  //detach it
		
	}
	//Claim the interface now with this driver
	r = libusb_claim_interface(libusbDevHandle, 1); //claim interface 0
	if(r < 0) 
	{
		cout<<"Cannot Claim Interface"<<endl;
		return false;
	}
		
	IsReadyforCommunication=true;	

	return IsSuccess;
}

bool Ccr95HIDManager::WriteToDevice(unsigned char* datatowrite,int sizeofDatatoWrite)
{
	int actualwritten;
	bool isSuccess;
	int result = libusb_interrupt_transfer(libusbDevHandle,OutEP, datatowrite,sizeofDatatoWrite , &actualwritten,timeoutValue ); 
	if(result==0)
	{
		if(actualwritten==sizeofDatatoWrite)
		{
			//cout<<"Data is written to the device successfully "<<endl;
			isSuccess=true;
		}
	}
	else
	{
		cout<<"write to device failed"<<endl;
		isSuccess=false;
	}
	return isSuccess;

}

bool Ccr95HIDManager::ReadFromDevice(unsigned char* receiveddata,int sizeofDatatoRead)
{
	int actualdataRead;
	bool isSuccess;	
	int result = libusb_interrupt_transfer(libusbDevHandle,InEP, receiveddata,MAX_DATA_SIZE, &actualdataRead,timeoutValue ); 
	if(result==0)
	{		
		//cout<<"Data is raed from the device successfully "<<endl;
		isSuccess=true;	
	}
	else
	{
		cout<<"Process to read data from device is failed"<<endl;
		isSuccess=false;
	}
	return isSuccess;

}

bool Ccr95HIDManager::Close_Device()
{
	bool IsSuccess=true;
	// free the resources
	int r = libusb_release_interface(libusbDevHandle, 1); //release the claimed interface

	if(r!=0) 
	{
	cout<<"Cannot Release Interface"<<endl;
	return false;
        }
    	cout<<"Released Interface"<<endl;

	libusb_close(libusbDevHandle); //close the device we opened

	libusb_exit(libusbSession); //close the session

	return IsSuccess;

}


/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************/

