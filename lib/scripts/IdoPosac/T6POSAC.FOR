

      SUBROUTINE ITER

INCLUDE 'MPARMLIN'

C  THIS SUB. PERFORMS ALL THE WORK FOR ONE ITERATION
C
C     COMMON X(1)

INCLUDE 'MCOMNBLK'

      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
C      COMMON/DIM/M,N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12
      COMMON/AA/NV,NCAS,NXT,MAP,M
      COMMON/CC/ISMN,ISMX,IEND
      COMMON/XMN/STEP
      COMMON/VALMU/XMUT
      COMMON/ABTOL/A0,B0,TOL,EXTRA
C
      INTEGER*2 NV,NCAS,NXT,MAP,M,ISMN,ISMX,IEND
C      INTEGER*2 IER
C
C  DETERMINATION OF THE MATRIX DERIVATIVE DMU
C
      CALL FINDER(XN7,XN7,XN8,XN3,XN10,IEND)
C
C  FINDING THE OPTIMUM STEP
      A1=A0
      B1=B0
      FA = FUNCT (A1)
      FB = FUNCT (B1)
 60   CONTINUE
      C1 = (A1+B1)*0.5
      FC = FUNCT (C1)
 80   CONTINUE
      IF (FC .GT. FA) THEN
          B1 = C1
          FB = FC
          GOTO 60
      END IF
      IF (FC .EQ. FA .AND. FB .EQ. FA) THEN
          STEP = B1
          GOTO 70
      END IF
      IF (FC .GT. FB) THEN
          A1 = C1
          FA = FC
          C1 = B1
          FC = FB
          B1 = B1 + EXTRA
          FB = FUNCT (B1)
          GOTO 80
      END IF
C   10 CONTINUE
C      A=A1
C      B=B1
C      WRITE (*,*) 'IN ITER ', A1, B1, TOL
C      WRITE (NWRITE,*) 'IN ITER ', A1, B1, TOL
C      CALL ZXGSN(A,B,TOL,STEP,IER)
C      WRITE (NWRITE,*) 'DOING ITER ', A, B, TOL, STEP, IER
      CALL BRENT (A1,C1,B1,FC,TOL,STEP)
C      WRITE (NWRITE,*) 'DOING ITER ', A1, B1, TOL, STEP
C
C      IF(STEP.NE.B1) GO TO 20
C  IF STEP=B1 THIS MEANS THAT THE BOUND B HAS TO BE ENLARGED
C      A1=B1
C      B1=B1+EXTRA
C      GO TO 10
C   20 CONTINUE
C
C  AT NEXT ITERATION THE SOLUTION IS
C  X2=X1-STEP*DMUT/DX
C
 70   CONTINUE
C      WRITE (NWRITE,*) 'DONE ITER ', A, B, TOL, STEP, IER
C      WRITE (NWRITE,*) 'DONE ITER ', A1, B1, TOL, STEP
      CALL OPRMAT(XN8,-STEP,XN10,XN9,IEND,M)
C
      RETURN
C
      END

      SUBROUTINE FINDER (ALFA, WEIGHT, X, IFREQ, DMU, N)

C  THIS SUB. FINDS THE MATRIX DERIVATIVE DMU

      INTEGER*2 N,IFREQ(N)
      REAL      ALFA(N,N),WEIGHT(N,N),X(N,2),DMU(N,2)
C
      INTEGER*2 N1,IH,L,IAL
      INTEGER*4 IFH
C
C **********************************************************************
C
      N1=N-1
      DO 10 IH=2,N1
         XH=X(IH,1)
         YH=X(IH,2)
         IFH=IFREQ(IH)
         DU1X=0.
         DU1Y=0.
         DU2X=0.
         DU2Y=0.
         DVX=0.
         DVY=0.
         DO 20 L=1,N
            XHL=XH-X(L,1)
            YHL=YH-X(L,2)
            XHL2=XHL*XHL
            YHL2=YHL*YHL
            XYHL=XHL*YHL
            ABXHL=ABS(XHL)
            ABYHL=ABS(YHL)
            ABXYHL=ABS(XYHL)
            IF(L.GE.IH) GO TO 15
            IAL=-ALFA(L,IH)
            WHT=WEIGHT(IH,L)
            GO TO 16
   15       CONTINUE
            IAL=ALFA(IH,L)
            WHT=WEIGHT(L,IH)
   16       CONTINUE
            FWHL=IFH*IFREQ(L)*WHT
            FACT1=FWHL*IAL
            DVX=DVX+FWHL*XHL*YHL2
            DVY=DVY+FWHL*XHL2*YHL
            IF(IAL.EQ.0) GO TO 30
            DU2X=DU2X+FACT1*(ABXHL*YHL2+XYHL*ABYHL)
            DU2Y=DU2Y+FACT1*(XYHL*ABXHL+ABYHL*XHL2)
            GO TO 20
   30       CONTINUE
            FACT2=FWHL*ABXYHL
            DU1X=DU1X-FACT2*YHL
            DU1Y=DU1Y-FACT2*XHL
   20    CONTINUE
         DU1X=4.*DU1X
         DU1Y=4.*DU1Y
         DU2X=2.*DU2X
         DU2Y=2.*DU2Y
         DVX=4.*DVX
         DVY=4.*DVY
         DMU(IH,1)=DVX-DU1X-DU2X
         DMU(IH,2)=DVY-DU1Y-DU2Y
