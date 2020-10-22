/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************

* File Name        : libcr95hf.cpp

* Author           : IMS Systems Lab & Technical Marketing

* Version          : 1.0

* Date             : 17th May, 2014

* Description      : CR95HF library on Linux

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

#include <HIDManager.h>
#include <string.h>
#include <stdio.h>
/* HID Commands */
# define ID_SPI_SEND_DATA		0x01
# define ID_SEND_request_to_MCU 0x02
# define ID_SEND_HID_RESPONSE	0x07 

/* CR95HF Commands */
#define IDN				        0x01
#define SELECT			        0x02
#define POLL			        0x03
#define SENDRECEIVE		        0x04
#define LISTEN			        0x05
#define SEND			        0x06
#define ECHO			        0x55

/* CR95 Demo Reader Errors returned on commands */
#define STM32_error             0x01
#define empty_argument_error    0x02
#define cmd_parameter_error     0x03
#define communication_error     0x04
#define STM32_connection_error  0x05

/* Max buffer size = 256 data bytes + 2 cmd bytes */
#define MAX_BUFFER_SIZE	64 

int Hex2Asc(char*,unsigned char*,int);
int Asc2Hex(unsigned char *,char *,int);


Ccr95HIDManager mgrObj;



int CR95HFlib_Idn(unsigned char* Reply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE], RespArray[MAX_BUFFER_SIZE];
	
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else {
		CmdArray[0] = ID_SPI_SEND_DATA;
		CmdArray[1] = IDN;
		CmdArray[2] = 0x00;
		/* Transmits the command */
		mgrObj.WriteToDevice(CmdArray,3);//size of data to write should not be hardcoded ??
		/* Recovers the reply */
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);
		
		return 0 ; 
	}
}

int CR95HFlib_USBConnect()
{
	
	bool isSuccess=mgrObj.MakeDeviceReady();
	if(isSuccess)
	{
		
		return 0;
	}
	else
	{
		return STM32_error;
	}
}

int CR95HFlib_MCUVer(char* StringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE];
        unsigned char RespArray[MAX_BUFFER_SIZE];
		
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else
	{
		CmdArray[0]= ID_SEND_request_to_MCU;	
		CmdArray[1]= 0xBC;
		// Transmits the command 
		mgrObj.WriteToDevice(CmdArray,2);//size of data to write should not be hardcoded ??
		// Recovers the reply 
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);		
		
		Hex2Asc(StringReply,&RespArray[1],RespArray[2]+2);
		return 0;
					
	}
}

int  CR95HFlib_Echo(char* StringReply)
{
	
	unsigned char CmdArray[MAX_BUFFER_SIZE], RespArray[MAX_BUFFER_SIZE];
	 
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error ;
    	}


    else
	{
		CmdArray[0] = ID_SPI_SEND_DATA;
		CmdArray[1] = ECHO;
		/* Transmits the command */		
		mgrObj.WriteToDevice(CmdArray,2);//size of data to write should not be  ??
		
		/* Recovers the reply */
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);
		Hex2Asc(StringReply,&RespArray[1],RespArray[2]+2);		
		return 0;
	}
}

int CR95HFlib_FieldOff(char* StringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE], RespArray[MAX_BUFFER_SIZE];
	
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else{
		CmdArray[0] = ID_SPI_SEND_DATA;
		CmdArray[1] = SELECT;
		CmdArray[2] = 0x02;
		CmdArray[3] = 0x00;
		CmdArray[4] = 0x00;
		/* Transmits the command */
		mgrObj.WriteToDevice(CmdArray,5);
		/* Recovers the reply */
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);
		/* Converts Hexa to Ascii */
		Hex2Asc(StringReply, &RespArray[1], RespArray[2] + 2);
		return 0 ; 
	}
}

int  CR95HFlib_Idn(char *StringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE], RespArray[MAX_BUFFER_SIZE];
	
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else {
		CmdArray[0] = ID_SPI_SEND_DATA;
		CmdArray[1] = IDN;
		CmdArray[2] = 0x00;
		/* Transmits the command */
		mgrObj.WriteToDevice(CmdArray,3);
		/* Recovers the reply */
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);
		/* Converts Hexa to Ascii */
		Hex2Asc(StringReply, &RespArray[1], RespArray[2] + 2);
		return 0 ; 
	}
}


int  CR95HFlib_Select(char* StringCmd, char* StringReply)  //select protocol
{
		
	unsigned char CmdArray[MAX_BUFFER_SIZE], RespArray[MAX_BUFFER_SIZE], RespCode;
	
	
	    
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}

	else 
	{
		// Checks if the string is empty 
		if(strlen(StringCmd) == 0)
			{
			// An error occured 
			return empty_argument_error ;
			}
		else
		{
			CmdArray[0] = ID_SPI_SEND_DATA;
			CmdArray[1] = SELECT;
			CmdArray[2] = strlen(StringCmd)/2;//??
			// append passed string to the command array
			Asc2Hex(&CmdArray[3],StringCmd,strlen(StringCmd));	
		
			/* Transmits the command */
			mgrObj.WriteToDevice(CmdArray,strlen(StringCmd)+3);//??	
			/* Recovers the reply */
			mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);
			RespCode = RespArray[1];
			if(RespCode != 0x00)
			{ 
				if (RespCode == 0x82)
				{
					strcpy(StringReply , "8200 : Invalid command length");
				}
				else if ( RespCode == 0x83 ) 
				{
					strcpy(StringReply , "8300 : Invalid protocol");
				} 

				return cmd_parameter_error ; 
			}
			else
				{
					Hex2Asc(StringReply, &RespArray[1], RespArray[2] + 2);
					return 0 ; 
				}
		}//end else
	
	}//End else

} 

