

      SUBROUTINE INITIAL

INCLUDE 'MPARMLIN'

C **********************************************************************
C  INITIALIZE SIZE OF MAIN BLANK COMMON BLOCK
C  IBLOCK APPEARS IN THE FOLLOWING SUBROUTINES : NWPOSA, INITIAL
C
C     PARAMETER (IBLOCK=80000)
C
C **********************************************************************
C  INITIALIZE MAXIMUM NUMBER OF INTERNAL VARIABLES (ITEMS)
C  INTMAX APPEARS IN THE FOLLOWING SUBROUTINES : INITIAL, INIT
C
C      PARAMETER (INTMAX=26)
C
C **********************************************************************
C  INITIALIZE MAXIMUM LENGTH OF INPUT FORMAT TO 100 CHARACTERS
C  LENIFOR APPEARS IN THE FOLLOWING SUBROUTINES :
C                          MAINSUB, INITIAL, ENTER, READAT, POSAC
C
      PARAMETER (LENIFOR=100)
C
C **********************************************************************
C  INITIALIZE LENGTH OF EXTERNAL TRAIT LABEL TO 10 WORDS OF 4 BYTES EACH
C  NWORDS APPEARS IN THE FOLLOWING SUBROUTINES : EXTMAP, PLOTS, VALMAP
C
      PARAMETER (NWORDS=10)
C
C **********************************************************************
C  INITIALIZE MAXIMUM NUMBER OF EXTERNAL MAPS TO 30
C  MAXEXMAP APPEARS IN THE FOLLOWING SUBROUTINES : EXTMAP, VALMAP
C
      PARAMETER (MAXEXMAP=30)
C
C **********************************************************************
C  INITIALIZE MAXIMUM NUMBER OF INTERVALS FOR DEFINING EXTERNAL VARIABLE
C  OR TRAIT TO 10 .  MAXINTRV APPEARS IN THE FOLLOWING SUBROUTINES :
C                            EXTVAR, EXTMAP, ORDEXT, READAT, VALMAP
C
C      PARAMETER (MAXINTRV=10)
C
C **********************************************************************
C  INITIALIZE MAXIMUM NUMBER OF CASE ID'S
C  IDMAX APPEARS IN THE FOLLOWING SUBROUTINES :
C               MAINSUB, INITIAL, ADDMNX, PERMUT, POFREQ, PRFOUT, PRNTID
C
C      PARAMETER (IDMAX=500)
C
C **********************************************************************
C  INITIALIZE MAXIMUM LENGTH INTERNAL VARIABLES LABELS
C  LABLEN APPEARS IN THE FOLLOWING SUBROUTINES :
C               MAINSUB, INITIAL
C
      PARAMETER (LABLEN=40)
C
C **********************************************************************
C  INITIALIZE MAXIMUM LENGTH OF CASE ID
C  IDLEN APPEARS IN THE FOLLOWING SUBROUTINES :
C        MAINSUB, INITIAL, ADDMNX, PERMUT, POFREQ, PRFOUT, PRNTID, READAT
C                              VALMAP
C
      PARAMETER (IDLEN=10)
C
C **********************************************************************
C  INITIALIZE MAXIMUM NUMBER OF EXTERNAL MAPS
C  MAXEXTMP APPEARS IN THE FOLLOWING SUBROUTINES :
C               MAINSUB, INITIAL
C
C      PARAMETER (MAXEXTMP=30)
C
C **********************************************************************
C  INITIALIZE MAXIMUM NUMBER OF ITERATIONS
C  MITR APPEARS IN THE FOLLOWING SUBROUTINES :
C               MAINSUB, INITIAL
C
      PARAMETER (MITR=15)
