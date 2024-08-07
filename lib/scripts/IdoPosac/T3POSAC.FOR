

      SUBROUTINE POFREQ(IFREQ, IPRF, ISCO, ORGFRQ, NCAS, NV)

      PARAMETER (IDMAX=500)
      PARAMETER (IDLEN=10)
C
C  COMPUTES FREQUENCIES AND SCORES OF INTERNAL PROFILES
C
      INTEGER*2 NCAS,NV
      INTEGER*2 IFREQ(NCAS), IPRF(NV,NCAS), ISCO(NCAS), ORGFRQ(NCAS)
C
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/VARINT/INTERN
      COMMON/ZIHOUY/ID
      COMMON/PARZIH/IND,NN,INDEX,NONUL
C
      CHARACTER*10 ID(IDMAX)
C
      INTEGER*2 IND,NN,INDEX(IDMAX),NONUL(IDMAX)
C
      INTEGER*2 I,II,J,NCASI,NCAS1,J1,K,IS
C
C **********************************************************************
C
      REWIND NSCR
      DO 10 I=1,NCAS
       IF (I.LE.IDMAX) II=I
       READ(NSCR) ID(II),IFREQ(I),(IPRF(J,I),J=1,NV)
       ORGFRQ (I) = IFREQ (I)
   10 CONTINUE
C  COMPUTING FREQUENCIES OF PROFILES
      NCASI=NCAS-1
      NCAS1=NCAS
      NN=0
      IND=0
      DO 20 I=1,NCASI
       IF(IFREQ(I).EQ.0) GO TO 20
       IF (I.LE.IDMAX) THEN
       IND=IND+1
       INDEX(IND)=I
       NN=NN+1
       NONUL(NN)=I
       ENDIF
       J1=I+1
       DO 30 J=J1,NCAS
          DO 40 K=1,INTERN
             IF(IPRF(K,I).NE.IPRF(K,J)) GO TO 30
   40     CONTINUE
          IFREQ(I)=IFREQ(I)+IFREQ(J)
          IFREQ(J)=0
          NCAS1=NCAS1-1
          IF (J.LE.IDMAX) THEN
          IND=IND+1
          INDEX(IND)=J
          ENDIF
   30  CONTINUE
   20 CONTINUE
C
C  FOR THE LAST SUBJECT ....
      IF (IFREQ(NCAS) .EQ. 0) GO TO 25
      IF (NCAS.LE.IDMAX) THEN
      IND = IND +1
      INDEX(IND) = NCAS
      NN = NN + 1
      NONUL(NN) = NCAS
      ENDIF
   25 CONTINUE
C  COMPUTING SCORES
      DO 60 I=1,NCAS
C  PUT SCORE=-1 IF FREQ=0
       IF(IFREQ(I).EQ.0) GO TO 80
       IS=0
       DO 70 J=1,INTERN
          IS=IS+IPRF(J,I)
   70  CONTINUE
       ISCO(I)=IS
       GO TO 60
   80  ISCO(I)=-1
   60 CONTINUE
      RETURN
C
      END

      SUBROUTINE PRFOUT (IFREQ, IPRF, ISCO, ORGFRQ, NCAS, NV)

      PARAMETER (IDMAX=500)
      PARAMETER (IDLEN=10)
C
C  THIS SUB. REJECTS CASES WHICH CAN GIVE FREQUENCY
C  LE.LOWFRQ
C
      INTEGER*2 NCAS,NV
      INTEGER*2 IFREQ(NCAS), IPRF(NV,NCAS), ISCO(NCAS), ORGFRQ (NCAS)
C
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/VARINT/INTERN
      COMMON/REJECT/ LOWFRQ, IFRQONE
      COMMON/ZIHOUY/ID
C
      CHARACTER*10 ID(IDMAX)
C
      INTEGER*2 I,NCASI,J,J1,K,LAST,II,NEWCAS,IREJ
