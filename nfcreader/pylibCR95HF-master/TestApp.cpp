/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************

* File Name        : TestApp.cpp

* Author           : IMS Systems Lab & Technical Marketing

* Version          : 1.0

* Date             : 17th May, 2014

* Description      : To test CR95HF library on linux platform

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


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "libcr95hf.h"
#include "TestApp.h"

//User menu: exit emulator
#define		exit_cmd			'0'

//User menu: To test the library
#define		DEMO_CR95HF_A_USBconnect_cmd	'a'
#define		Get_MCU_rev_cmd			'b'		
#define		Echo_cmd			'c'
#define		Idn_cmd				'd'
#define		Select_ISO15693_cmd		'e'
#define		Send_ISO15693_Inventory_cmd	'f'
#define		ReadBlock_cmd			'r'
#define		WriteBlock_cmd			'w'
#define		FieldOff_cmd			'g'
#define		ResetSPI_cmd			'h'
#define		Send_IRQ_Pulse_cmd		'i'
#define		Get_Interface_Pin_State_cmd	'j'
#define		Send_NSS_Pulse_cmd		'k'
#define		STCmd_ISO15693_cmd		'l'






//char entry=0;
int main ()
{
	char entry=0;	

	do
	{
		printf("\n");
		printf("\n");
		printf("\n---------------------------------------------------");
		printf("\n-                USER MENU release %s           -", release_xy);
		printf("\n---------------------------------------------------");

		printf("\n");	
		
		printf("\n  %c)   -> CR95HFlib_USBConnect : DEMO-CR95HF-A USB connection  <-- TBD 1st ", DEMO_CR95HF_A_USBconnect_cmd);
		
		//printf("\n");
		printf("\n  %c)   -> CR95HFlib_MCUVer : get MCU revision",Get_MCU_rev_cmd);
		//printf("\n");
		printf("\n  %c)   -> CR95HFDll_Echo : send Echo command",Echo_cmd);
		//printf("\n");	
		printf("\n  %c)   -> CR95HFlib_Idn : send Idn command",Idn_cmd);
		//printf("\n");		
		printf("\n  %c)   -> CR95HFlib_Select : select ISO15693 protocol",Select_ISO15693_cmd);
		//printf("\n");		
		printf("\n  %c)   -> CR95HFlib_SendReceive : send ISO15693 Inventory request",Send_ISO15693_Inventory_cmd);
		//printf("\n");	
		printf("\n  %c)   -> CR95HFlib_Read_Block : Read data of user entered block",ReadBlock_cmd);
		//printf("\n");	
		printf("\n  %c)   -> CR95HFlib_Write_Block : write 4 byte data into block",WriteBlock_cmd);
		//printf("\n");
		printf("\n  %c)   -> CR95HFlib_FieldOff : send Field Off request ",FieldOff_cmd);
		//printf("\n");		
		printf("\n  %c)   -> CR95HFlib_ResetSPI : reset SPI",ResetSPI_cmd);
		//printf("\n");		
		printf("\n  %c)   -> CR95HFlib_SendIRQPulse : send IRQ pulse",Send_IRQ_Pulse_cmd);	
		//printf("\n");		
		printf("\n  %c)   -> CR95HFlib_getInterfacePinState : get interface pin state",Get_Interface_Pin_State_cmd);
		//printf("\n");	
		printf("\n  %c)   -> CR95HFlib_SendNSSPulse : send NSS pulse",Send_NSS_Pulse_cmd);	
		//printf("\n");		
		printf("\n  %c)   -> CR95HFlib_STCmd : ISO15693 Protocol Select through STCmd",STCmd_ISO15693_cmd);
		//printf("\n");		
		/*printf("\n  %c)   -> CR95HFlib_Polling_Reading : Polling Reading state",Set_Polling_Reading_config_cmd);
		//printf("\n");	*/
		printf("\n");
		printf("\n  %c)   -> Exit\n\n", exit_cmd);
		printf("your choice:?");
		scanf("%c", &entry);  

		switch (entry)
		{

		case exit_cmd:
			break;			

		case DEMO_CR95HF_A_USBconnect_cmd: 
			{
				Device_Connect();
			}; break;

		case Get_MCU_rev_cmd:
			{
				Get_MCU_rev();
			}; break;
		case Echo_cmd:
			{
				Echo();
			}; break;

		case FieldOff_cmd:
			{
				FieldOff();
			};break;
		case Idn_cmd:
			{
				Idn();
			};break;
		case Select_ISO15693_cmd:

			{
				Select_ISO15693();
			}; break;
		case Send_ISO15693_Inventory_cmd:
			{

				Send_ISO15693_Inventory();
			}; break;
		case ReadBlock_cmd:
			{
				Read_Block();
			}; break;

		case WriteBlock_cmd:
			{
				Write_Block();
			}; break;
		case ResetSPI_cmd:
			{
				Reset_SPI();
			}; break;

		case Send_IRQ_Pulse_cmd:
			{
				Send_IRQPulse();
			}; break;

		case Get_Interface_Pin_State_cmd:
			{
				Get_InterfacePinState();
			}; break;
		
		case Send_NSS_Pulse_cmd:
			{
				Send_NSS_Pulse();
			}; break;

		case STCmd_ISO15693_cmd:
			{
				STCmd_ISO15693();
			}; break;
		}
	} while (entry!='0');
return 0;
}