C
      COMMON/INITL/MINVAL,MAXVAL
      COMMON/ZEROES/ZERO,ZEROMU2
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/SHEMOR/INDIC, IFSHMR
C      COMMON/DIM/M,N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12
      COMMON/AA/NV,NCAS,NXT,MAP,M
      COMMON/SBPOSA/INITX,FND1,FND2
      COMMON/ABTOL/A0,B0,TOL,EXTRA
      COMMON/LAB/LABEL(MNV), PATH
      COMMON/KENID/YESID
      COMMON/FF/FORMFEED
      COMMON/BOXSTRNG/UP,BOTTM,LEFT,RIGHT,
     $                   UPLEFT,UPRIGHT,BOTTMLEFT,BOTTMRIGHT
C
C
      CHARACTER*1 UP,BOTTM,LEFT,RIGHT,
     $              UPLEFT,UPRIGHT,BOTTMLEFT,BOTTMRIGHT
      CHARACTER*1 FORMFEED
      CHARACTER*40 LABEL
      CHARACTER*80 PATH
C
      INTEGER*2 NV,NCAS,NXT,MAP,M
      LOGICAL YESID
C
C **********************************************************************
C  DEFINE A VERY SMALL VALUE AS ZERO FOR SUBROUTINE POSAC
C
      ZERO=1.E-38
C
C **********************************************************************
C  DEFINE A VERY SMALL VALUE AS ZERO FOR SUBROUTINE MU2 AND MUTRET
C
      ZEROMU2=1.E-20
C
C **********************************************************************
C  INITIALIZE YESID TO .FALSE. WHICH MEANS NO ID'S EXIST IN DATA
C
      YESID = .FALSE.
C
C **********************************************************************
C  TAPE ASSIGNEMENTS
C
      NREAD=1
      NTAPE=2
      NWRITE=7
      NSCR=9
C
C **********************************************************************
C  INDIC IS THE UNIT ON WHICH INFORMATION IS
C   WRITTEN FOR PROGRAM SHEMOR
C
      INDIC=10
C
C **********************************************************************
C
C       NOTE THAT UNIT 12 IS USED FOR THE AUXILIARY OUTPUT FILES,
C       SET AS THE VALUE OF IWRTFLS IN MAINSUB
C
C **********************************************************************
C
C       NOTE THAT UNIT 14 IS USED FOR INFOMATION WRITTEN ON THE
C       EXTERNAL VARIABLES IN POSAC -
C         variable IEXTOUT in subroutine PLOTS
C
C **********************************************************************
C
C       NOTE THAT UNIT 21 IS USED FOR THE TEMPORARY PARAMATER FILE
C       IN OPENFILE, AND AS THE SCREEN IMAGE FILE IN PLSCRN
C
C **********************************************************************
C  INITIALIZE PARAMETERS FOR SUB. MAINSUB
C
C  INITIALIZE NUMBER OF DIMENSIONS TO 2 .
C
      M=2
C
C **********************************************************************
C  INITIALIZE PARAMETERS FOR SUB. MISS
C
C  INITIALIZE MINIMUM AND MAXIMUM VALUES OF VARIABLES .
C
      MINVAL=1
      MAXVAL=99
C
C **********************************************************************
C  INITIALIZE PARAMETERS FOR SUB. ZXGSN
C
      A0=0.
      B0=2.
C      TOL=.00001
      TOL=.0001
      EXTRA=2.
C
C **********************************************************************
C  INITALIZE POWER OF THE BALANCING WEIGHT
      FND1=4.0
      FND2=4.0
C
C **********************************************************************
C  INITALIZE VARIABLE LABELS
C
      DO 10 I=1,MNV
            LABEL(I)=' '
 10   CONTINUE
C
C **********************************************************************
C  INITIALIZE GRAPHIC CHARACTERS FOR FRAME DRAWING
C
      UP='Í'
      BOTTM='Í'
      LEFT='º'
      RIGHT ='º'
      UPLEFT='É'
      UPRIGHT = '»'
      BOTTMLEFT = 'È'
      BOTTMRIGHT='¼'
