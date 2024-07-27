ECHO OFF
ECHO .   
ECHO                 *******************************************************
ECHO                 *                                                     *
ECHO                 *       P R O G R A M     P O S A C / L S A           *
ECHO                 *                                                     *
ECHO                 *******************************************************
REM
IF %3==PRN  GOTO SETPRN
IF %3==prn  GOTO SETPRN
IF %4==PRN  GOTO SETPRN
IF %4==prn  GOTO SETPRN
IF %5==PRN  GOTO SETPRN
IF %5==prn  GOTO SETPRN
GOTO DOPROG
:SETPRN
REM ********** BEGIN PRINTER SETTING **************
ECHO PLEASE SCROLL PAPER IN PRINTER TO TOP OF PAGE
PAUSE
TYPE \SETPRNTR.COD>PRN
TIMEMARK>PRN
:DOPROG
REM ********** BEGIN PROGRAM POSAC ****************
TNWPOSAC_32  %1  %2  %3
IF %3==PRN  GOTO PAGEPRN
IF %3==prn  GOTO PAGEPRN
GOTO DOPR2
:PAGEPRN
TYPE \FORMFEED.COD>PRN
:DOPR2
IF ERRORLEVEL 2 GOTO fail
REM *********** BEGIN PROGRAM LSA1 ****************
SLSA1_32  %4
REM *********** BEGIN PROGRAM LSA2 ****************
SLSA2_32  %5
REM *********** BEGIN PROGRAM SHEMOR **************
IF X%6==X  GOTO end
SSHEMOR_32  %1  %2  CON  %6
:end
REM *********** BEGIN PROGRAM POSACSEP ************
REM   **** temporary shell with fixed names and input direct to prog ****
POSACSEP_32  POSACSEP.OUT  POSACSEP.TAB
REM   ******* END POSACSEP ***********************
ECHO     Enter PL to view POSAC, LSA1, or LSA2 screen diagrams.
:fail