C
   10 CONTINUE
C
      RETURN
      END

      SUBROUTINE BRENT (AX, CX, BX, FC, TOL, XMIN)

      PARAMETER (ITMAX = 100)
      PARAMETER (CGOLD = 0.381966011251)
      PARAMETER (ZEPS = 1.0E-10)
      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR

C
C     AX is start point, BX is end point; AX < BX;
C     CX is in between, with F (CX) < F (AX);  F (CX) < F (BX).
C
C     Source: W.H. Press et al, p.285;

      A = AX
      B = BX
      V = CX
      W = V
      X = V
      E = 0
      FX = FC
      FV = FX
      FW = FX
      DO 11 ITER = 1,ITMAX
          XM = 0.5 * (A + B)
          TOL1 = TOL * ABS (X) + ZEPS
          TOL2 = 2 * TOL1
          IF (ABS (X-XM).LE.(TOL2-.5*(B-A))) GOTO 3
          IF (ABS (E) .GT. TOL1) THEN
               R = (X - W) * (FX - FV)
               Q = (X - V) * (FX - FW)
               P = (X - V) * Q - (X - W) * R
               Q = 2 * (Q - R)
               IF (Q .GT. 0) P = -P
               Q = ABS (Q)
               ETEMP = E
               E = D
               IF (ABS (P) .GE. ABS (.5*Q*ETEMP) .OR. P .LE. Q*(A-X)
     $              .OR. P .GE. Q*(B-X) ) GOTO 1
               D = P / Q
               U = X + D
               IF (U-A .LT. TOL2 .OR. B-U .LT. TOL2)
     $                    D = SIGN (TOL1, XM - X)
               GOTO 2
          END IF
 1        IF (X .GE. XM) THEN
               E = A - X
          ELSE
               E = B - X
          END IF
          D = CGOLD * E
 2        IF (ABS (D) .GE. TOL1) THEN
               U = X + D
          ELSE
               U = X + SIGN (TOL1, D)
          END IF
          FU = FUNCT (U)
C      write (nwrite,*) 'brent pt, val ', U, FU, tol1
          IF (FU .LE. FX) THEN
               IF (U .GE. X) THEN
                    A = X
               ELSE
                    B = X
               END IF
               V = W
               FV = FW
               W = X
               FW = FX
               X = U
               FX = FU
          ELSE
               IF (U .LT. X) THEN
                    A = U
               ELSE
                    B = U
               END IF
               IF (FU .LE. FW .OR. W .EQ. X) THEN
                    V = W
                    FV = FW
                    W = U
                    FW = FU
               ELSE IF (FU .LE. FV .OR. V .EQ. X .OR. V .EQ. W) THEN
                    V = U
                    FV = FU
               END IF
          END IF
 11   CONTINUE
      WRITE (*,*) '*** WARNING *** No convergence in BRENT routine.'
      WRITE(NWRITE,*)'*** WARNING *** No convergence in BRENT routine.'
 3    XMIN = X
      RETURN
      END