C
C **********************************************************************
C  INITIALIZE FORM-FEED CHARACTER FOR PRINTER
C
      FORMFEED= CHAR (12)
C
      RETURN
      END

      SUBROUTINE OPENFIL
C
C         OPENFIL reads the parameter line, and opens the files required.
C         PARS in common block WCHAR is set to the name of the data file
C         PATH in common block LAB is set to the path for the output file
C
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/SHEMOR/INDIC, IFSHMR
      COMMON   /WCHAR/ PARS, DUMMY
C
      CHARACTER*128 PARS
      CHARACTER*152 DUMMY (2)
      INTEGER*2 I, STATUS
C
CY      I = NARGS () - 1
      I = IARGC()
      IF (I .LT. 3) GOTO 800
C
      I = 1
CY      CALL GETARG (I, PARS, STATUS)
CY      IF (STATUS .LE. 0)  GOTO 810
      CALL GETARG (I, PARS)
      IF (PARS(1:1).EQ.' ')  GOTO 810
C
      OPEN (NREAD,FILE=PARS,STATUS='OLD',ACCESS='SEQUENTIAL',
     $              FORM='FORMATTED',ERR=820 )
C
      I = 3
      CALL GETARG (I, PARS)
CY      IF (STATUS .LE. 0)  GOTO 810
      IF (PARS(1:1).EQ.' ')  GOTO 810
C
      OPEN (NWRITE,FILE=PARS,ACCESS='SEQUENTIAL',
     $              FORM='FORMATTED',ERR=820 )
C
      I = 1
      CALL GETPATH (PARS, I, STATUS)
C
      I = 2
      CALL GETARG (I, PARS)
CY      IF (STATUS .LE. 0)  GOTO 810
      IF (PARS(1:1).EQ.' ')  GOTO 810
C
      OPEN (NTAPE,FILE=PARS,STATUS='OLD',ACCESS='SEQUENTIAL',
     $              FORM='FORMATTED',ERR=820 )
C
      OPEN (NSCR,FILE='FORT9',ACCESS='SEQUENTIAL',
     $              FORM='UNFORMATTED' )
C
      OPEN (INDIC,FILE='FORT10',ACCESS='SEQUENTIAL',
     $              FORM='UNFORMATTED' )
C
      RETURN
C
 800  WRITE (*,900) I, CHAR(7)
      GOTO 850
C
 810  WRITE (*,920) CHAR(7)
      GOTO 850
C
CY 820  WRITE (*,910) PARS (1:STATUS), CHAR(7)
 820  WRITE (*,910) PARS, CHAR(7)
      GOTO 850
C
 850  STOP 2
C
 900  FORMAT (' *** ERROR ***  only ', I1,
     1        ' parameters supplied - 3 required.', A1)
 910  FORMAT (' *** ERROR *** opening file ', A, A1)
 920  FORMAT (' *** ERROR *** Parameter status error in  GETARG.', A1)
C
      END


      SUBROUTINE GETPATH (PARS, I, J)
C
      CHARACTER*(*) PARS
      INTEGER*2 I, J
C
C         Given PARS, I and J such that PARS (I:J) is a valid filename,
C         returns in common PATHLEN = 0 if the filename contains no drive
C         or path component, or PATH (1:PATHLEN) as a string containing the 
C         drive and path used to address the file.
C
INCLUDE 'MPARMLIN'
      COMMON/NPG/NEWPAGE, PATHLEN
      COMMON/LAB/LABEL (MNV),PATH
C
      INTEGER*2 NEWPAGE, PATHLEN
      CHARACTER*40 LABEL
      CHARACTER*80 PATH
      INTEGER*2 K
C
      PATHLEN = 0
      IF (J .LT. I) RETURN
      K = J
