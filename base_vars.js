var Boot=99
var AnlagenKWP=103760
var time_start = new Array(8,7,6,6,6,6,6,6,6,7,7,8)
var time_end = new Array(17,18,20,21,21,22,22,21,20,19,17,17)
var sollMonth = new Array(2,6,9,11,11,13,13,12,10,6,4,3)
var SollYearKWP=950
var AnzahlWR = 15
var MaxWRP=new Array(AnzahlWR)
MaxWRP[0]=new Array(8800,70000,1350000,10500000)
MaxWRP[1]=new Array(8800,70000,1350000,10500000)
MaxWRP[2]=new Array(8800,70000,1350000,10500000)
MaxWRP[3]=new Array(8800,70000,1350000,10500000)
MaxWRP[4]=new Array(8800,70000,1350000,10500000)
MaxWRP[5]=new Array(8800,70000,1350000,10500000)
MaxWRP[6]=new Array(8200,65000,1250000,10000000)
MaxWRP[7]=new Array(6900,55000,1050000,8000000)
MaxWRP[8]=new Array(6900,55000,1050000,8000000)
MaxWRP[9]=new Array(6900,55000,1050000,8000000)
MaxWRP[10]=new Array(6900,55000,1050000,8000000)
MaxWRP[11]=new Array(6900,55000,1050000,8000000)
MaxWRP[12]=new Array(5800,45000,900000,7000000)
MaxWRP[13]=new Array(5800,45000,900000,7000000)
MaxWRP[14]=new Array(6900,55000,1050000,8000000)
var WRInfo = new Array(AnzahlWR)
WRInfo[0]=new Array("PAC7","  27103504",7980,1,"WR 1",1,null,null,0,null,14,0,1,1000,null)
WRInfo[0][16]=1
WRInfo[0][17]=1
WRInfo[1]=new Array("PAC7","  29100134",7980,1,"WR 2",1,null,null,0,null,14,0,1,1000,null)
WRInfo[1][16]=1
WRInfo[1][17]=1
WRInfo[2]=new Array("PAC7","  27103502",7980,1,"WR 3",1,null,null,0,null,14,0,1,1000,null)
WRInfo[2][16]=1
WRInfo[2][17]=1
WRInfo[3]=new Array("PAC7","  27103508",7980,1,"WR 4",1,null,null,0,null,14,0,1,1000,null)
WRInfo[3][16]=1
WRInfo[3][17]=1
WRInfo[4]=new Array("PAC7","  40090558",7980,1,"WR 5",1,null,null,0,null,14,0,1,1000,null)
WRInfo[4][16]=1
WRInfo[4][17]=1
WRInfo[5]=new Array("PAC7","  49092007",7980,1,"WR 6",1,null,null,0,null,14,0,1,1000,null)
WRInfo[5][16]=1
WRInfo[5][17]=1
WRInfo[6]=new Array("PAC7","  27103506",7480,1,"WR 7",1,null,null,0,null,14,0,1,1000,null)
WRInfo[6][16]=1
WRInfo[6][17]=1
WRInfo[7]=new Array("6300 TL","1003.101006015",6300,1,"WR 1",1,null,null,0,null,19,0,0,1000,null)
WRInfo[7][16]=2
WRInfo[7][17]=1
WRInfo[8]=new Array("6300 TL","1003.101006014",6300,1,"WR 2",1,null,null,0,null,19,0,0,1000,null)
WRInfo[8][16]=2
WRInfo[8][17]=1
WRInfo[9]=new Array("6300 TL","1003.101013034",6300,1,"WR 3",1,null,null,0,null,19,0,0,1000,null)
WRInfo[9][16]=2
WRInfo[9][17]=1
WRInfo[10]=new Array("6300 TL","1003.101006019",6300,1,"WR 4",1,null,null,0,null,19,0,0,1000,null)
WRInfo[10][16]=2
WRInfo[10][17]=1
WRInfo[11]=new Array("6300 TL","1003.101013035",6300,1,"WR 5",1,null,null,0,null,19,0,0,1000,null)
WRInfo[11][16]=2
WRInfo[11][17]=1
WRInfo[12]=new Array("5300 TL","1001.100709093",5300,1,"WR 6",1,null,null,0,null,19,0,0,1000,null)
WRInfo[12][16]=2
WRInfo[12][17]=1
WRInfo[13]=new Array("5300 TL","1001.100709098",5300,1,"WR 7",1,null,null,0,null,19,0,0,1000,null)
WRInfo[13][16]=2
WRInfo[13][17]=1
WRInfo[14]=new Array("6300 TL","1003.101006020",6300,1,"WR 8",1,null,null,0,null,19,0,0,1000,null)
WRInfo[14][16]=2
WRInfo[14][17]=1
var HPTitel="PV Gbr Schuster"
var HPBetreiber="PV Gbr Schuster"
var HPEmail="b.herb@klima-schuster.de"
var HPStandort="86316 Friedberg"
var HPModul="Suisse Soleil OKTOLON 190M36V1"
var HPWR="15x Diel Ako 5300TLO / Oelmaier Pac7"
var HPLeistung="104,29 kWp"
var HPInbetrieb="26. 6. 2010"
var HPAusricht="20 Grad Süd - Südöstlich"
var BannerZeile1=""
var BannerZeile2=""
var BannerZeile3=""
var BannerLink=""
var StatusCodes = new Array(15)
var FehlerCodes = new Array(15)
StatusCodes[0] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[0] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[1] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[1] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[2] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[2] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[3] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[3] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[4] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[4] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[5] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[5] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[6] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[6] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[7] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[7] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[8] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[8] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[9] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[9] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[10] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[10] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[11] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[11] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[12] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[12] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[13] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[13] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[14] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[14] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
var Verguetung=3914
var Serialnr = 4433585
var Firmware = "3.6.0 Build 99"
var FirmwareDate = "15.10.2019"
var WRTyp = "MULTIPROTOCOL"
var OEMTyp = 0
var SLTyp = "1000"
var SLVer = 2
var SLHW = 8461821
var SLBV = 22
var Intervall = 300
var SLDatum = "22.07.23"
var SLUhrzeit = "04:03:27"
var isTemp=true
var isOnline=true
var eventsHP=1
var exportDir="/friedberg"
var Lang="DE"
var AnlagenGrp=new Array()
AnlagenGrp[0]=new Array("Süd",null,950,3800)
AnlagenGrp[0][1]=new Array()
AnlagenGrp[0][1][0]=1
AnlagenGrp[0][1][1]=2
AnlagenGrp[0][1][2]=3
AnlagenGrp[0][1][3]=4
AnlagenGrp[0][1][4]=5
AnlagenGrp[0][1][5]=6
AnlagenGrp[0][1][6]=7
AnlagenGrp[0][1][7]=13
AnlagenGrp[0][1][8]=14
AnlagenGrp[1]=new Array("Nord",null,850,2874)
AnlagenGrp[1][1]=new Array()
AnlagenGrp[1][1][0]=8
AnlagenGrp[1][1][1]=9
AnlagenGrp[1][1][2]=10
AnlagenGrp[1][1][3]=11
AnlagenGrp[1][1][4]=12
AnlagenGrp[1][1][5]=15
var AnzahlGrp=2
var CFDatum = "21.11.21"
var CFUhrzeit = "17:34:37"
var SCB = true
var SCBIF1 = 0
var webMenuFull = 0
var IPlatform = 3
var DateFormat ="dd.mm.yy"
var TimeFormat ="HH:MM:ss"
var TimeFormatNoSec ="HH:MM"
var Currency ="€"
var CurrencySub ="Cent"
var CurrencyFirst ="0"
var ISOCode ="DE"
var DSTMode ="1"
var Dezimalseparator =","
var WeightUnit ="KG"
var DirectMarketing = false
var AdamAvailable=0
var netProfile=0
var pmControlType=0
var pmReductionOnSerialType=0
var windinverters=0
var co2factor=700