int  CR95HFlib_SendReceive(char *StringCmd, char *StringReply) 
{

	unsigned char CmdArray[MAX_BUFFER_SIZE], RespArray[MAX_BUFFER_SIZE], RespCode;

	    
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else
	{
		
		if(strlen(StringCmd) == 0)
			{
			CmdArray[0] = ID_SPI_SEND_DATA;
			CmdArray[1] = SENDRECEIVE;
			CmdArray[2] = 0x0;
			}
		else	{ 
			CmdArray[0] = ID_SPI_SEND_DATA;
			CmdArray[1] = SENDRECEIVE;
			CmdArray[2] = strlen(StringCmd)/2;
			
			Asc2Hex(&CmdArray[3] , StringCmd, strlen(StringCmd));
			}
			
		mgrObj.WriteToDevice(CmdArray,CmdArray[2]+3);//??	
			
			
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);
			
		RespCode = RespArray[1];
		if((RespCode != 0x80) && (RespCode != 0x90))
			{ 
				if ( RespCode == 0x86 ) 
					{
					strcpy(StringReply , "8600 : Communication error");
					} 
				else if ( RespCode == 0x87 ) 
					{
					strcpy(StringReply , "8700 : Frame wait time out OR no tag");
					} 
				else if ( RespCode == 0x88 ) 
					{
					strcpy(StringReply , "8800 : Invalid Start Of Frame");				
					} 
				else if ( RespCode == 0x89 ) 
					{
					strcpy(StringReply , "8900 : Receive buffer overflow (too many bytes received)");
					} 

				else if ( RespCode == 0x8A ) 
					{
					strcpy(StringReply , "8A00: Framing error (start bit=0, stop bit=1)");
					} 
				else if ( RespCode == 0x8B ) 
					{
					strcpy(StringReply , "8B00 : EGT time out (for Iso14443-B)");				
					} 
				else if ( RespCode == 0x8C ) 
					{
					strcpy(StringReply , "8C00 : Invalid length. Used in Felica, when field Length < 3");
					} 
				else if ( RespCode == 0x8D ) 
					{
					strcpy(StringReply , "8D00 : CRC error (Used in Felica protocol)");
					} 
				else if ( RespCode == 0x8E ) 
					{
					strcpy(StringReply , "8E00 : Reception lost without EOF received");	
					} 
				else 
					{
					strcpy(StringReply , "Unknow error");
					//StringReply = "Unknow error";  //?? why it didnt work
					}
				return communication_error ; 
			}
		else
			{
				
				Hex2Asc(StringReply, &RespArray[1], RespArray[2] + 2);
				return 0; 
			}
	} 	
}




int CR95HFlib_Read_Block(int RegAdd, unsigned char* DataReceived)

{
char arrReceived[MAX_BUFFER_SIZE];
char cmdRead[40];

unsigned char nibbleArr[4];

//char cmdArray[40];

unsigned char maskReg1 = 0XF0;

unsigned char maskReg2 = 0X0F;

unsigned char arrbyte[2];

arrbyte[0]=(
unsigned char)RegAdd;

arrbyte[1]=(
unsigned char)(RegAdd>>8);

nibbleArr[0] = (
unsigned char)((arrbyte[0] & maskReg1) >> 4);

nibbleArr[1] = (
unsigned char)(arrbyte[0] & maskReg2);

nibbleArr[2] = (
unsigned char)((arrbyte[1] & maskReg2) >> 4);

nibbleArr[3] = (
unsigned char)(arrbyte[1] & maskReg2);

cmdRead[0] =
'0';

cmdRead[1] =
'A';

cmdRead[2] =
'2';

cmdRead[3] =
'0';

int i,j;
for (j = 4, i = 0; j <= 7; j++, i++)
{
	char hexVal = ' ';
	if (nibbleArr[i] < 10)
	{
		hexVal=nibbleArr[i]+48;
	}
	else 
	{
		hexVal=nibbleArr[i]+55;
	}
cmdRead[j] = hexVal;		
}
cmdRead[j]=0;


// send command to get data

int istatus = CR95HFlib_SendReceive(cmdRead, arrReceived);
Asc2Hex(DataReceived , arrReceived, strlen(arrReceived));

return istatus;

}