void Device_Connect()
{
	char entry3;	
	int iResult;
	iResult=CR95HFlib_USBConnect();
	printf("\n Establishing CR95HR Reader connection through USB \n");
	printf("\n --> Library function call : CR95HFlibUSB_Connect() \n");
	printf("\n <-- Return from Library function : 0X%x \n",iResult);

	  if (iResult == 0) 
			printf("\n SUCCESS : Board connected successfully and ready to use \n");
	  else
			printf("\n ERROR : Connection failed \n");
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

}

void Get_MCU_rev ()
{

  char strAnswer[50]="";
  int iresult;
  char entry3;	 

  iresult = CR95HFlib_MCUVer(strAnswer);
  printf("\n Get MCU Version request is sent \n");
  printf("\n --> Library function call : CR95HFlibUSB_MCUVer(strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	

  if (iresult == 0) 
	{		
		printf("\n SUCCESS: MCU Version Reply=%s \n", strAnswer);
	} 
		
  else
	{
		printf("\n ERROR : Get MCU Version Failed \n");
	}

  
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

}

void Echo ()
{
  char strAnswer[50]="";
  char entry3;	 
  printf("\n Echo command sent to MCU \n");
  int iresult= CR95HFlib_Echo (strAnswer);	
  printf("\n --> Library function call : CR95HFlib_Echo (strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	
  
  if (iresult == 0) 
			printf("\n SUCCESS : Echo command answer = %s \n", strAnswer);
	  else
			printf("\n ERROR : Echo command failed, no answer \n");


  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);
  
}


void FieldOff ()
{
  int iresult;
  char strAnswer[50]="";
  char entry3;	
  printf("\n FieldOff command is sent \n"); 
  iresult= CR95HFlib_FieldOff (strAnswer);
  printf("\n --> Library function call : CR95HFDll_FieldOff(strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	  


  if (iresult == 0) 
		printf("\n SUCCESS : RF Field Off ok = %s \n", strAnswer);
		
  else
		printf("\n ERROR : RF Field Off command error %s \n",strAnswer);
		

  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);
  

}

void Idn ()
{
  int iresult;
  char strAnswer[50]="";
  char entry3;	 
  printf("\n IDN command is sent \n");
  
  iresult= CR95HFlib_Idn (strAnswer);	
  printf("\n --> Library function call : CR95HFlib_Idn (strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	
  
  if (iresult == 0) 
		printf("\n SUCCESS : Idn command response = %s \n", strAnswer);		
  else
		printf("\n ERROR : no Idn returned %s \n",strAnswer);
		

  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

	
}



void Select_ISO15693 ()
{
  int iresult;
  char strRequest[50]="";
  char strAnswer[50]="";
  
  char entry3;	 

  printf("\n ISO 15693 Protocol selection for future NFC communication:\n");
  
  strcpy(strRequest,"010D");

  iresult = CR95HFlib_Select(strRequest ,strAnswer);
  printf("\n --> Library function call : CR95HFlib_Select(strRequest ,strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	
  

  if (iresult == 0) 
		printf("\n SUCCESS : ISO15693 protocol selected : Answer Received=%s \n", strAnswer);
  else
		printf("\n ERROR : ISO15693 protocol selection failed :No Answer Received %s \n", strAnswer);

 
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);
 
}



void Send_ISO15693_Inventory ()
{
  int iresult;
  char strRequest[50]="";
  char strTagAnswer[50]="";  
  char entry3;	 

  
  strcpy(strRequest,"260100");

 iresult=CR95HFlib_SendReceive(strRequest,strTagAnswer);
  
  printf("\nISO15695 inventory using CR95HF SendReceive command:\n");
  printf("\n --> Library function call : CR95HFlib_Select(260100 ,strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	


  if ((strTagAnswer[0] == '8') & (strTagAnswer[1] == '0')) //CR95HF Tag answer OK
  {
	printf("\n SUCCESS : Tag answer=%s \n",strTagAnswer);	
  }
  else
  {
	printf("\n ERROR : No tag answer received %s \n",strTagAnswer);
  }	

  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);  	

}


void Read_Block()
{
  char entry3;	
  unsigned char strTagAnswer[50]="";  
  int RegAdd=0;
  printf("\n This option will read 4 byte data of the block entered by user \n");
  printf("\n");
  printf("\n please enter the Block address in hex \n");
  printf("\n");
  scanf("%x", (int*)&RegAdd); 
  int r = CR95HFlib_Read_Block(RegAdd, strTagAnswer);
  printf("\n --> Library function call : CR95HFlib_Read_Block(RegAdd, strTagAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",r);	
	if(r==0)
	{
		printf("\n SUCCESS : Received Tag answer=%s \n",strTagAnswer);	

		for(int i=3;i<=6;i++)
		{
		 printf("%x",(int)strTagAnswer[i]);
		 printf(" ");
		} 
	}
	else
	{
		printf("\n ERROR : No tag answer received %s \n",strTagAnswer);
	}

  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);  	

}

void Write_Block()
{
  char entry3;	
  unsigned char strBytestowrite[50]="";  
  unsigned char strTagAnswer[50]="";  
  int WriteAdd;
  printf("\n This option will write 4 bytes of data entered by user into the selected block\n");
  printf("\n");
  printf("\n please enter the Block address in hex");
  printf("\n");
  scanf("%x", (int*)&WriteAdd); 
  
  printf("\n enter first byte \n");
  scanf("%x",(int*)&strBytestowrite[0]);
  printf("\n enter second byte \n");
  scanf("%x",(int*)&strBytestowrite[1]);
  printf("\n enter third byte \n");
  scanf("%x",(int*)&strBytestowrite[2]);
  printf("\n enter fourth byte \n");
  scanf("%x",(int*)&strBytestowrite[3]);
  printf("\n");
  int r = CR95HFlib_Write_Block(WriteAdd, strTagAnswer,strBytestowrite);

  printf("\n --> Library function call : CR95HFlib_Write_Block(WriteAdd, strTagAnswer,strBytestowrite) \n");
  printf("\n <-- Return from Library function : 0X%x \n",r);	
	
  if(r==0)
	{
		printf("\n SUCCESS : Data written into the block successfully %s\n",strTagAnswer);	
		
	}
	else
	{
		printf("\n ERROR : data write on block is failed \n");
	}

  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3); 
}


