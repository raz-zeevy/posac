    
      SUBROUTINE graphicsmode (graphOK)

      IMPLICIT NONE

      LOGICAL*2  graphOK, OK
      INTEGER*2  mode, TEMP, LL
      CHARACTER*1 CH
      CHARACTER*128 STRING
      CHARACTER*9 FNAME
      LOGICAL*2  first /.TRUE./
      SAVE       first, mode
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

C     get rid of any old CR-LF
      WRITE (*, '(1X)', advance="no")

	  graphOK = .FALSE.

      RETURN
      END

      SUBROUTINE textmode

      IMPLICIT NONE

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      RETURN
      END

      SUBROUTINE clrscrn

      IMPLICIT NONE

      RETURN
      END

      SUBROUTINE drawframe (X1, X2, Y1, Y2)

      IMPLICIT NONE

      REAL X1, X2, Y1, Y2
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      INTEGER*2        dummy, XM, YM, sty

      RETURN
      END

CC  NEWX - This function finds new x coordinates.

      INTEGER*2 FUNCTION newx ( xcoord )

      IMPLICIT NONE
      REAL*4    xcoord
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      newx  = 1
      RETURN
      END


CC  NEWY - This function finds new y coordinates.

      INTEGER*2 FUNCTION newy ( ycoord )

      IMPLICIT NONE
      REAL*4    ycoord
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      newy  = 1
      RETURN
      END

      SUBROUTINE drawline (X1, Y1, X2, Y2)

C         draw the line from (X1, Y1) to (X2, Y2)

      IMPLICIT NONE

      REAL*4 X1, Y1, X2, Y2

      INTEGER*2 newx, newy, dummy

      RETURN
      END

      SUBROUTINE drawcircle (X, Y, RADIUS)

C         draw the circle centred at (X, Y) with given radius

      IMPLICIT NONE

      REAL*4 X, Y, RADIUS

      INTEGER*2 newx, newy, dummy

      RETURN
      END

      SUBROUTINE drawarc (X, Y, RADIUS, X1, Y1, X2, Y2)

C         draw the arc of the circle centred at (X, Y) with given radius
C         counterclockwise from (X1, Y1) to (X2, Y2)

      IMPLICIT NONE

      REAL*4 X, Y, RADIUS, X1, Y1, X2, Y2

      INTEGER*2 newx, newy, dummy

      RETURN
      END

      SUBROUTINE putnum (K, X, Y)

C         put the number K at (x, y)

      IMPLICIT NONE

      INTEGER*2 K, L
      REAL X, Y
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN
      INTEGER*2 newx, newy

      RETURN
      END


      SUBROUTINE putgtext (text, X, Y, horalign, vertalign)

      IMPLICIT NONE

      CHARACTER*(*) text
      REAL X, Y
      INTEGER*2 horalign, vertalign
C
C         horalign is 0 for left align, 1 for centre, 2 for right align
C         vertalign is 0 for bottom align, 1 for centre, 2 for top align
C
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN
      INTEGER*2 newx, newy
      INTEGER*2 xdiff, ydiff

      RETURN
      END


      SUBROUTINE puttext (text, column, row)

      IMPLICIT NONE

      INTEGER*2 row, column
      CHARACTER*(*) text

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

C      call settextposition (row, column, rc)
C      call outtext (text)
C
      RETURN
      END


      SUBROUTINE endgraph

      IMPLICIT NONE


C      call settextposition (25, 1, rc)

      RETURN
      END


      SUBROUTINE printgraph (XMAX, YMAX)

      IMPLICIT NONE

      INTEGER*2 XMAX, YMAX

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      IF (GRAPHICS .EQ. 0)  RETURN

      IF (RESLN .EQ. 0) THEN
          CALL printgraph1 (XMAX, YMAX)
      ELSE
          CALL printgraph2 (XMAX, YMAX)
      END IF
      RETURN
      END


      SUBROUTINE printgraph1 (XMAX, YMAX)

      IMPLICIT NONE
      INTEGER*2 XMAX, YMAX

      RETURN
      END


      SUBROUTINE printgraph2 (XMAX, YMAX)

      IMPLICIT NONE
      INTEGER*2 XMAX, YMAX

      RETURN
      END


      SUBROUTINE printlaser (XMAX, YMAX)

      IMPLICIT NONE
      INTEGER*2 XMAX, YMAX


      RETURN
      END


      SUBROUTINE Conv2PCX (FN, XMAX, YMAX)

      IMPLICIT NONE

      INTEGER*2 XMAX, YMAX
      CHARACTER*(*) FN

      INTEGER*2 MAXCOLS
      PARAMETER (MAXCOLS = 720)

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      IF (GRAPHICS .EQ. 0)  RETURN

      RETURN
      END


      BLOCK DATA

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      DATA graphics /0/
      END


C      SUBROUTINE tryout
C
C      IMPLICIT NONE
C      INCLUDE  'FGRAPH.FD'
C
C      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
C     1           charx, chary, resln
C      REAL*4 xmult, ymult
C      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
C     1                  XMULT, YMULT, CHARX, CHARY, RESLN
C      INTEGER*2 newx, newy, dummy
C      RECORD /xycoord/ xy
C
C      CALL moveto (newx (20.0), newy (20.0), xy)
C      dummy = lineto (newx (60.0), newy (60.0))
C      CALL moveto (newx (60.0) - charx/2, newy (60.0) - chary/2, xy)
C      CALL outgtext ('IIIIIII')
C      RETURN
C      END