C      SUBROUTINE ZXGSN (A,B,TOL,XMIN,IER)
C
C      COMMON/IO/NTAPE,NREAD,NWRITE,NSCR
C
C  SPECIFICATIONS FOR ARGUMENTS
C      INTEGER*2 IER
C      REAL A,B,TOL,XMIN
C  SPECIFICATIONS FOR LOCAL VARIABLES
C      REAL C,FA,FB,H,V1,V2,FV1,FV2
C
C **********************************************************************
C
C  FIRST EXECUTABLE STATEMENT
C
C      XMIN=A
C      IER=129
C
C  B MUST BE GREATER THAN A
C
C      IF(B.LE.A) GO TO 9000
C      IER=130
C
C  TOL MUST BE SMALLER THAN THE
C   INITIAL INTERVAL
C
C      IF(TOL.GE.(B-A)) GO TO 9000
C      IER=0
C
C  COMPUTE THE FIBONACCI CONSTANT
C
C      C=(3.0-SQRT(5.0))/2.0
C
C  COMPUTE THE INITIAL STEP
C
C      H=C*(B-A)
C
C  COMPUTE THE NEW POINTS
C
C      V1=A+H
C      V2=B-H
C
C  MAKE THE INITIAL FUNCTION EVALUATIONS
C
C      FA=FUNCT(A)
C      FB=FUNCT(B)
C      FV1=FUNCT(V1)
C      FV2=FUNCT(V2)
C
C  EACH ITERATION BEGINS HERE
C
C    5 CONTINUE
C
C      WRITE (NWRITE,*) 'ZX POINTS', A, V1, V2, B
C      WRITE (NWRITE,*) 'ZX VALUES', FA, FV1, FV2, FB
C
C  HAS THE INTERVAL BECOME TOO SMALL
C
C      IF(A.GE.V1.OR.V1.GE.V2.OR.V2.GE.B) GO TO 40
C
C  FIND THE CURRENT MINIMUM
C
C      IF(FV1.GE.FV2) GO TO 10
C
C  V1 IS THE MINIMUM
C  CHECK TO SEE IF THE FUNCTION IS
C  NOT UNIMODAL
C
C      IF(FV2.GT.FB) GO TO 25
C
C  UPDATE THE INTERVAL
C   V2 BECOMES THE NEW B
C
C      B=V2
C
C  IS THE INTERVAL SUFFICIENTLY SMALL
C
C      IF(TOL.GE.(B-A)) GO TO 15
C
C  REDUCE THE INTERVAL FURTHER
C
C      FB=FV2
C      V2=V1
C      FV2=FV1
C      H=C*(B-A)
C      V1=A+H
C      FV1=FUNCT(V1)
C      GO TO 5
C
C  V2 IS THE MINIMUM
C  CHECK TO SEE IF THE FUNCTION IS
C    NOT UNIMODAL
C
C   10 IF(FV1.GT.FA) GO TO 30
C
C  UPDATE THE INTERVAL
C    V1 BECOMES THE NEW A
C
C      A=V1
C
C  IS THE INTERVAL SUFFICIENTLY SMALL
C
C      IF(TOL.GE.(B-A)) GO TO 20
C
C  REDUCE THE INTERVAL FURTHER
C
C      FA=FV1
C      V1=V2
C      FV1=FV2
C      H=C*(B-A)
C      V2=B-H
C      FV2=FUNCT(V2)
C      GO TO 5
C
C  CONVERGENCE OBTAINED. V1 OR A
C    IS THE MINIMUM
C
C   15 XMIN=V1
C      IF(FA.LT.FV1) XMIN=A
C      GO TO 9005
C
C  CONVERGENCE OBTAINED. V2 OR B
C    IS THE MINIMUM
C
C   20 XMIN=V2
C      IF(FB.LT.FV2) XMIN=B
C      GO TO 9005
C
C   FUNCTION IS NOT UNIMODAL. RETURN
C     THE NECESSARY PARAMETERS
C
C   25 XMIN=V2
C      A=V1
C   30 XMIN=V1
C      B=V2
C   35 IER=131
C
C**   GO TO 9000
C** CHANGED IN ORDER TO SUPPRESS GARBAGE ( JANUARY 1983)
C
C      GO TO 9005
C
C  THE INTERVAL HAS BECOME TOO SMALL
C
C   40 IER=132
C      XMIN=A
C      IF(FB.LT.FA) XMIN=B
C
C 9000 CONTINUE
C      WRITE(NWRITE,100) IER
C 9005 RETURN
C
C  100 FORMAT(5X,16H**ERROR**   IER=,I3)
C
C      END

      FUNCTION FUNCT (STEP)

INCLUDE 'MPARMLIN'

C  THIS FUNCTION IS AN ARGUMENT FOR
C  THE CALLING SEQUENCE ZXGSN
C
C     COMMON X(1)

INCLUDE 'MCOMNBLK'

C      COMMON/DIM/M,N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12
      COMMON/AA/NV,NCAS,NXT,MAP,M
      COMMON/CC/ISMN,ISMX,IEND
C
      INTEGER*2 NV,NCAS,NXT,MAP,M,ISMN,ISMX,IEND
C
C **********************************************************************
C
      CALL OPRMAT(XN8,-STEP,XN10,XN9,IEND,M)
      CALL UVMU(XN7,XN7,XN9,XN3,IEND,UT1,VT1,XMUT1)
      FUNCT=XMUT1
C
      RETURN
C
      END

      SUBROUTINE OPRMAT (A,UB,B,C,N,M)