C
C  LOWFRQ IS THE FREQUENCY SUCH THAT IF A CASE GIVE
C  A FREQUENCY LE.LOWFRQ THEN THIS CASE IS REJECTED
C
C  IF LOWFRQ=1 THE TREATMENT IS MORE SIMPLE
      IF (LOWFRQ.NE.1) GO TO 8
      DO 5 I=1,NCAS
       IF (IFREQ(I).GT.1) GO TO 5
       IF (ISCO(I).EQ.-1) GO TO 5
       ISCO(I)=-2
    5 CONTINUE
      GO TO 35
    8 CONTINUE
      NCASI=NCAS-1
      DO 10 I=1,NCASI
       IF (IFREQ(I).GT.LOWFRQ) GO TO 10
       IF(ISCO(I).EQ.-1) GO TO 10
       IF(ISCO(I).EQ.-2) GO TO 10
       ISCO(I)=-2
       J1=I+1
       DO 20 J=J1,NCAS
          IF(ISCO(J).NE.-1) GO TO 20
C  HERE SELECTING CASES J WHICH HAVE SAME PROFILE
C  THAN I AND MARKING -2 TO REJECT THEM
          DO 30 K=1,INTERN
             IF(IPRF(K,I).NE.IPRF(K,J)) GO TO 20
   30     CONTINUE
          ISCO(J)=-2
   20  CONTINUE
   10 CONTINUE
      LAST=IFREQ(NCAS)
      IF(LAST.GT.0.AND.LAST.LE.LOWFRQ) ISCO(NCAS)=-2
   35 CONTINUE
C  NOW REJECTING CASES WHICH GIVE FREQUENCIES LE.LOWFRQ
C  THE RETAINED ONES ARE WRITTEN ON UNIT NSCR
      REWIND NSCR
      NEWCAS=0
      DO 40 I=1,NCAS
       IF (ISCO(I).EQ.-2) GO TO 40
       NEWCAS=NEWCAS+1
       IF (I.LE.IDMAX) II=I
C         WRITE(NSCR) ID(II),IFREQ(I),(IPRF(K,I),K=1,NV)
       WRITE(NSCR) ID (II), ORGFRQ (I), (IPRF (K,I),K=1,NV)
   40 CONTINUE
C  REJECTED CASES IREJ
      IREJ=NCAS-NEWCAS
      IF(IREJ.EQ.0) RETURN
      WRITE(NWRITE,100) LOWFRQ,IREJ,NEWCAS
C  AFTER REJECTING CASES NCAS BECOMES
      NCAS=NEWCAS
      IF (NCAS.LT.3)  WRITE(NWRITE,200)
      IF (NCAS.LT.3)  STOP
      CALL POFREQ (IFREQ,IPRF,ISCO, ORGFRQ, NCAS,NV)
      RETURN
C
  100 FORMAT(/,' LOWFRQ=',I4,'   IREJ=',I4,'   NEWCAS=',I4)
  200 FORMAT(/,'  ERROR  NCAS.LT.3 ')
C
      END

      SUBROUTINE ADDMNX (IPMIN, IPMAX, IFREQ, IPRF, ISCO,
     $                    NV, NCAS2)
C
      PARAMETER (IDMAX=500)
      PARAMETER (IDLEN=10)
C
C  ADDS MAXIMAL AND MINIMAL PROFILES IF THEY ARE ABSENT
C
      COMMON/TEST/ITESTN,ITESTX
      COMMON/VARINT/INTERN
      COMMON/ZIHOUY/ID
      COMMON/PARZIH/IND,NN,INDEX,NONUL
C
      CHARACTER*10 ID(IDMAX)
C
      INTEGER*2 NV, NCAS2
      INTEGER*2 IND,NN,INDEX(IDMAX),NONUL(IDMAX)
      INTEGER*2 IPMIN(NV),IPMAX(NV),IFREQ(NCAS2),IPRF(NV,NCAS2),
     $                                     ISCO(NCAS2)
C
      INTEGER*2 I,J,IS
C
C **********************************************************************
C
      ITESTN=0
      ITESTX=0
