
CY$STORAGE:2
      PROGRAM POSXTSEP
C***************************************************************
C
C
C***************************************************************
C
C  THIS PROGRAM IS RUN AFTER PROGRAM 'POSAC' WITHOUT ANY
C  ADDITIONAL DIRECTIVES . IT WORKS ON RESULTS WRITTEN
C  BY 'POSAC' ON UNIT 'IEXTOUT' - FILE FORT14
C
C  The supplied parameters are
C
CXXXXX     1.  The item number to be analysed
C     1.  The item threshold:-  the two groups are defined as
C                item < theshold   (lower left)
C                item >= threshold (upper right)
C     2.  The name of the file for the output summary
C     3.  The name of the file for the results table.
C
C    In case only 2 parameters are given, the thresholds
C        are taken from interactive input
C
C*******************************************************************************
C
C     This version is designed to work on a case basis - that is, each point
C     is treated as a set of cases, and is given weighting in the loss
C     function according to those cases which are the wrong side of the line
C
C     The line is designed to separate those cases which have the property,
C     (above the line) from those that do not (below the line).  Each point
C     is labelled by its number of cases which have the property (in YES(I))
C     and its number of cases which do not have the property (in NO(I)).
C
C*******************************************************************************
C
C     This is a version designed to be mathematically the same as POSXTSP2
C     but is designed to work faster by combining the analysis
C     in the loss function into a single pass in one loop.
C
C*******************************************************************************
C
      IMPLICIT NONE
      INTEGER*2 MAXCOR
      PARAMETER (MAXCOR = 5)
      REAL FIRST (MAXCOR+1)
INCLUDE 'MPARMLIN'
      REAL XX (MIEND), YY (MIEND), VALUE (MIEND),
     &     YES (MIEND), NO (MIEND)
      COMMON XX, YY, VALUE, YES, NO
      INTEGER*2 NWRITE,NTABLE,IEXT
      COMMON/IO/NWRITE,NTABLE,IEXT
      CHARACTER*1 UP,BOTTM,LEFT,RIGHT,
     $             UPLEFT,UPRIGHT,BOTTMLEFT,BOTTMRIGHT,FORMFEED
      COMMON/SCHARS/UP,BOTTM,LEFT,RIGHT,
     $               UPLEFT,UPRIGHT,BOTTMLEFT,BOTTMRIGHT,FORMFEED
      INTEGER*2 NP, NX, NY, TYPE, I, NCORN
      INTEGER*2 DEVFRQ
      REAL TOTFRQ
      LOGICAL*2 STARTED
      REAL LOSS, SOLVE_MIN, COEF (MAXCOR+1)
      CHARACTER*1  CH, TYPCH (MAXCOR+1)
      INTEGER*2 MAP, IEND, M
      REAL  THR1, THR2

      WRITE(*,1001)
      CALL GETPARS
      READ (IEXT) MAP, IEND
      WRITE(NWRITE,1000) FORMFEED
      WRITE (NTABLE, 1008)
      WRITE (NTABLE, 1004)
      DO 200 M = 1, MAP
          WRITE (NWRITE, 1011) M
          CALL FREAD (XX, YY, VALUE, THR1, THR2, YES, NO, IEND)
          NP = IEND
          TOTFRQ = 0
          DO 20 I = 1, NP
               TOTFRQ = TOTFRQ + YES (I) + NO (I)
 20       CONTINUE
          STARTED = .FALSE.
          CALL SETUP_POINTS (XX, YY, YES, NO, NP)
          DO 50 NCORN = 0, 3
               LOSS = SOLVE_MIN (NCORN, FIRST, NX, NY, TYPE, DEVFRQ)
