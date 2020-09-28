/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************

* File Name        : HIDManager.h

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

#include <string.h>
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <libusb-1.0/libusb.h>

using namespace std;


//Declaration of class

class Ccr95HIDManager
{
	//Take variable for device handle and libusb session
	//take a static variable to store the libusb session
    	public:
	libusb_context* libusbSession; 
    	libusb_device_handle* libusbDevHandle;

	bool IsReadyforCommunication;
	
	//Is device ready for communication
	bool MakeDeviceReady();

	//WriteToDevice
	bool WriteToDevice(unsigned char* datatowrite,int sizeofDatatoWrite);

	//ReadeFromDevice
	bool ReadFromDevice(unsigned char* receiveddata,int sizeofDatatoRead);
	
	//ReadeFromDevice
	bool Close_Device();

};

/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************/