C
 10   IF (PARS (K:K) .EQ. '\' .OR. PARS (K:K) .EQ. ':') THEN
          PATHLEN = K - I + 1
          PATH = PARS (I:K)
      ELSE IF (K .GT. I) THEN
          K = K - 1
          GOTO 10
      END IF
C
      RETURN
C
      END

      SUBROUTINE WHATFR(IFOR,YESID)

C  THIS SUB. TESTS THE FORMAT IN ORDER TO DETECT THE REQUEST
C  OF AN USER ID , AND DETECTS ALSO SOME USER'S ERRORS.

      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/AA/NV,NCAS,NXT,MAP,MDUM
      COMMON/OPT/IDATA
      INTEGER*2 NV,NCAS,NXT,MAP,MDUM
C
      PARAMETER (MFRLIN = 10)
      INTEGER*2 NFRLIN, JSTRT, JEND, NUMRD, IDLIN
      COMMON /FORANL/ NFRLIN, JSTRT (MFRLIN), JEND (MFRLIN),
     $                NUMRD (MFRLIN), IDLIN
C
      CHARACTER IFOR*(*)
      CHARACTER DIGITS*15, CHAR
C
      LOGICAL YESID
      INTEGER*2 L, NERROR, I1, I, J, SUM, TOT
C
C      DATA DIGITS/' TAXI0123456789(,/)'/
      DATA DIGITS/' TAX0123456789,'/
C
C **********************************************************************
C
      YESID = .FALSE.
      IDLIN = 0
      L =LEN(IFOR)
      NERROR = 0
      NFRLIN = 0
      I1 = 1
C
 5    CONTINUE
C
C  SUPPRESS BLANKS BEFORE OPENING BRACKET
C
      DO 10 I = I1, L
         IF (IFOR (I:I) .EQ. ' ') GO TO 10
         GO TO 20
   10 CONTINUE
      GOTO 60
   20 CONTINUE
C
C  TEST IF THE FORMAT BEGINS WITH '('
      IF (IFOR (I:I) .NE. '(') THEN
          NERROR = NERROR + 1
          WRITE(NWRITE,200)
      ENDIF
      NFRLIN = NFRLIN + 1
      IF (NFRLIN .GT. MFRLIN) THEN
          WRITE (NWRITE, 820) MFRLIN
          GOTO 999
      END IF
      JSTRT (NFRLIN) = I
      I1 = I+1
C
C         GET CORRESPONDING ')'
C
      DO 30 I = I1, L
          IF (IFOR(I:I) .EQ. ')') GOTO 40
 30   CONTINUE
      NERROR = NERROR + 1
      WRITE (NWRITE, 300)
      JEND (NFRLIN) = L
      GOTO 60
 40   JEND (NFRLIN) = I
      I1 = I + 1
      GOTO 5
C
 60   CONTINUE
      IF (NFRLIN .EQ. 0) GOTO 100
C
C  TEST FOR ILLEGAL CHARACTERS IN POSAC FORMAT
C
      TOT = 0
      DO 80 J = 1, NFRLIN
          SUM = 0
          DO 70 I = JSTRT (J) +1, JEND (J) -1
               CHAR = IFOR (I:I)
               IF (CHAR .EQ. 'I') THEN
                    SUM = SUM + 1
               ELSE IF (INDEX (DIGITS, CHAR) .EQ. 0) THEN
                    NERROR = NERROR + 1
                    WRITE (NWRITE,400) CHAR
               ENDIF
 70       CONTINUE
          NUMRD (J) = SUM
          TOT = TOT + SUM
 80   CONTINUE
C
      IF (IDATA .NE. 0) TOT = TOT - 1
      IF (TOT .NE. NV) THEN
          NERROR = NERROR + 1
          WRITE (NWRITE, 650)
      END IF
C
C  TEST FOR AN A-SPECIFICATION AND IT'S POSITION
C  IT HAS TO BE THE FIRST SPECIFICATION
C
      I1 = INDEX (IFOR, 'A')
      IF (I1 .GT. JEND (NFRLIN)) THEN
          NERROR = NERROR + 1
          WRITE (NWRITE, 670)
      ELSE IF (I1.NE.0) THEN
          DO 90 J = 1, NFRLIN
               IF (I1 .LE. JEND (J)) GOTO 95
 90       CONTINUE
          J = NFRLIN
 95       YESID = .TRUE.
          IDLIN = J
          IF (I1 .GT. INDEX (IFOR, 'I') ) THEN
               NERROR = NERROR + 1
               WRITE (NWRITE,500)
          ENDIF
C
C         CHECK CONSISTENCY OF NUMRD ARRAY (NO I BEFORE A)
C
          IF (IDLIN .GT. 1) THEN
               DO 97 J = 1, IDLIN - 1
                    IF (NUMRD (J) .NE.0) THEN
                         NERROR = NERROR + 1
                         WRITE (NWRITE,500)
                    END IF
 97            CONTINUE
          END IF
C
C              TEST FOR ANOTHER A SPECIFICATION
C
          IF (INDEX (IFOR (I1+1:L), 'A') .NE. 0) THEN
               NERROR = NERROR + 1
               WRITE (NWRITE,600)
          ENDIF
      ENDIF
C
      IF (NERROR.EQ.0) THEN
          RETURN
      ELSE
          WRITE(NWRITE,700) NERROR
          GOTO 999
      ENDIF
 100  CONTINUE
      WRITE(NWRITE,800)
 999  WRITE (*, *) ' Fatal errors in data format supplied.'
      STOP 2
C
  200 FORMAT(' ** ERROR ** Missing separator : (')
  300 FORMAT(' ** ERROR ** Missing separator : )')
  400 FORMAT(' ** ERROR ** Illegal character : ',A)
  500 FORMAT(' ** ERROR ** A-specification has to be the first')
  600 FORMAT(' ** ERROR ** Only one A-specification for',
     $       ' case ID is permitted')
  650 FORMAT(' ** ERROR ** I-specifications must match number of',
     $       ' variables.')
  670 FORMAT (' ** ERROR ** A-specification found after last format.')
  700 FORMAT(1X,I3,' ERRORS EXECUTION ABORTED')
  800 FORMAT (' ** ERROR ** Empty format')
  820 FORMAT (' ** ERROR ** Too many lines in data format. Maximum',
     $        ' allowed is ', I3)
      END

      SUBROUTINE MISS(ICATMN,ICATMX,NV)
C
C  THIS SUB. READS MINIMAL AND MAXIMAL CATEGORY FOR
C  EACH VARIABLE WHEN MISSNG.NE.0
C  WHEN MISSNG=0 ,ICATMN=MINVAL  ICATMX=MAXVAL
C
      COMMON/OPMISS/MISSNG
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/INITL/MINVAL,MAXVAL
C
      INTEGER*2 NV,ICATMN(NV),ICATMX(NV)
C
      INTEGER*2 I
C
C **********************************************************************
C
      IF(MISSNG.EQ.0) GO TO 10
      READ(NREAD,100) (ICATMN(I),I=1,NV)
      READ(NREAD,100) (ICATMX(I),I=1,NV)
      WRITE(NWRITE,200)
      DO 20 I=1,NV
         WRITE(NWRITE,300) I,ICATMN(I),ICATMX(I)
   20 CONTINUE
      RETURN
   10 CONTINUE
      DO 30 I=1,NV
         ICATMN(I)=MINVAL
         ICATMX(I)=MAXVAL
   30 CONTINUE
      WRITE(NWRITE,400)
      RETURN
  100 FORMAT(26I4)
  200 FORMAT(16H MISSING VALUES ,14(1H.),16H  FOR VARIABLE  ,
     $17HOUTSIDE THE RANGE)
  300 FORMAT(39X,I3,14X,1H(,I2,1H,,I2,1H))
  400 FORMAT(15H MISSING VALUE ,15(1H.),4H   0)
      END

      SUBROUTINE EXTVAR(IVEXT,NBINT,IBORNE,JBORNE)
C
      PARAMETER (MAXINTRV=10)
C
C  READS INFORMATION ON EXTERNAL VARIABLES
C
      COMMON/AA/NV,NCAS,NXT,MAP,MDUM
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/SHEMOR/INDIC, IFSHMR
C
      INTEGER*2 NV,NCAS,NXT,MAP,MDUM
      INTEGER*2 IVEXT(NXT),NBINT(NXT),IBORNE(MAXINTRV,NXT),
     $                                 JBORNE(MAXINTRV,NXT)
C
      INTEGER*2 I,J,NB
C
C **********************************************************************
C
      DO 10 I=1,NXT
          READ(NREAD,200) IVEXT(I),NB,(IBORNE(J,I),JBORNE(J,I),J=1,NB)
          NBINT(I)=NB
          IF (NB .GT. MAXINTRV) THEN
               WRITE (*,*) '*** ERROR *** External variable with more',
     $             ' than', MAXINTRV, ' category intervals.', CHAR(7)
               WRITE (*,*) IVEXT(I),NB,(IBORNE(J,I),JBORNE(J,I),J=1,NB)
               STOP
          END IF
   10 CONTINUE
C  WRITE SERIAL NUMBER OF EXTERNAL VARIABLES FOR PRG. SHEMOR
      WRITE(INDIC) (IVEXT(I),I=1,NXT)
      RETURN
  200 FORMAT(20I4)
      END

      SUBROUTINE OUTVAR(IVEXT,NBINT,IBORNE,JBORNE, NLAB)
C
INCLUDE 'MPARMLIN'
      PARAMETER (MAXINTRV=10)
C
C  WRITES INFORMATION ON EXTERNAL AND INTERNAL VARIABLES
C
      COMMON/AA/NV,NCAS,NXT,MAP,MDUM
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/SHEMOR/INDIC, IFSHMR
      COMMON/LAB/LABEL (MNV),PATH
      CHARACTER*40 LABEL
      CHARACTER*80 PATH

C
      INTEGER*2 NV,NCAS,NXT,MAP,MDUM
      INTEGER*2 IVEXT(NXT),NBINT(NXT),IBORNE(MAXINTRV,NXT),
     $                                 JBORNE(MAXINTRV,NXT)

C
      INTEGER*2 I,J,NB
C
      IF (NLAB .NE. 0) THEN
          WRITE (NWRITE,1008)
          WRITE (NWRITE,1009)
          DO 20 J = 1, NV
               DO 10 I = 1, NXT
                    IF (IVEXT (I) .EQ. J) GOTO 20
  10           CONTINUE
               WRITE (NWRITE,1010) J, LABEL(J)
  20      CONTINUE
C
          IF (NXT .NE. 0) THEN
               WRITE (NWRITE,1011)
               WRITE (NWRITE,1009)
               DO 30 I = 1, NXT
                    J = IVEXT (I)
                    WRITE (NWRITE,1010) J, LABEL(J)
  30           CONTINUE
          END IF
      ENDIF
C
      WRITE(NWRITE,100)
C
      DO 50 I=1,NXT
          NB = NBINT(I)
          WRITE(NWRITE,300) IVEXT(I),(IBORNE(J,I),JBORNE(J,I),J=1,NB)
  50  CONTINUE
C
      RETURN
C
 100  FORMAT(/,18H EXTERNAL VARIABLE,6X,18HCATEGORY INTERVALS,
     $/,1X,17(1H-),6X,18(1H-))
 300  FORMAT(8X,I2,14X,10(1H(,I2,1H,,I2,2H) :2H, ))
 1008 FORMAT(//'INTERNAL POSAC')
 1009 FORMAT(3X,'VARIABLE',17X,'VARIABLE LABEL'/ 14('-'),7X,40('-'))
 1010 FORMAT(3X,'ITEM ',I3,1H:,9X,A40)
 1011 FORMAT(/'   EXTERNAL')
C
      END