C  THIS SUB. PERFORMS THE FOLLOWING OPERATION
C    C=A+UB*B FOR I=2,...,N-1 AND J=1,...,M
C  WHERE A B AND C ARE N*M MATRICES, UB IS A SCALAR

      INTEGER*2 N,M
      REAL      A(N,M),B(N,M),C(N,M)
C
      INTEGER*2 N1,I,J
C
C **********************************************************************
C
      N1=N-1
C
      DO 10 I=2,N1
          DO 20 J=1,M
               C(I,J)=A(I,J)+UB*B(I,J)
   20     CONTINUE
   10 CONTINUE
C
      RETURN
      END

      SUBROUTINE UVMU (ALFA, WEIGHT,
     $                 X, IFREQ, N, U, V, XMU)
C
      INTEGER*2 N,IFREQ(N)
      REAL      ALFA(N,N),WEIGHT(N,N),X(N,2)
C
      INTEGER*2 N1,K,L1,L,IAL
      INTEGER*4 IFK
      DOUBLE PRECISION U1, U2, VV, FACT, XXK, YYK, XKL, YKL,
     $                 VAXKL, VAYKL, XKL2, YKL2
C
      U1=0.
      U2=0.
      VV=0.
      N1=N-1
      DO 10 K=1,N1
         L1=K+1
         XXK=X(K,1)
         YYK=X(K,2)
         IFK=IFREQ(K)
         DO 11 L=L1,N
            XKL=XXK-X(L,1)
            YKL=YYK-X(L,2)
            VAXKL=XKL*ABS(XKL)
            VAYKL=YKL*ABS(YKL)
            XKL2=XKL*XKL
            YKL2=YKL*YKL
            FACT=IFK*IFREQ(L)
            FACT = FACT*WEIGHT(L,K)
            VV=VV+FACT*XKL2*YKL2
            IAL=ALFA(K,L)
            IF(IAL.EQ.0) GO TO 20
            U2=U2+FACT*(VAXKL*YKL2+VAYKL*XKL2)
            GO TO 11
   20       U1=U1-FACT*VAXKL*VAYKL
   11    CONTINUE
   10 CONTINUE
      U=2.*U1+U2
      V=2.*VV
      XMU=2.*(VV-U1)-U2
C
      RETURN
C
      END

      SUBROUTINE TRANS3(X2,ICOMP,N,M)

C  THIS SUB. FINDS THE TWO PERMUTATIONS ON X AND Y AND
C  TRANSFORMS THE SOLUTION X2 ACCORDING TO THESE PERMUTATIONS

      INTEGER*2 N,M,ICOMP(N)
      REAL      X2(N,M)
C
      INTEGER*2 N1,IM,K,ICK,I
C
      N1=N-1
      DO 10 IM=1,M
         DO 20 K=2,N1
            VALMAX=X2(K,IM)
            ICK=K
            DO 30 I=2,N1
               VALX=X2(I,IM)
               IF(VALX.LT.-100.) GO TO 30
               VALMAX=AMAX1(VALMAX,VALX)
               IF(VALMAX.EQ.VALX) ICK=I
   30       CONTINUE
            ICOMP(K)=ICK
            X2(ICK,IM)=-200.
   20    CONTINUE
         DO 40 K=2,N1
            ICK=ICOMP(K)
            X2(ICK,IM)=(N-K)/FLOAT(N1)
   40    CONTINUE
   10 CONTINUE
C
      RETURN
C
      END

      SUBROUTINE NORMU (ALFA, X, IFREQ, N, U, V, XMU)

C  COMPUTES THE NORMALISED MU FOR THE SOLUTION X

      INTEGER*2 N,IFREQ(N)
      REAL      ALFA(N,N), X(N,2)
C
      INTEGER*4 IFK, IFKL
C
C
      U1=0.
      U2=0.
      V=0.
      N1=N-1
      DO 10 K=1,N1
         L1=K+1
         XXK=X(K,1)
         YYK=X(K,2)
         IFK=IFREQ(K)
         DO 11 L=L1,N
            XKL=XXK-X(L,1)
            YKL=YYK-X(L,2)
            SXKL=SIGN(1.,XKL)
            SYKL=SIGN(1.,YKL)
            IFKL=IFK*IFREQ(L)
            V=V+IFKL
            IAL=ALFA(K,L)
            IF(IAL.EQ.0) GO TO 20
            U2=U2+IFKL*(SXKL+SYKL)
            GO TO 11
   20       U1=U1-IFKL*SXKL*SYKL
   11    CONTINUE
   10 CONTINUE
      U=2.*U1+U2
      V=2.*V
      XMU=U/V
C
      RETURN
C
      END