CCC               IF (NCORN .NE. 0)  READ (*,'(A1)') CH
               WRITE (NWRITE, 1002) NCORN, LOSS, LOSS / TOTFRQ,
     1                          DEVFRQ, (100.0 * DEVFRQ) / TOTFRQ
               COEF (NCORN+1) = LOSS
               IF (IAND (NCORN, INT2(1)) .EQ. 0) THEN
                    IF (TYPE .EQ. 1) THEN
                         TYPCH (NCORN+1) = 'X'
                    ELSE
                         TYPCH (NCORN+1) = 'Y'
                    ENDIF
               ELSE
                    IF (TYPE .EQ. 1) THEN
                         TYPCH (NCORN+1) = 'T'
                    ELSE
                         TYPCH (NCORN+1) = 'C'
                    ENDIF
               ENDIF
               IF (STARTED) THEN
                    READ (*,'(A1)') CH
               ELSE
                    STARTED = .TRUE.
               END IF
               CALL PLOT (XX, YY, VALUE, THR1, THR2, NP, M, FIRST,
     1                    NX, NY, TYPE, NCORN)
               WRITE (NWRITE,1010)
 50       CONTINUE
          IF (M .EQ. 1) THEN
               WRITE (NTABLE, 1005)
          ELSE
               WRITE (NTABLE, 1009)
          END IF
          WRITE (NTABLE, 1006)  M, (COEF (I), TYPCH (I), I=1,4)
 200  CONTINUE
      WRITE (NTABLE, 1007)
      CLOSE (NTABLE)
      READ (*,'(A1)') CH
      CALL textmode
      STOP ' '
 1000 FORMAT(A1,/,40X,55(1H*),/,40X,1H*,22X,
     $8HPOSXTSEP,23X,1H*,/,40X,1H*,
     $39H   A PROGRAM FOR OPTIMALLY PARTITIONING,
     $14H POSAC SPACE  ,1H*/40X,1H*,
     $15X,23HBY AN EXTERNAL VARIABLE,15X,1H*/40X,55(1H*),///)
 1001 FORMAT(7X,55(1H*)/7X,1H*,22X,
     $8HPOSACSEP,23X,1H*/7X,1H*,
     $39H   A PROGRAM FOR OPTIMALLY PARTITIONING,
     $14H POSAC SPACE  ,1H*/7X,1H*,
     $15X,23HBY EACH ITEM (VARIABLE),15X,1H*/7X,55(1H*)/)
 1002 FORMAT (' For', I2, ' corners: minimum deviation is', F9.2,
     1        ' or', F7.3, ' per profile'/
C     2        ' Number of different deviant profiles is ', I3/
     3        ' Frequency of deviant profiles is', I5, ' or ', F6.2,
     4        '% of the total'/)
CY 1003 FORMAT (' FATAL ERROR: Incorrect item number', I3, '. Only', I3,
CY     1        ' items available.')
 1004 FORMAT(' � ITEM �   POLAR   �  ACC/ATT  �   PROMO   �   MODIF   �'
     1       )
 1005 FORMAT(' 쳐컴컴컵컴컴컴컴컫컵컴컴컴컴컫컵컴컴컴컴컫컵컴컴컴컴컫캑'
     1       )
 1006 FORMAT (' �', I4, 2X, '�', 4(F8.2, ' �', A1, '�'))
 1007 FORMAT(' 읕컴컴컨컴컴컴컴컨컨컴컴컴컴컨컨컴컴컴컴컨컨컴컴컴컴컨켸'
     1       )
 1008 FORMAT(' 旼컴컴컫컴컴컴컴컴컫컴컴컴컴컴컫컴컴컴컴컴컫컴컴컴컴컴커'
     1       )
 1009 FORMAT(' 쳐컴컴컵컴컴컴컴컵컵컴컴컴컴컵컵컴컴컴컴컵컵컴컴컴컴컵캑'
     1       )
 1010 FORMAT (/)
 1011 FORMAT (' ITEM NO.', I3/ ' -----------'/)
      END
C
      SUBROUTINE GETPARS
      IMPLICIT NONE
C
      INTEGER*2 NWRITE,NTABLE,IEXT
      COMMON/IO/NWRITE,NTABLE,IEXT
      CHARACTER*128 PARS
CY      INTEGER*2 I, STATUS, J
CY      INTEGER*4 NARGS
      INTEGER*2 I, J
      INTEGER*4 IARGC
C
      NWRITE=3
      NTABLE=20
      I = IARGC()
C
      IF (I .NE. 2) GOTO 800
      J = 1
C      IF (I .EQ. 2)  J = 1
C
C      I = 1
C      CALL GETARG (I, PARS, STATUS)
C      IF (STATUS .LE. 0)  GOTO 810
C      READ (PARS (1:STATUS), 930, ERR=810) ITEM
C
C      IF (J .EQ. 0) THEN
C          I = 1
C          CALL GETARG (I, PARS, STATUS)
C          IF (STATUS .LE. 0)  GOTO 810
C          READ (PARS (1:STATUS), 930, ERR=810) THRESH
C      ELSE
C          THRESH = -1
C      END IF
C
      I = 2 - J
CY      CALL GETARG (I, PARS, STATUS)
CY      IF (STATUS .LE. 0)  GOTO 810
      CALL GETARG (I, PARS)
      IF (PARS(1:1).EQ.' ')  GOTO 810
C
      OPEN (NWRITE,FILE=PARS,ACCESS='SEQUENTIAL',
     $              FORM='FORMATTED',ERR=820 )
C
      I = 3 - J
CY      CALL GETARG (I, PARS, STATUS)
CY      IF (STATUS .LE. 0)  GOTO 810
      CALL GETARG (I, PARS)
      IF (PARS(1:1).EQ.' ')  GOTO 810
C
      OPEN (NTABLE,FILE=PARS,ACCESS='SEQUENTIAL',
     $              FORM='FORMATTED',ERR=820 )
C
C      OPEN (NSCR,FILE='FORT9',STATUS='OLD',ACCESS='SEQUENTIAL',
C     $              FORM='UNFORMATTED',ERR=830 )
C      REWIND NSCR
C
      IEXT = 14
      OPEN (IEXT,FILE='FORT14',ACCESS='SEQUENTIAL',
     $              FORM='UNFORMATTED' )
C
      RETURN
C
 800  WRITE (*,900) CHAR(7)
C      WRITE (*,905)
      GOTO 850
C
 810  WRITE (*,920) I, CHAR(7)
      GOTO 850
C
CY 820  WRITE (*,910) PARS (1:STATUS), CHAR(7)
 820  WRITE (*,910) PARS, CHAR(7)
      GOTO 850
C
CY 830  WRITE (*,910) 'FORT9', CHAR(7)
CY      GOTO 850
C
 850  STOP 2
C
C 900  FORMAT (' *** ERROR ***  Insufficient parameters supplied.'/
C     1   '  USAGE is POSACSEP <ITEM-NUMBER> <ITEM-THRESHOLD> <OUTFILE>',
C     2       A1)
 900  FORMAT (' *** ERROR ***  Insufficient parameters supplied.'/
C     1 '  USAGE is POSACSEP [<ITEM-THRESHOLD>] <OUTFILE> <TABLE-FILE>',
     1 '  USAGE is POSACSEP <OUTFILE> <TABLE-FILE>',
     2       A1)
C 905  FORMAT (' Here "ITEM-THRESHOLD" is the lowest category in the',
C     1        ' higher group.')
 910  FORMAT (' *** ERROR *** opening file ', A, A1)
 920  FORMAT (' *** ERROR *** Parameter error in  GETARG.',
     1        ' - parameter #', I1, A1)
CY 930  FORMAT (BN,I30)
C
      END
C
C      SUBROUTINE GETTHR (THRESH, NV)
C      IMPLICIT NONE
C      INTEGER*2 NV, THRESH (*)
C      INTEGER*2 I
C
C      IF (THRESH (1) .EQ. -1) THEN
C          WRITE (*, 930)
C          DO 100 I = 1, NV
C 30            WRITE (*, 900) I
C               READ (*, *, ERR=50) THRESH (I)
C               GOTO 100
C 50            WRITE (*, 920)
C               GOTO 30
C 100      CONTINUE
C      ELSE
C          DO 200 I = 1, NV
C               THRESH (I) = THRESH (1)
C 200      CONTINUE
C      END IF
C
C      RETURN
C
C 900  FORMAT (' ENTER THE THRESHOLD FOR ITEM NUMBER', I3, ':  '\)
C 920  FORMAT (' ERROR IN INPUT')
C 930  FORMAT (' Now input the THRESHOLD for each ITEM,'
C     1        ' or CTRL-C to abort POSACSEP'/
C     2        ' Here "THRESHOLD" is the lowest category in the',
C     3        ' higher group.')
C      END
C
      SUBROUTINE FREAD (XX, YY, VALUE, V1, V2, YES, NO, IEND)
      IMPLICIT NONE
      INTEGER*2 IEND
      REAL XX(*), YY(*), VALUE (*), YES(*), NO(*)
      REAL V1,V2
      INTEGER*2 NWRITE,NTABLE,IEXT
      COMMON/IO/NWRITE,NTABLE,IEXT
      INTEGER*2 I, K
      REAL VMEAN
      INTEGER*2 IFREQ
C
      READ (IEXT) V1, V2, VMEAN, K
      IF (K .NE. IEND) STOP 'ERROR READING INPUT FILE' 
      DO 10 I=1, IEND
         READ (IEXT) XX(I),YY(I),VALUE(I),IFREQ
         YES (I) = IFREQ * VALUE (I)
         NO (I) = IFREQ * (1 - VALUE(I))
   10 CONTINUE
      RETURN
      END
C
C
      LOGICAL*2 FUNCTION FINPOS (X, NPTS, PTS, POS)
      
      IMPLICIT NONE

      INTEGER*2 NPTS, POS
      REAL X, PTS (*)


C     INPUT: X    -  the argument (REAL)
C            XARR -  a REAL array of values stored in ascending order,
C                     from index 1 to index NPTS.
C
C                    i.e.  X [I] <= X [I+1] for all I with
C                            0 < I < NPTS
C
C            NPTS - Number of values in array XARR

C     OUTPUT:  IF FINPOS IS .FALSE.
C            POS   - the index such that   0 < POS < NPTS
C                    and                   XARR (POS) < X < XARR (POS+1)
C
C                    OR POS = 0 IF   X < XARR (1)
C                    OR POS = NPTS IF X > XARR (NPTS)

C              IF FINPOS IS .TRUE.
C            POS   - the index such that   0 < POS <= NPTS
C                    and                   XARR (POS) = X

      INTEGER*2 INDEX, START, FIN

      START = 0
      FIN = NPTS + 1

 50   CONTINUE
      IF (FIN - START .LE. 1)  GOTO 100
          INDEX = (START + FIN) / 2
          IF (X .LT. PTS (INDEX)) THEN
               FIN = INDEX
          ELSE IF (X .GT. PTS (INDEX)) THEN
               START = INDEX
          ELSE
               POS = INDEX
               FINPOS = .TRUE.
               RETURN
          END IF
      GOTO 50
 100  CONTINUE

      POS = START
      FINPOS = .FALSE.
      RETURN
      END


      SUBROUTINE SORT_PTS (N, AX, AY, YY, NN)

      IMPLICIT NONE

      INTEGER*2 N
      REAL AX (N), AY (N), YY (N), NN (N)      

      INTEGER*2 I, J, K
      LOGICAL*2 DUM, FINPOS
      REAL X, Y, YYT, NNT

      DO 50 I = 2, N
          X = AX (I)
          Y = AY (I)
          YYT = YY (I)
          NNT = NN (I)
          K = I-1
          DUM = FINPOS (X, K, AX, J)
          J = J + 1
          IF (J .LT. I) THEN
               DO 40 K = I-1, J, -1
                    AX (K+1) = AX (K)
                    AY (K+1) = AY (K)
                    YY (K+1) = YY (K)
                    NN (K+1) = NN (K)
 40            CONTINUE
               AX (J) = X
               AY (J) = Y
               YY (J) = YYT
               NN (J) = NNT
          END IF
 50   CONTINUE
      RETURN
      END

C      SUBROUTINE SORT_PTS (N, PTS)
C
C      IMPLICIT NONE
C
C      INTEGER*2 N
C      REAL PTS (2, N)
C
C      INTEGER*2 I, J, K
C      LOGICAL*2 DUM, FINPOS
C      REAL X, Y
C
C      DO 50 I = 2, N
C          X = PTS (1,I)
C          Y = PTS (2,I)
C          K = I-1
C          DUM = FINPOS (X, K, PTS, J)
C          J = J + 1
C          IF (J .LT. I) THEN
C               DO 40 K = I-1, J, -1
C                    PTS (1,K+1) = PTS (1,K)
C                    PTS (2,K+1) = PTS (2,K)
C 40            CONTINUE
C               PTS (1,J) = X
C               PTS (2,J) = Y
C          END IF
C 50   CONTINUE
C      RETURN
C      END


      REAL FUNCTION LOSS1 (ZARR)

      IMPLICIT NONE

      REAL ZARR (*)

      INTEGER*2       NCOR, NXV, NYV, NTOT, N1, SUMFRQ
      COMMON /CORLOS/ NCOR, NXV, NYV, NTOT, N1, SUMFRQ
INCLUDE 'MPARMLIN'
      REAL  XARR (MIEND), YARR (MIEND), YES (MIEND), NO (MIEND)
      COMMON /POINTS/ XARR, YARR, YES, NO
C      INTEGER*2 MAXPTS
C      PARAMETER (MAXPTS = 200)
C      REAL XARR1 (MAXPTS), YARR1 (MAXPTS), XARR2 (MAXPTS), YARR2(MAXPTS)
C      COMMON /CORPTS/ XARR1, YARR1, XARR2, YARR2

      REAL*8  SUM
      INTEGER*2  I, J, K
      REAL    X, Y, DIST, DIST1, MAX
      PARAMETER (MAX = 1.0E30)
      REAL TOP, BOTTOM
      PARAMETER (BOTTOM  = 0.0)
      PARAMETER (TOP  = 100.0)

      IF ((ZARR (1) .LT. BOTTOM) .OR. (ZARR (NXV) .GT. TOP) .OR.
     1    (ZARR (NXV+1) .GT. TOP) .OR. (ZARR (NTOT) .LT. BOTTOM) )
     2            GOTO 100
      DO 20 J = 2, NXV
          IF (ZARR (J) .LT. ZARR (J-1))  GOTO 100
 20   CONTINUE
      DO 40 J = NXV+2, NTOT
          IF (ZARR (J) .GT. ZARR (J-1))  GOTO 100
 40   CONTINUE
      GOTO 200
 100  LOSS1 = MAX
      RETURN
 200  CONTINUE
      SUM = 0
      SUMFRQ = 0
      J = 1
      DO 300 I = 1, N1
          X = XARR (I)
          Y = YARR (I)
 220      CONTINUE
               IF (J .GT. NXV)  GOTO 240
               IF (X .LE. ZARR (J))  GOTO 240
               J = J + 1
          GOTO 220
 240      CONTINUE
C
C        for this version, DIST is positive for points above the line
C
          IF (J .EQ. 1) THEN
               DIST = - MAX
          ELSE IF ((J .GT. NXV) .AND. (NYV .LT. NXV))  THEN
               DIST = MAX
          ELSE
               DIST = Y - ZARR (NXV + J - 1)
          END IF
          IF (DIST .GT. 0) THEN
               K = J - 2
 260           CONTINUE
                    IF (K .LE. 0)  GOTO 280
                    IF (ZARR (NXV + K) .GE. Y)  GOTO 280
                    DIST1 = (Y - ZARR (NXV + K)) + (X - ZARR (K+1))
                    IF (DIST .GT. DIST1)  DIST = DIST1
                    K = K - 1
               GOTO 260
 280           CONTINUE
               DIST1 = X - ZARR (K+1)
               IF (DIST .GT. DIST1)  DIST = DIST1
               IF (DIST .GT. 0) THEN
                    SUM = SUM + DIST * NO (I)
                    SUMFRQ = SUMFRQ + NO (I)
               ENDIF
          ELSE IF (DIST .LT. 0) THEN
               K = J
 360           CONTINUE
                    IF (K .GT. NYV)  GOTO 380
                    IF (ZARR (NXV + K) .LE. Y)  GOTO 380
                    DIST1 = (Y - ZARR (NXV + K)) + (X - ZARR (K))
                    IF (DIST .LT. DIST1)  DIST = DIST1
                    K = K + 1
               GOTO 360
 380           CONTINUE
               IF (K .LE. NXV) THEN
                    DIST1 = X - ZARR (K)
                    IF (DIST .LT. DIST1)  DIST = DIST1
               END IF
               IF (DIST .LT. 0) THEN
                    SUM = SUM - DIST * YES (I)
                    SUMFRQ = SUMFRQ + YES (I)
               ENDIF
          END IF
 300  CONTINUE

      LOSS1 = SUM
      RETURN
      END


      REAL FUNCTION LOSS2 (ZARR)

      IMPLICIT NONE

      REAL ZARR (*)

      INTEGER*2       NCOR, NXV, NYV, NTOT, N1, SUMFRQ
      COMMON /CORLOS/ NCOR, NXV, NYV, NTOT, N1, SUMFRQ
INCLUDE 'MPARMLIN'
      REAL  XARR (MIEND), YARR (MIEND), YES (MIEND), NO (MIEND)
      COMMON /POINTS/ XARR, YARR, YES, NO
C      INTEGER*2 MAXPTS
C      PARAMETER (MAXPTS = 200)
C      REAL XARR1 (MAXPTS), YARR1 (MAXPTS), XARR2 (MAXPTS), YARR2(MAXPTS)
C      COMMON /CORPTS/ XARR1, YARR1, XARR2, YARR2

      REAL*8  SUM
      INTEGER*2  I, J, K
      REAL    X, Y, DIST, DIST1, MAX
      PARAMETER (MAX = 1.0E30)
      REAL TOP, BOTTOM
      PARAMETER (BOTTOM  = 0.0)
      PARAMETER (TOP  = 100.0)

      IF ((ZARR (1) .LT. BOTTOM) .OR. (ZARR (NXV) .GT. TOP) .OR.
     1    (ZARR (NXV+1) .GT. TOP) .OR. (ZARR (NTOT) .LT. BOTTOM) )
     2            GOTO 100
      DO 20 J = 2, NXV
          IF (ZARR (J) .LT. ZARR (J-1))  GOTO 100
 20   CONTINUE
      DO 40 J = NXV+2, NTOT
          IF (ZARR (J) .GT. ZARR (J-1))  GOTO 100
 40   CONTINUE
      GOTO 200
 100  LOSS2 = MAX
      RETURN
 200  CONTINUE
      SUM = 0
      SUMFRQ = 0
      J = 1
      DO 300 I = 1, N1
          X = XARR (I)
          Y = YARR (I)
 220      CONTINUE
               IF (J .GT. NXV)  GOTO 240
               IF (X .LE. ZARR (J))  GOTO 240
               J = J + 1
          GOTO 220
 240      CONTINUE
          IF ((J .GT. NXV) .AND. (NYV .EQ. NXV))  THEN
               DIST = MAX
          ELSE
               DIST = Y - ZARR (NXV + J)
          END IF
          IF (DIST .GT. 0) THEN
               K = J - 1
 260           CONTINUE
                    IF (K .LE. 0)  GOTO 280
                    IF (ZARR (NXV + K) .GE. Y)  GOTO 280
                    DIST1 = (Y - ZARR (NXV + K)) + (X - ZARR (K))
                    IF (DIST .GT. DIST1)  DIST = DIST1
                    K = K - 1
               GOTO 260
 280           CONTINUE
               IF (K .GT. 0) THEN
                    DIST1 = X - ZARR (K)
                    IF (DIST .GT. DIST1)  DIST = DIST1
               END IF
               IF (DIST .GT. 0) THEN
                    SUM = SUM + DIST * NO (I)
                    SUMFRQ = SUMFRQ + NO (I)
               ENDIF
          ELSE IF (DIST .LT. 0) THEN
               K = J + 1
 360           CONTINUE
                    IF (K .GT. NYV)  GOTO 380
                    IF (ZARR (NXV + K) .LE. Y)  GOTO 380
                    DIST1 = (Y - ZARR (NXV + K)) + (X - ZARR (K-1))
                    IF (DIST .LT. DIST1)  DIST = DIST1
                    K = K + 1
               GOTO 360
 380           CONTINUE
               IF (K .LE. NXV+1) THEN
                    DIST1 = X - ZARR (K-1)
                    IF (DIST .LT. DIST1)  DIST = DIST1
               END IF
               IF (DIST .LT. 0) THEN
                    SUM = SUM - DIST * YES (I)
                    SUMFRQ = SUMFRQ + YES (I)
               ENDIF
          END IF
 300  CONTINUE

      LOSS2 = SUM
      RETURN
      END


      SUBROUTINE AMOEBA (FUNCT, NDIM, XI, XIVAL,
     1                   VAL_ABS_TOL, VAL_REL_TOL, ITER)

      IMPLICIT NONE

      REAL FUNCT, XI (*), XIVAL (*), VAL_ABS_TOL, VAL_REL_TOL
      INTEGER*2  NDIM, ITER

      INTEGER*2 NWRITE,NTABLE,IEXT
      COMMON/IO/NWRITE,NTABLE,IEXT
C        Function to find a minimum value of a n-dim function 
C
C         Using Nelder and Mead's downhill simplex method
C         Press et al p. 289
C
C           FUNCT is the function to be integrated;
C           NDIM is the number of dimensions in the argument of FUNCT;
C           XI is a pointer to the (N+1)*N matrix of corner points
C                     of the simplex
C           XIVAL is a pointer to the (N+1) values of fn at the points of xi
C           VAL_ABS_TOL is the absolute precision acceptable in the minimum
C                   function value.
C           VAL_REL_TOL is the fractional precision acceptable in the minimum
C                   function value.
C           XI returns the simplex points contracted around the minimum
C           XIVAL returns the (N+1) values of fn at the points of xi
C           ITER returns the number of iterations used.
C                                   
C           FUNCT is defined as REAL FUNCTION FUNCT (X)
C                               REAL X (NDIM)

      INTEGER*2 ITMAX, MAX_DIM
      PARAMETER (ITMAX = 16000)
      PARAMETER (MAX_DIM = 4)
      INTEGER*2 MPTS,  LOW,  HIGH,  I,  J,  INDEX,  INDEX2
      REAL LOVAL,  HIVAL,  NXTHIVAL,  RTOL,   YPR,  YPRR,  REL_TOL
      REAL PBAR (MAX_DIM),  PR (MAX_DIM),  PRR (MAX_DIM)

      REAL  ALPHA,  BETA,  GAMMA
      PARAMETER (ALPHA = 1.0,  BETA  = 0.5,  GAMMA = 2.0)

      IF (NDIM .GT. MAX_DIM) THEN
          WRITE (*,*)  ' FATAL ERROR: DIMENSION TOO LARGE IN AMOEBA.'
          STOP
      END IF
      REL_TOL = VAL_REL_TOL * 0.5
      MPTS = NDIM + 1
      ITER = 0
 20   CONTINUE
          NXTHIVAL = XIVAL (1)
          HIVAL = XIVAL (2) 
          IF (NXTHIVAL .GT. HIVAL) THEN
               HIGH = 1
               LOW = 2
               LOVAL = HIVAL
               HIVAL = NXTHIVAL
               NXTHIVAL = LOVAL
          ELSE
               LOW = 1
               HIGH = 2
               LOVAL = NXTHIVAL
          END IF
          DO 50 I = 3, MPTS
               YPR = XIVAL (I)
               IF (YPR .LT. LOVAL) THEN
                    LOW = I
                    LOVAL = YPR 
               ELSE IF (YPR .GT. HIVAL) THEN
                    HIGH = I
                    NXTHIVAL = HIVAL
                    HIVAL = YPR 
               ELSE IF (YPR .GT. NXTHIVAL) THEN
                    NXTHIVAL = YPR
               END IF
 50       CONTINUE
          RTOL = HIVAL - LOVAL
          IF ((RTOL .LT. REL_TOL * (ABS (HIVAL) + ABS (LOVAL)))
     1         .OR. (RTOL .LT. VAL_ABS_TOL))      RETURN
          IF (ITER .GE. ITMAX) THEN
              WRITE (NWRITE, *)
     1             ' WARNING: TOO MANY ITERATIONS IN AMOEBA.'
              WRITE (*,*) ' WARNING: TOO MANY ITERATIONS IN AMOEBA.'
              RETURN
          END IF
          ITER = ITER + 1
          INDEX2 = (HIGH - 1) * NDIM + 1
          DO 60 J = 1, NDIM
               PBAR (J) = 0
 60       CONTINUE
          DO 100 I = 1, MPTS
               IF (I .NE. HIGH) THEN
                    INDEX = (I - 1) * NDIM
                    DO 80 J = 1, NDIM
                         INDEX = INDEX + 1
                         PBAR (J) = PBAR (J) + XI (INDEX)
 80                 CONTINUE
               END IF
 100      CONTINUE
          INDEX = INDEX2
          DO 120 J = 1, NDIM
               PBAR (J) = PBAR (J) / NDIM
               PR (J) = (1 + ALPHA) * PBAR (J) - ALPHA * XI (INDEX)
               INDEX = INDEX + 1
 120      CONTINUE
          YPR = FUNCT (PR)
          IF (YPR .LE. LOVAL) THEN
               DO 140 J = 1, NDIM
                    PRR (J) = GAMMA * PR (J) + (1 - GAMMA) * PBAR (J)
 140           CONTINUE
               YPRR = FUNCT (PRR)
               INDEX = INDEX2
               IF (YPRR .LT. YPR) THEN
                    DO 160 J = 1, NDIM
                         XI (INDEX) = PRR (J)
                         INDEX = INDEX + 1
 160                CONTINUE
                    XIVAL (HIGH) = YPRR
               ELSE
                    DO 180 J = 1, NDIM
                         XI (INDEX) = PR (J)
                         INDEX = INDEX + 1
 180                CONTINUE
                    XIVAL (HIGH) = YPR
               END IF
          ELSE IF (YPR .GE. NXTHIVAL) THEN
               IF (YPR .LT. HIVAL) THEN
                    INDEX = INDEX2
                    DO 190 J = 1, NDIM
                         XI (INDEX) = PR (J)
                         INDEX = INDEX + 1
 190                CONTINUE
                    XIVAL (HIGH) = YPR
                    HIVAL = YPR
               END IF
               INDEX = INDEX2
               DO 200 J = 1, NDIM
                    PRR (J) = BETA * XI (INDEX) + (1 - BETA) * PBAR (J)
                    INDEX = INDEX + 1
 200           CONTINUE
               YPRR = FUNCT (PRR)
               IF (YPRR .LT. HIVAL) THEN
                    INDEX = INDEX2
                    DO 220 J = 1, NDIM
                         XI (INDEX) = PRR (J)
                         INDEX = INDEX + 1
 220                CONTINUE
                    XIVAL (HIGH) = YPRR
               ELSE
                    DO 260 I = 1, MPTS
                         INDEX2 = LOW * NDIM
                         IF (I .NE. LOW) THEN
                              INDEX = (I - 1) * NDIM + 1
                              INDEX2 = INDEX2 - NDIM
                              DO 240 J = 1, NDIM
                                   INDEX2 = INDEX2 + 1
                                   XI (INDEX) =
     1                                0.5 * (XI (INDEX) + XI (INDEX2))
                                   INDEX = INDEX + 1
 240                          CONTINUE
                              XIVAL (I) = FUNCT (XI (INDEX - NDIM))
                         END IF
 260                CONTINUE
               END IF
          ELSE
               INDEX = INDEX2
               DO 280 J = 1, NDIM
                    XI (INDEX) = PR (J)
                    INDEX = INDEX + 1
 280           CONTINUE
               XIVAL (HIGH) = YPR
          END IF
      GOTO 20
      END


      REAL FUNCTION AUX_SOLV (LOSS, MODE, FIRST)

      IMPLICIT NONE

      REAL FIRST (*), LOSS
      INTEGER  MODE
      EXTERNAL LOSS

C     if MODE is non-zero, the first FIRST is taken from input
C     FIRST has NTOT = NXV + NYV = NCOR + 1 elements
C     WORK has (NTOT+1)**2 elements

      INTEGER*2 MAXCOR
      PARAMETER (MAXCOR = 5)
      REAL SAVED (MAXCOR+1), XIVAL (MAXCOR+2),
     1     XI ((MAXCOR+1)*(MAXCOR+2)), WTEMP (MAXCOR+1)
      COMMON /WORK/ SAVED, XIVAL, XI, WTEMP

      INTEGER*2       NCOR, NXV, NYV, NTOT, N1, SUMFRQ
      COMMON /CORLOS/ NCOR, NXV, NYV, NTOT, N1, SUMFRQ

      REAL VAL_ABS_TOL, VAL_REL_TOL
      REAL LOVAL, OLDVAL, RTOL, GAP
      INTEGER*2  TIMES, I, J, IG, IND2, INDEX, LOW, ITER
      REAL TOP, BOTTOM
      PARAMETER (BOTTOM  = 0.0)
      PARAMETER (TOP  = 100.0)

      VAL_ABS_TOL = 1.0E-4
      VAL_REL_TOL = 1.0E-6

C      xival = work (1..(ntot+1))
C      xi = work ((ntot+2)..(ntot+1)*(ntot+1))
      
      IF (MODE .EQ. 0) THEN
          GAP = (TOP - BOTTOM) / (NXV + 1)
          DO 20 I = 1, NXV
               FIRST (I) = BOTTOM + I * GAP
 20       CONTINUE
          GAP = (TOP - BOTTOM) / (NYV + 1)
          DO 40 I = 1, NYV
               FIRST (I+NXV) = TOP - I * GAP
 40       CONTINUE
      ENDIF
      TIMES = 2
      LOVAL = 1.0E30
 50   CONTINUE
          OLDVAL = LOVAL
          TIMES = TIMES - 1
          XIVAL (1) = LOSS (FIRST)
          DO 60 J = 1, NTOT
               XI (J) = FIRST (J)
 60       CONTINUE
          INDEX = NTOT
          IND2 = 1
          GAP = TOP - FIRST (NXV)
          IG = NXV         
          IF (FIRST (1) .GT. GAP) THEN
               GAP = FIRST (1)
               IG = 0
          ENDIF
          DO 70 J = 2, NXV
               IF (FIRST (J) - FIRST (J-1) .GT. GAP) THEN
                    GAP = FIRST (J) - FIRST (J-1)
                    IG = J-1
               ENDIF
 70       CONTINUE
          GAP = (7 * GAP) / 8
C              was GAP / 2
          IF (IG .LT. NXV) THEN
               DO 75 I = 1, NTOT
                    WTEMP (I) = FIRST (I)
 75            CONTINUE
               DO 80 I = IG+1, NXV
                    WTEMP (I) = WTEMP (I) - GAP
                    IND2 = IND2 + 1
                    XIVAL (IND2) = LOSS (WTEMP)
                    DO 78 J = 1, NTOT
                         XI (J+INDEX) = WTEMP (J)
 78                 CONTINUE
                    INDEX = INDEX + NTOT
 80            CONTINUE
          ENDIF
          IF (IG .GT. 0) THEN
               DO 82 I = 1, NTOT
                    WTEMP (I) = FIRST (I)
 82            CONTINUE
               DO 88 I = IG, 1, -1
                    WTEMP (I) = WTEMP (I) + GAP
                    IND2 = IND2 + 1
                    XIVAL (IND2) = LOSS (WTEMP)
                    DO 85 J = 1, NTOT
                         XI (J+INDEX) = WTEMP (J)
 85                 CONTINUE
                    INDEX = INDEX + NTOT
 88            CONTINUE
          ENDIF
C
          GAP = TOP - FIRST (NXV+1)
          IG = NXV         
          IF (FIRST (NTOT) .GT. GAP) THEN
               GAP = FIRST (NTOT)
               IG = NTOT
          ENDIF
          DO 90 J = NXV+2, NTOT
               IF (FIRST (J-1) - FIRST (J) .GT. GAP) THEN
                    GAP = FIRST (J-1) - FIRST (J)
                    IG = J-1
               ENDIF
 90       CONTINUE
          GAP = (7 * GAP) / 8
C              was GAP / 2
          IF (IG .LT. NTOT) THEN
               DO 92 I = 1, NTOT
                    WTEMP (I) = FIRST (I)
 92            CONTINUE
               DO 94 I = IG+1, NTOT
                    WTEMP (I) = WTEMP (I) + GAP
                    IND2 = IND2 + 1
                    XIVAL (IND2) = LOSS (WTEMP)
                    DO 93 J = 1, NTOT
                         XI (J+INDEX) = WTEMP (J)
 93                 CONTINUE
                    INDEX = INDEX + NTOT
 94            CONTINUE
          ENDIF
          IF (IG .GT. NXV) THEN
               DO 96 I = 1, NTOT
                    WTEMP (I) = FIRST (I)
 96            CONTINUE
               DO 99 I = IG, NXV+1, -1
                    WTEMP (I) = WTEMP (I) - GAP
                    IND2 = IND2 + 1
                    XIVAL (IND2) = LOSS (WTEMP)
                    DO 98 J = 1, NTOT
                         XI (J+INDEX) = WTEMP (J)
 98                 CONTINUE
                    INDEX = INDEX + NTOT
 99            CONTINUE
          ENDIF
C
          CALL AMOEBA (LOSS, NTOT, XI, XIVAL,
     1                 VAL_ABS_TOL, VAL_REL_TOL, ITER)
          LOW = NTOT + 1
          LOVAL = XIVAL (LOW)
          DO 120 I = 1, NTOT
               IF (XIVAL (I) .LT. LOVAL) THEN
                    LOW = I
                    LOVAL = XIVAL (I)
               END IF
 120      CONTINUE
          INDEX = (LOW - 1) * NTOT
          DO 130 J = 1, NTOT
               FIRST (J) = XI (J+INDEX)
 130      CONTINUE
          RTOL = ABS (LOVAL - OLDVAL)
C      writeln (Lst, 'MinAmoeba: Ending value is ', loval:12:6, ' after ',
C                           iter, ' iterations.');
      IF ((TIMES .GT. 0) .OR. ((RTOL .GT. VAL_ABS_TOL) .AND.
     1    (RTOL .GT. VAL_REL_TOL * 0.5 * (ABS (OLDVAL) + ABS (LOVAL)))))
     2         GOTO 50

      AUX_SOLV = LOVAL
      RETURN
      END


      REAL FUNCTION SOLVE_MIN (NCORN, FIRST, NX, NY, TYPE, DEVFRQ)

      IMPLICIT NONE

      INTEGER*2 NCORN, NX, NY, TYPE, DEVFRQ
      REAL FIRST (*)

C     FIRST has NTOT = NXV + NYV = NCORN + 1 elements
C     WORK has (NTOT+1)**2 + NTOT elements

      INTEGER*2       NCOR, NXV, NYV, NTOT, N1, SUMFRQ
      COMMON /CORLOS/ NCOR, NXV, NYV, NTOT, N1, SUMFRQ
C      INTEGER*2 MAXPTS
C      PARAMETER (MAXPTS = 200)
C      REAL XARR1 (MAXPTS), YARR1 (MAXPTS), XARR2 (MAXPTS), YARR2(MAXPTS)
C      COMMON /CORPTS/ XARR1, YARR1, XARR2, YARR2
      INTEGER*2 MAXCOR
      PARAMETER (MAXCOR = 5)
      REAL SAVED (MAXCOR+1), XIVAL (MAXCOR+2),
     1     XI ((MAXCOR+1)*(MAXCOR+2)), WTEMP (MAXCOR+1)
      COMMON /WORK/ SAVED, XIVAL, XI, WTEMP

      REAL LOVAL1, LOVAL2, LOSS1, LOSS2, AUX_SOLV, DUMMY
      EXTERNAL LOSS1, LOSS2
      INTEGER*2 J

      NCOR = NCORN
      NXV = (NCOR + 2) / 2
      NYV = (NCOR + 1) / 2
      NTOT = NCOR + 1
      LOVAL1 = AUX_SOLV (LOSS1, 0, SAVED)
      NXV = (NCOR + 1) / 2
      NYV = (NCOR + 2) / 2
      LOVAL2 = AUX_SOLV (LOSS2, 0, FIRST)
      IF (LOVAL1 .LT. LOVAL2) THEN
          NXV = (NCOR + 2) / 2
          NYV = (NCOR + 1) / 2
          DO 50 J = 1, NTOT
               FIRST (J) = SAVED (J)
 50       CONTINUE
          SOLVE_MIN = LOVAL1
          DUMMY = LOSS1 (FIRST)
          TYPE = 1
      ELSE
          SOLVE_MIN = LOVAL2
          DUMMY = LOSS2 (FIRST)
          TYPE = 2
      END IF
      NX = NXV
      NY = NYV
      DEVFRQ = SUMFRQ
      RETURN
      END


      SUBROUTINE SETUP_POINTS (XX, YY, YYES, NNO, NP)
      IMPLICIT NONE

      INTEGER*2 NP
      REAL XX (NP), YY (NP), YYES (NP), NNO (NP)

      INTEGER*2       NCOR, NXV, NYV, NTOT, N1, SUMFRQ
      COMMON /CORLOS/ NCOR, NXV, NYV, NTOT, N1, SUMFRQ
INCLUDE 'MPARMLIN'
      REAL  XARR (MIEND), YARR (MIEND), YES (MIEND), NO (MIEND)
      COMMON /POINTS/ XARR, YARR, YES, NO

C      INTEGER*2 MAXPTS
C      PARAMETER (MAXPTS = 200)
C      REAL XARR1 (MAXPTS), YARR1 (MAXPTS), XARR2 (MAXPTS), YARR2(MAXPTS)
C      COMMON /CORPTS/ XARR1, YARR1, XARR2, YARR2
      INTEGER*2 I

      N1 = 0
      DO 50 I = 1, NP
          N1 = N1 + 1
          XARR (N1) = XX (I)
          YARR (N1) = YY (I)
          YES (N1) = YYES (I)
          NO (N1) = NNO (I)
 50   CONTINUE
C
      CALL SORT_PTS (N1, XARR, YARR, YES, NO)
      RETURN
      END
C
      SUBROUTINE PLOT (XX, YY, VALUE, THR1, THR2, NP, ITEM, FIRST,
     1                 NX, NY, TYPE, NCORN)
      IMPLICIT NONE

      INTEGER*2 NP, ITEM, NX, NY, TYPE, NCORN
      REAL XX (NP), YY (NP), VALUE (NP), FIRST (*), THR1, THR2

      LOGICAL*2  GROK
      INTEGER*2  J, K, KK
      INTEGER*2 MAXCOR
      PARAMETER (MAXCOR = 5)
      REAL XL (MAXCOR/2+3), YL (MAXCOR/2+3)
      CHARACTER*12 NAME
      CHARACTER*8 CHITEM
      LOGICAL*2  TMPOPEN
      INTEGER*2  ITEMP
      COMMON /GRLOC/ TMPOPEN, ITEMP

      TMPOPEN = .TRUE.
      IF (NCORN .EQ. 0) THEN
          NAME = 'EXPOL'
      ELSE IF (NCORN .EQ. 1) THEN
          NAME = 'EXATC'
      ELSE IF (NCORN .EQ. 2) THEN
          NAME = 'EXPRM'
      ELSE IF (NCORN .EQ. 3) THEN
          NAME = 'EXMOD'
      ELSE
          TMPOPEN = .FALSE.
      ENDIF
      J = ITEM / 10
      K = ITEM - 10 * J
      NAME = NAME (1:5) // CHAR(J+48) // CHAR(K+48) // '.SCR'
      IF (J .EQ. 0) THEN
          CHITEM = 'ITEM   ' // CHAR(ITEM+48)
      ELSE
          CHITEM = 'ITEM  ' // CHAR(J+48) // CHAR(K+48)
      ENDIF

      XL (1) = 0.0
      DO 20 J = 1, NX
          XL (J+1) = FIRST (J)
 20   CONTINUE
      XL (NX+2) = 100.0
      YL (1) = 100.0
      DO 30 J = 1, NY
          YL (J+1) = FIRST (NX+J)
 30   CONTINUE
      YL (NY+2) = 0.0
       
C      WRITE(*,72) CHAR (7), CHAR (7)
      CALL graphicsmode (GROK)
      IF (.NOT. GROK)  THEN
          WRITE (*,*)  ' NO GRAPHICS AVAILABLE'
          RETURN
      END IF

      ITEMP = 22
      IF (TMPOPEN) THEN     
          OPEN (ITEMP, FILE = NAME, ACCESS='SEQUENTIAL',
     $             FORM='FORMATTED', ERR=100)
      ENDIF
      WRITE (ITEMP,'(A)') 'GRAPHICS'
      GOTO 200
 100  TMPOPEN = .FALSE.
 200  CONTINUE
                          
      CALL drawframe (5.0, 55.9, 1.0, 23.4)
      IF (TMPOPEN)  WRITE (ITEMP, '(A)')
     1               'FRAM     5.000    55.900     1.000    23.400'
      CALL putgtext ('100..', -0.5,  99.0, INT2(2), INT2(0))
      IF (TMPOPEN)  WRITE (ITEMP, '(A)')
     1           'GTXT   5100..    -0.500    99.000    2    0'
      CALL putgtext ('50..', -0.5, 49.0, INT2(2), INT2(0))
      IF (TMPOPEN)  WRITE (ITEMP, '(A)')
     1           'GTXT   450..    -0.500    49.000    2    0'
      CALL putgtext ('0..', -0.5, -1.0, INT2(2), INT2(0))
      IF (TMPOPEN)  WRITE (ITEMP, '(A)')
     1           'GTXT   30..    -0.500    -1.000    2    0'
      CALL putgtext (CHITEM, 105.0,  99.0, INT2(0), INT2(0))
      IF (TMPOPEN)  WRITE (ITEMP, '(A,A8,A)')
     1         'GTXT   8', CHITEM, '   105.000    99.000    0    0'
      NAME = NAME (1:5) // ' ROLE'
      CALL putgtext (NAME(1:10), 105.0,  95.0, INT2(0), INT2(0))
      IF (TMPOPEN)  WRITE (ITEMP, '(A,A10,A)')
     1         'GTXT  10', NAME(1:10), '   105.000    95.000    0    0'

      DO 70 K = 1, NP
          IF (VALUE (K) .LE. THR1) THEN
               KK = 1
          ELSE IF (VALUE (K) .LT. THR2) THEN
               KK = 2
          ELSE
               KK = 3
          END IF
          CALL putnum (KK, XX (K), YY (K))
          IF (TMPOPEN) WRITE (ITEMP, '(A4,I5,2F10.3)') 'NUMB',
     1                         KK, XX (K), YY (K)
 70   CONTINUE
      IF (TYPE .EQ. 1) THEN
          DO 110 J = 1, NY
               CALL OUTLINE (XL (J+1), YL (J), XL (J+1), YL (J+1))
               CALL OUTLINE (XL (J+1), YL (J+1), XL (J+2), YL (J+1))
 110      CONTINUE
          IF (NX .GT. NY) THEN
               CALL OUTLINE (XL (NX+1), YL (NX), XL (NX+1), YL (NX+1))
          END IF
      ELSE
          DO 130 J = 1, NX
               CALL OUTLINE (XL (J), YL (J+1), XL (J+1), YL (J+1))
               CALL OUTLINE (XL (J+1), YL (J+1), XL (J+1), YL (J+2))
 130      CONTINUE
          IF (NY .GT. NX) THEN
               CALL OUTLINE (XL (NY), YL (NY+1), XL (NY+1), YL (NY+1))
          END IF
      ENDIF
      CALL endgraph
      IF (TMPOPEN) THEN
          WRITE (ITEMP, '(A)') 'END '
          CLOSE (ITEMP)
      END IF

      RETURN
CY   72 FORMAT(1X,2A1)
      END

      SUBROUTINE OUTLINE (X1, Y1, X2, Y2)
      IMPLICIT NONE
      REAL X1, Y1, X2, Y2
      INTEGER*2 NWRITE,NTABLE,IEXT
      COMMON/IO/NWRITE,NTABLE,IEXT
      LOGICAL*2  TMPOPEN
      INTEGER*2  ITEMP
      COMMON /GRLOC/ TMPOPEN, ITEMP

      WRITE (NWRITE, 900) X1, Y1, X2, Y2
      CALL drawline ( X1, Y1, X2, Y2)
      IF (TMPOPEN) WRITE (ITEMP,  '(A4,4F10.3)') 'LINE', X1, Y1, X2, Y2

      RETURN
 900  FORMAT (' Dividing line from (', F6.2, ',', F6.2, ') to (',
     1         F6.2, ',', F6.2, ')')
      END