C  ITESTN OR ITESX=0 MEANS THAT MINIMAL OR
C  MAXIMAL PROFILES DON'T EXIST .
      DO 10 I=1,NCAS2
       DO 20 J=1,INTERN
          IF(IPRF(J,I).NE.IPMIN(J)) GO TO 30
   20  CONTINUE
       ITESTN=1
   30  DO 40 J=1,INTERN
          IF(IPRF(J,I).NE.IPMAX(J)) GO TO 10
   40  CONTINUE
       ITESTX=1
   10 CONTINUE
      IF(ITESTN.EQ.1) GO TO 50
      NCAS2=NCAS2+1
      IS=0
      DO 60 J=1,INTERN
       IPRF(J,NCAS2)=IPMIN(J)
       IS=IS+IPMIN(J)
   60 CONTINUE
      IFREQ(NCAS2)=1
      ISCO(NCAS2)=IS
      IF (NCAS2.LE.IDMAX) THEN
      IND = IND + 1
      INDEX(IND) = NCAS2
      NN = NN + 1
      NONUL(NN) = NCAS2
      ID(NCAS2) = 'NOBODY'
      ENDIF
   50 IF(ITESTX.EQ.1) RETURN
      NCAS2=NCAS2+1
      IS=0
      DO 70 J=1,INTERN
       IPRF(J,NCAS2)=IPMAX(J)
       IS=IS+IPMAX(J)
   70 CONTINUE
      IFREQ(NCAS2)=1
      ISCO(NCAS2)=IS
      IF (NCAS2.LE.IDMAX) THEN
      IND = IND + 1
      INDEX(IND) = NCAS2
      NN = NN + 1
      NONUL(NN) = NCAS2
      ID(NCAS2) = 'NOBODY'
      ENDIF
C
      RETURN
C
      END

      SUBROUTINE DECRES (ICOMP, IFREQ, IPRF, ISCO, NCAS2, NV)

C  ORDERS THE PROFILES ACCORDING TO THE DECREASING SCORES.
C  BUT OF COURSE FOR THE SAME SCORE THE ORDER OF THE
C  PROFILES IS RANDOM

      INTEGER*2 NCAS2,NV
      INTEGER*2 ICOMP(NCAS2),IFREQ(NCAS2),IPRF(NV,NCAS2),ISCO(NCAS2)
C
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/CC/ISMN,ISMX,IEND
      COMMON/VARINT/INTERN
C
      INTEGER*2 ISMN,ISMX,IEND
C
      INTEGER*2 I,IS,J,IW,IARG
C
C **********************************************************************
C
C  INITIALIZE ICOMP(.)
      DO 5 I=1,NCAS2
       ICOMP(I)=I
    5 CONTINUE
