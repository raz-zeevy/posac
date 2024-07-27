      SUBROUTINE PRNT (IFREQ, IPRF, ISCO, XY, NV, NP)

INCLUDE 'MPARMLIN'

      COMMON/TEST/ITESTN,ITESTX
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/VARINT/INTERN
      COMMON/PARAM/IEXDIAGRM, ITEMDGPLT, IWRTFLS
      COMMON /WCHAR/ FMT20,FMT1,FMT3,FMT4,FMT5,FMT6,FMT7,FMT8,FMT9,CH,
     $               DUMMY
      COMMON/LAB/LABEL (MNV),PATH
      COMMON/NPG/NEWPAGE, PATHLEN
C
      INTEGER*2 NV, NP, IFREQ(NP),IPRF(NV,NP),ISCO(NP)
      REAL      XY(NP,2)
C
      CHARACTER*40 LABEL
      CHARACTER*80 PATH
      INTEGER*2 NEWPAGE, PATHLEN
      CHARACTER FMT20*66,FMT1*13,FMT3*3,FMT4*3,FMT5*2,FMT6*45
      CHARACTER FMT7*4,FMT8*38,FMT9*49,CH*1
      CHARACTER*208 DUMMY
C
      INTEGER*2 NPLINE, IXX, K
C
C **********************************************************************
C
      IF (IWRTFLS .GT. 0) THEN
          IF (PATHLEN .GT. 0) THEN
               OPEN (IWRTFLS, FILE = PATH(1:PATHLEN)//'SOLUTION.PSC')
          ELSE
               OPEN (IWRTFLS, FILE = 'SOLUTION.PSC')
          END IF
      END IF
C
C  INITIALIZING VARIABLE FORMAT
C
      NPLINE=MIN0(INTERN,20)
      FMT1='(1X,I3,A1,1X,'
      WRITE (FMT3,'(I3)') NPLINE
      FMT4='I2,'
      IXX=(20-NPLINE)*2+2
      WRITE (FMT5,'(I2)') IXX
      FMT6='X,I3,2X,I4,10X,F6.2,4X,F6.2,14X,F6.2,4X,F6.2)'
      FMT20=FMT1//FMT3//FMT4//FMT5//FMT6
C
      IXX = (16-NPLINE)*2
      IF (IXX .GT. 0) THEN
          WRITE (FMT7,'(I2,2HX,)') IXX
      ELSE
          FMT7 = '   '
      END IF
      FMT8 = 'I4,I5,1X,F6.2,2X,F6.2,4X,F6.2,2X,F6.2)'
      FMT9 = '('//FMT3//FMT4//FMT7//FMT8
C
C **********************************************************************
C
      WRITE (NWRITE,100)
C
      DO 10 K=1,NP
C
          X=XY(K,1)
          Y=XY(K,2)
          XPRIM=X-Y+100.
          YPRIM=X+Y
C
          IF ( (K.EQ.1 .AND. ITESTX.EQ.0) .OR.
     $                    (K.EQ.NP .AND. ITESTN.EQ.0) ) THEN
               CH = '*'
          ELSE
               CH = ' '
          END IF
          WRITE(NWRITE,FMT20) K, CH, (IPRF(I,K),I=1,NPLINE),
     $                        ISCO(K),IFREQ(K),X,Y,YPRIM,XPRIM
          IF (IWRTFLS .GT. 0)   WRITE (IWRTFLS, FMT9)
     $                              (IPRF(I,K),I=1,NPLINE), ISCO(K),
     $                              IFREQ(K),X,Y,YPRIM,XPRIM
C
          IF (INTERN.GT.20) WRITE(NWRITE,201) (IPRF(I,K),I=20,INTERN)
C
   10 CONTINUE
C
      IF (ITESTN+ITESTX.LE.1) WRITE(NWRITE,1600)
C
      IF (IWRTFLS .GT. 0) CLOSE (IWRTFLS)
C
      RETURN
C
  100 FORMAT(//,67X,16HBASE COORDINATES,7X,
     $              23HTRANSFORMED COORDINATES,/,
     $      /,1X,3H ID,3X,7HPROFILE,34X,3HSCO,2X,4HFREQ,
     $           15X,1HX,9X,1HY,15X,5HJOINT,3X,7HLATERAL,
     $         /,2X,2H--,3X,7(1H-),34X,3H---,2X,4H----,15X,1H-,
     $                       9X,1H-,15X,5(1H-),3X,7(1H-))
  201 FORMAT(6X,20I2)
 1600 FORMAT(///,37H    *EXTREME PROFILE ADDED BY PROGRAM   )
C
      END

      SUBROUTINE MUVRXY (IFREQ, IPRF, XY, VAR1, VAR2, NV, NP)

C THIS SUB. COMPUTES MONOTONICITY COEFFICIENTS BETWEEN EACH
C   VARIABLE IPRF(I,.)  AND
C    X        : RMUX
C    Y        : RMUY
C    X+Y      : RMUJ  (J FOR JOINT  )
C    X-Y      : RMUL  (L FOR LATERAL)
C    MAX(X,Y) : RMUMAX
C    MIN(X,Y) : RMUMIN
C
C IFREQ(IP) : FREQUENCY OF PROFILE IP  (IP=IPRF(.,IP))
C IPRF(I,.) : VARIABLE (ITEM) NUMBER I
C XY(IP,1)  : COORDINATE X OF PROFILE IP
C XY(IP,2)  : COORDINATE Y OF PROFILE IP
C VAR1(.) AND VAR2(.) : WORKING AREAS

      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/VARINT/INTERN
      COMMON/PARAM/IEXDIAGRM, ITEMDGPLT, IWRTFLS
      COMMON /WCHAR/ PRMUJ,PRMUL,PRMUX,PRMUY,PRMUMIN,PRMUMAX,DUMMY

INCLUDE 'MPARMLIN'

      COMMON/LAB/LABEL (MNV),PATH
      COMMON/NPG/NEWPAGE, PATHLEN
C
      CHARACTER*40 LABEL
      CHARACTER*80 PATH
      INTEGER*2 NEWPAGE, PATHLEN
C
      INTEGER*2 NV, NP, IFREQ(NP),IPRF(NV,NP)
      REAL      XY(NP,2),VAR1(NP),VAR2(NP)
C
      CHARACTER*6 PRMUJ,PRMUL,PRMUX,PRMUY,PRMUMIN,PRMUMAX
      CHARACTER*198 DUMMY(2)
C
      INTEGER*2 I, J
C
C **********************************************************************
C
      WRITE(NWRITE,100)
      IF (IWRTFLS .GT. 0) THEN
          IF (PATHLEN .GT. 0) THEN
               OPEN (IWRTFLS, FILE = PATH(1:PATHLEN)//'ITEMFACT.PSC')
          ELSE
               OPEN (IWRTFLS, FILE = 'ITEMFACT.PSC')
          END IF
      END IF
C
      DO 10 I=1,INTERN
C
C  STORING IPRF(I,.) IN VAR1(.)
          DO 20 J=1,NP
               VAR1(J)=IPRF(I,J)
   20     CONTINUE
C ----------- 1 -----------
C  STORING X IN VAR2
          DO 30 J=1,NP
               VAR2(J)=XY(J,1)
   30     CONTINUE
C
C  COMPUTING RMUX
          RMUX=RMU2(IFREQ,VAR1,VAR2,NP)
C ----------- 2 -----------
C  STORING Y IN VAR2
          DO 40 J=1,NP
               VAR2(J)=XY(J,2)
   40     CONTINUE
C
C  COMPUTING RMUY
          RMUY=RMU2(IFREQ,VAR1,VAR2,NP)
C ----------- 3 -----------
C  STORING (X+Y) IN VAR2
          DO 50 J=1,NP
               VAR2(J)=XY(J,1)+XY(J,2)
   50     CONTINUE
C
C  COMPUTING RMUJ
          RMUJ=RMU2(IFREQ,VAR1,VAR2,NP)
C ----------- 4 -----------
C  STORING (X-Y) IN VAR2
          DO 60 J=1,NP
               VAR2(J)=XY(J,1)-XY(J,2)
   60     CONTINUE
C
C  COMPUTING RMUL
          RMUL=RMU2(IFREQ,VAR1,VAR2,NP)
C ----------- 5 -----------
C  STORING MAX(X,Y) IN VAR2
          DO 70 J=1,NP
               VAR2(J)=AMAX1(XY(J,1),XY(J,2))
   70     CONTINUE
C
C  COMPUTING RMUMAX
          RMUMAX=RMU2(IFREQ,VAR1,VAR2,NP)
C ----------- 6 -----------
C  STORING MIN(X,Y) IN VAR2
          DO 80 J=1,NP
               VAR2(J)=AMIN1(XY(J,1),XY(J,2))
   80     CONTINUE
C
C  COMPUTING RMUMIN
          RMUMIN=RMU2(IFREQ,VAR1,VAR2,NP)
C -------------------------
C  PRINTING RESULTS FOR VARIABLE IPRF(I,.)
C
          WRITE (PRMUJ,'(F6.2)') RMUJ
          WRITE (PRMUL,'(F6.2)') RMUL
          WRITE (PRMUX,'(F6.2)') RMUX
          WRITE (PRMUY,'(F6.2)') RMUY
          WRITE (PRMUMIN,'(F6.2)') RMUMIN
          WRITE (PRMUMAX,'(F6.2)') RMUMAX
C
          IF (RMUJ.EQ.9.) PRMUJ='   .  '
          IF (RMUL.EQ.9.) PRMUL='   .  '
          IF (RMUX.EQ.9.) PRMUX='   .  '
          IF (RMUY.EQ.9.) PRMUY='   .  '
          IF (RMUMIN.EQ.9.) PRMUMIN='   .  '
          IF (RMUMAX.EQ.9.) PRMUMAX='   .  '
C
          WRITE(NWRITE,200) I,PRMUJ,PRMUL,PRMUX,PRMUY,PRMUMIN,PRMUMAX
          IF (IWRTFLS .GT. 0)     WRITE (IWRTFLS,300)
     $                       PRMUJ,PRMUL,PRMUX,PRMUY,PRMUMIN,PRMUMAX
   10 CONTINUE
C
      IF (IWRTFLS .GT. 0) CLOSE (IWRTFLS)
      RETURN
C
  100 FORMAT(//,2X,40HCOEFFICIENT OF WEAK MONOTONICITY BETWEEN,
     $       37H EACH OBSERVED ITEM AND THE FACTORS :,/,2X,
     $       37HJ (I.E. X+Y) , L (I.E. X-Y) , X , Y ,,
     $       38H P (I.E. MIN(X,Y)) , Q (I.E. MAX(X,Y)),//,
     $       2X,4HITEM,5X,1HJ,5X,1HL,5X,1HX,5X,1HY,5X,1HP,5X,1HQ,/,
     $       2X,4H----,5X,1H-,5X,1H-,5X,1H-,5X,1H-,5X,1H-,5X,1H-)
  200 FORMAT(2X,I3,1X,6A6)
  300 FORMAT(6A6)
C
      END

      FUNCTION RMU2 (IFREQ,VAR1,VAR2,N)

C  THIS FUNCTION COMPUTES A MONOTONICITY COEFFICIENT
C  BETWEEN VAR1 AND VAR2
C
      COMMON/ZEROES/ZERO,ZEROMU2
C
      INTEGER*2 N, IFREQ(N)
      REAL      VAR1(N),VAR2(N)
C
      INTEGER*4 IFK
      INTEGER*2 N1, K, L1, L
C
      U=0.
      V=0.
      RMU2=0.
      N1=N-1
      DO 10 K=1,N1
          IFK=IFREQ(K)
          VAR1K=VAR1(K)
          VAR2K=VAR2(K)
          L1=K+1
          DO 20 L=L1,N
               RNUM=IFK*IFREQ(L)*(VAR1K-VAR1(L))*(VAR2K-VAR2(L))
               RDEN=ABS(RNUM)
               U=U+RNUM
               V=V+RDEN
   20     CONTINUE
   10 CONTINUE
      IF(V.LT.ZEROMU2) THEN
          RMU2=9.
          RETURN
      END IF
      RMU2=U/V
      RETURN
      END