int CR95HFlib_Write_Block(int RegAdd, unsigned char* strTagAnswer,unsigned char* strBytestowrite)
{
char arrReceived[MAX_BUFFER_SIZE];
char cmdWrite[40];

unsigned char nibbleArr[4];

//char cmdArray[40];

unsigned char maskReg1 = 0XF0;

unsigned char maskReg2 = 0X0F;

unsigned char arrbyte[2];

arrbyte[0]=(
unsigned char)RegAdd;

arrbyte[1]=(
unsigned char)(RegAdd>>8);

nibbleArr[0] = (
unsigned char)((arrbyte[0] & maskReg1) >> 4);

nibbleArr[1] = (
unsigned char)(arrbyte[0] & maskReg2);

nibbleArr[2] = (
unsigned char)((arrbyte[1] & maskReg2) >> 4);

nibbleArr[3] = (
unsigned char)(arrbyte[1] & maskReg2);

cmdWrite[0] =
'0';

cmdWrite[1] =
'A';

cmdWrite[2] =
'2';

cmdWrite[3] =
'1';

int i,j;
for (j = 4, i = 0; j <= 7; j++, i++)
{
	char hexVal = ' ';
	if (nibbleArr[i] < 10)
	{
		hexVal=nibbleArr[i]+48;
	}
	else 
	{
		hexVal=nibbleArr[i]+55;
	}
cmdWrite[j] = hexVal;		
}

cmdWrite[j]=0;
Hex2Asc(&cmdWrite[j], strBytestowrite,4);
int istatus = CR95HFlib_SendReceive(cmdWrite, arrReceived);
return istatus;
}

int CR95HFlib_ResetSPI(char* StringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE];
        unsigned char RespArray[MAX_BUFFER_SIZE];
		
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else
	{
		CmdArray[0]= ID_SEND_request_to_MCU;	
		CmdArray[1]= 0xBD;
		// Transmits the command 
		mgrObj.WriteToDevice(CmdArray,2);//size of data to write should not be hardcoded ??
		// Recovers the reply 
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);		
		
		Hex2Asc(StringReply,&RespArray[1],RespArray[2]+2);
		return 0;
					
	}
}

int CR95HFlib_SendIRQPulse(char* StringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE];
        unsigned char RespArray[MAX_BUFFER_SIZE];
		
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else
	{
		CmdArray[0]= ID_SEND_request_to_MCU;	
		CmdArray[1]= 0xBE;
		// Transmits the command 
		mgrObj.WriteToDevice(CmdArray,2);//size of data to write should not be hardcoded ??
		// Recovers the reply 
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);		
		
		Hex2Asc(StringReply,&RespArray[1],RespArray[2]+2);
		return 0;					
	}
}

int CR95HFlib_getInterfacePinState(char* StringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE];
        unsigned char RespArray[MAX_BUFFER_SIZE];
		
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else
	{
		CmdArray[0]= ID_SEND_request_to_MCU;	
		CmdArray[1]= 0xBA;
		// Transmits the command 
		mgrObj.WriteToDevice(CmdArray,2);//size of data to write should not be hardcoded ??
		// Recovers the reply 
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);		
		
		Hex2Asc(StringReply,&RespArray[1],RespArray[2]+2);
		return 0;					
	}
}


int CR95HFlib_SendNSSPulse(char* StringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE];
        unsigned char RespArray[MAX_BUFFER_SIZE];
		
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else
	{
		CmdArray[0]= ID_SEND_request_to_MCU;	
		CmdArray[1]= 0xB9;
		// Transmits the command 
		mgrObj.WriteToDevice(CmdArray,2);//size of data to write should not be hardcoded ??
		// Recovers the reply 
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);		
		
		Hex2Asc(StringReply,&RespArray[1],RespArray[2]+2);
		return 0;					
	}
}





int CR95HFlib_STCmd(char* stringCmd, char* stringReply)
{
	unsigned char CmdArray[MAX_BUFFER_SIZE];
        unsigned char RespArray[MAX_BUFFER_SIZE];
		
	if(!mgrObj.IsReadyforCommunication)
	{
		return STM32_connection_error;
	}
	else
	{
		if(strlen(stringCmd)== 0)
		{
			return empty_argument_error;
		}
		Asc2Hex(&CmdArray[0],stringCmd,strlen(stringCmd));
		
		// Transmits the command 
		mgrObj.WriteToDevice(CmdArray,(strlen(stringCmd))/2);//size of data to write should not be hardcoded ??
		// Recovers the reply 
		mgrObj.ReadFromDevice(RespArray,MAX_BUFFER_SIZE);		
		
		Hex2Asc(stringReply,&RespArray[1],RespArray[2]+2);
		return 0;
					
	}
}




//
/* Hexa to Ascii 0x22 -> "22" */
int Hex2Asc(char *Dest,unsigned char *Src,int SrcLen)
{
	int i;
	for ( i = 0; i < SrcLen; i ++ )
	{
		sprintf(Dest + i * 2,"%02X",Src[i]);
	}
	Dest[i * 2] = 0;
	return 0;
}

/* Ascii to Hexa "22" -> 0x22 */
int Asc2Hex(unsigned char *Dest,char *Src,int SrcLen)
{
	int i;
	for ( i = 0; i < SrcLen / 2; i ++ )
	{
		sscanf(Src + i * 2,"%02X",(unsigned int*)&Dest[i]);
	}
	return 0;
}


/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************/