void Reset_SPI ()
{

  char strAnswer[50]="";
  int iresult;
  char entry3;	 

  iresult = CR95HFlib_ResetSPI(strAnswer);
  printf("\n Reset_SPI request is sent \n");
  printf("\n --> Library function call : CR95HFlib_ResetSPI(strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	

  if (iresult == 0) 
	{		
		printf("\n SUCCESS: Reset SPI successfully,Answer received= %s \n", strAnswer);
	} 
		
  else
	{
		printf("\n ERROR : Reset SPI failed, No answer received\n");
	}

  
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

}

void Send_IRQPulse ()
{

  char strAnswer[50]="";
  int iresult;
  char entry3;	 

  iresult = CR95HFlib_SendIRQPulse(strAnswer);
  printf("\n Send IRQPulse request is sent \n");
  printf("\n --> Library function call : CR95HFlib_SendIRQPulse(strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	

  if (iresult == 0) 
	{		
		printf("\n SUCCESS: Send IRQPulse completed successfully,Answer received= %s \n", strAnswer);
	} 
		
  else
	{
		printf("\n ERROR : Send IRQPulse failed, No answer received\n");
	}

  
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

}

void Get_InterfacePinState ()
{

  char strAnswer[50]="";
  int iresult;
  char entry3;	 

  iresult = CR95HFlib_getInterfacePinState(strAnswer);
  printf("\n Request for getInterfacePinState is sent \n");
  printf("\n --> Library function call : CR95HFlib_getInterfacePinState(strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	

  if (iresult == 0) 
	{		
		printf("\n SUCCESS: getInterfacePinState completed successfully,Answer received= %s \n", strAnswer);
                if(strAnswer[3]=='0')
			{
				printf("\n  Communication is in UART mode \n");
			}
		else
			{
				printf("\n  Communication is in SPI mode \n");
			}
	} 
		
  else
	{
		printf("\n ERROR : getInterfacePinState failed, No answer received\n");
	}

  
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

}


void Send_NSS_Pulse ()
{

  char strAnswer[50]="";
  int iresult;
  char entry3;	 

  iresult = CR95HFlib_SendNSSPulse(strAnswer);
  printf("\n Request for Send NSS_Pulse \n");
  printf("\n --> Library function call : CR95HFlib_SendNSSPulse(strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	

  if (iresult == 0) 
	{		
		printf("\n SUCCESS: Send NSS pulse successfully,Answer received= %s \n", strAnswer);
	} 
		
  else
	{
		printf("\n ERROR : Send NSS Pulse failed, No answer received\n");
	}

  
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

}


void STCmd_ISO15693()
{

  char strRequest[50]="";
  char strAnswer[50]="";
  int iresult;
  char entry3;	 
//  strcpy(strRequest,"010202010D");
//  strcpy(strRequest,"010202020D");
//  strcpy(strRequest,"0102020105\0");
  strcpy(strRequest,"010803620100\0");
	printf("\nout:%s",strRequest);
  iresult = CR95HFlib_STCmd(strRequest,strAnswer);
  printf("\n ISO15693 Protocol select using CR95HFlib_STCmd function \n");
  printf("\n --> Library function call : CR95HFlib_STCmd(strRequest,strAnswer) \n");
  printf("\n <-- Return from Library function : 0X%x \n",iresult);	

  if (iresult == 0) 
	{		
		printf("\n SUCCESS: ISO15693 protocol is selected through STCmd, Answer received= %s \n", strAnswer);
	} 
		
  else
	{
		printf("\n ERROR : ISO15693 protocol select through STCmd failed, Answer received= %s \n", strAnswer);
	}

  
  printf("\n Selected Task is completed, To proceed for another task put your choice");
  printf("\n");
  scanf("%c", &entry3);

}


/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************/
	
