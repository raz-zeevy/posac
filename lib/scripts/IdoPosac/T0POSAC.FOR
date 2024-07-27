      SUBROUTINE ENLA(A,FACT,N,M)
C
      INTEGER*2 N,M
      REAL      A(N,M)
C
      INTEGER*2 K,IM
C
      DO 10 K=1,N
          DO 11 IM=1,M
               A(K,IM)=FACT*A(K,IM)
   11     CONTINUE
   10 CONTINUE
C
      RETURN
C
      END

      SUBROUTINE STORE (A,B,N,M)
C
C  THIS SUB. STORES MATRIX B IN AREA A
C
      INTEGER*2 N,M
      REAL      A(N,M),B(N,M)
C
      INTEGER*2 I,J
C
      DO 10 I=1,N
          DO 20 J=1,M
               A(I,J)=B(I,J)
   20     CONTINUE
   10 CONTINUE
C
      RETURN
C
      END