C
      I=1
      IS=ISMX
   51 CONTINUE
      J=I
   31 CONTINUE
      IF(ISCO(J)-IS) 10,20,10
   10 IF(J-NCAS2) 30,40,30
   30 J=J+1
      GO TO 31
   40 IF(IS-ISMN) 50,62,50
   50 IS=IS-1
      GO TO 51
   20 IF(ISCO(I)+1) 70,80,70
   70 IW=ISCO(I)
      ISCO(I)=ISCO(J)
      ISCO(J)=IW
      IW=ICOMP(I)
      ICOMP(I)=ICOMP(J)
      ICOMP(J)=IW
      GO TO 100
   80 ISCO(I)=ISCO(J)
      ICOMP(I)=ICOMP(J)
      ISCO(J)=-1
  100 IF(I-NCAS2) 110,60,110
  110 IEND=I
      I=I+1
      GO TO 10
   60 IEND=I
   62 CONTINUE
      WRITE(NWRITE,250) IEND
  250 FORMAT(//,10H THERE ARE,I4,19H DIFFERENT PROFILES)
CY  350 FORMAT(1X,3I5,5X,4I2)
C
C  FIND THE INVERSE FUNCTION OF ICOMP(.)
C  PUT IT IN ISCO(.) , THEN REPUT IT IN ICOMP(.)
      DO 45 I=1,IEND
       IARG=ICOMP(I)
       ISCO(IARG)=I
   45 CONTINUE
C  *** PROVISOIRE *****
C     WRITE(NWRITE,*) 'I   ICOMP    ICOMP-1     IPRF'
C     DO 46 I=1,NCAS2
C      WRITE(NWRITE,350) I,ICOMP(I),ISCO(I),(IPRF(J,I),J=1,INTERN)
C  46 CONTINUE
C  *******************
      DO 55 I=1,NCAS2
       ICOMP(I)=ISCO(I)
   55 CONTINUE
C
C  RESET THE ORIGINAL SCORES (BEFORE ORDERING)
      DO 65 I=1,NCAS2
C  PUT SCORE=-1 IF FREQ=0
       IF(IFREQ(I).EQ.0) GO TO 85
       IS=0
       DO 75 J=1,INTERN
          IS=IS+IPRF(J,I)
   75  CONTINUE
       ISCO(I)=IS
       GO TO 65
   85  ISCO(I)=-1
   65 CONTINUE
      RETURN
C
      END

      SUBROUTINE PRNTID (ICOMP, IFREQ, IPRF, ISCO, NV, NCAS2)
C
      PARAMETER (IDMAX=500)
      PARAMETER (IDLEN=10)
C
C  TO PRINT CASE ID
C
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
      COMMON/VARINT/INTERN
      COMMON/ZIHOUY/ID
      COMMON/KENID/YESID
      COMMON/PARZIH/IND,NN,INDEX,NONUL
      COMMON /WCHAR/ FMT,FMT1,FMT2,FMT3,FMT4,FMT5,DUMMY
C
      LOGICAL YESID
C
      CHARACTER*10 ID(IDMAX)
      CHARACTER FMT*46,FMT1*10,FMT2*3,FMT3*3,FMT4*2,FMT5*28
      CHARACTER*170 DUMMY(2)
C
      INTEGER*2 IND,NN,INDEX(IDMAX),NONUL(IDMAX)
      INTEGER*2 NV, NCAS2
      INTEGER*2 IFREQ(NCAS2),IPRF(NV,NCAS2),ICOMP(NCAS2),ISCO(NCAS2)
C
      INTEGER*2 I,J,K,NUMB1,NUMB2,IDPROG,IXX
C
C **********************************************************************
C
C  INITIALIZING VARIABLE FORMAT FOR PRINTING THE TABLE
C
      IF (INTERN.GT.20) GOTO 10
      FMT1='(1X,I3,2X,'
      WRITE (FMT2,'(I3)') INTERN
      FMT3='I2,'
      IXX=(20-INTERN)*2+1
      WRITE (FMT4,'(I2)') IXX
      FMT5='X,I3,2X,I4,2X,(T59,8(A,1X)))'
      FMT=FMT1//FMT2//FMT3//FMT4//FMT5
C
C **********************************************************************
C
  10  CONTINUE
      IF (YESID) THEN
          IF(INTERN .LE. 20) THEN
               WRITE (NWRITE,300)
          ELSE
               WRITE (NWRITE,301)
          ENDIF
      ELSE
          IF(INTERN .LE. 20) THEN
               WRITE (NWRITE,310)
          ELSE
               WRITE (NWRITE,311)
          ENDIF
      ENDIF
      NUMB1=1
      DO 100 J=1,NN
          I = NONUL(J)
          IDPROG = ICOMP(I)
          IFREQI = IFREQ(I)
          NUMB2 = IFREQI + NUMB1 - 1
          IF (INTERN .LE. 20 ) THEN
               WRITE(NWRITE,FMT) IDPROG,(IPRF(K,I),K=1,INTERN),
     $                 ISCO(I),IFREQ(I),(ID(INDEX(K)),K=NUMB1,NUMB2)
          ELSE
               WRITE(NWRITE,201) IDPROG,(IPRF(K,I),K=1,INTERN)
               WRITE(NWRITE,250) ISCO(I),IFREQ(I),
     $                            (ID(INDEX(K)),K=NUMB1,NUMB2)
          ENDIF
          NUMB1 = NUMB2 + 1
  100 CONTINUE
      RETURN
C
201   FORMAT(1X,I3,2X,(T7,60I2))
250   FORMAT(12X,'SCO = ',I3,5X,'FREQ = ',I4,5X,'CASES : ',
     $                                   (T50,8(A,1X)))
300   FORMAT(//,1X,3H ID,3X,7HPROFILE,33X,3HSCO,2X,
     $                      4HFREQ,3X,7HUSER ID,
     $                       /,2X,2H--,3X,7(1H-),
     $                         33X,3H---,2X,4H----,3X,7(1H-)  ,/)
301   FORMAT(//,1X,3H ID,3X,7HPROFILE /,2X,2H--,3X,7(1H-),/)
310   FORMAT(//,1X,3H ID,3X,7HPROFILE,33X,3HSCO,2X,
     $                   4HFREQ,3X,18HSERIAL CASE NUMBER,
     $                             /,2X,2H--,3X,7(1H-),
     $                        33X,3H---,2X,4H----,3X,18(1H-)  ,/)
311   FORMAT(//,1X,3H ID,3X,7HPROFILE  /,2X,2H--,3X,7(1H-),/)
C
      END

