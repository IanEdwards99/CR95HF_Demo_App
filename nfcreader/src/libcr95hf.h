/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************

* File Name        : libcr95hf.h

* Author           : IMS Systems Lab & Technical Marketing

* Version          : 1.0

* Date             : 17th May, 2014

* Description      : CR95HF library header

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


extern int CR95HFlib_USBConnect();
extern int CR95HFlib_MCUVer(char* StringReply);
extern int CR95HFlib_Idn(char* );
extern int CR95HFlib_Echo(char*);
extern int CR95HFlib_FieldOff(char*);
extern int CR95HFlib_Select(char*, char*);
extern int CR95HFlib_SendReceive(char*,char*);
extern int CR95HFlib_Read_Block(int,unsigned char*); 
extern int CR95HFlib_Write_Block(int,unsigned char*,unsigned char*);
extern int CR95HFlib_ResetSPI(char*);
extern int CR95HFlib_SendIRQPulse(char*);
extern int CR95HFlib_getInterfacePinState(char*);
extern int CR95HFlib_SendNSSPulse(char*);
extern int CR95HFlib_STCmd(char*, char*);

/******************** (C) COPYRIGHT 2014 STMicroelectronics ********************/
