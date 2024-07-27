      INCLUDE  'FGRAPH.FI'

      SUBROUTINE graphicsmode (graphOK)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      LOGICAL*2  graphOK, OK
      INTEGER*2  mode, TEMP, LL
      CHARACTER*1 CH
      CHARACTER*128 STRING
      CHARACTER*9 FNAME
      LOGICAL*2  first /.TRUE./
      SAVE       first, mode
      RECORD /videoconfig/ myscreen
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

C     get rid of any old CR-LF
      WRITE (*, '(1X\)')

      IF (graphics .NE. 0) THEN
          CALL clrscrn
          graphOK = .TRUE.
          RETURN
      END IF

C     Find graphics mode.
      
      IF (first) THEN
          resln = 0
          first = .FALSE.
          CALL getvideoconfig (myscreen)
          tmode = myscreen.mode
          SELECT CASE ( myscreen.adapter )
             CASE( $MDPA )
                mode = $TEXTBW80
                 write (*,*) ' *** NO GRAPHICS CARD DETECTED ***'
                 write (*,*) ' NOTE: If you have a hercules,',
     1                       ' you must run MSHERC.COM first.'
             CASE( $CGA )
                mode = $MAXRESMODE
C                mode = $HRESBW
                colour = 1
                resln = 0
             CASE( $OCGA )
                mode = $MAXRESMODE
C                mode = $HRESBW
                colour = 1
C                mode = $ORESCOLOR
C                colour = 7
                resln = 1
             CASE( $EGA, $OEGA )
                mode = $MAXRESMODE
C                mode = $HRESBW
                colour = 7
                resln = 1
C                IF( myscreen.monitor .EQ. $MONO ) THEN
C                    mode = $ERESNOCOLOR
C                    colour = 1
C                ELSE
C                    mode = $ERESCOLOR
C                    colour = 7
C                END IF
             CASE( $VGA, $OVGA, $MCGA )
                mode = $MAXRESMODE
C                mode = $HRESBW
                colour = 7
                resln = 1
C                mode = $VRES2COLOR
             CASE( $HGC )
                mode = $HERCMONO
                colour = 1
                resln = 0
             CASE DEFAULT
                WRITE (*,*) 'ERROR:  cannot recognise graphics mode'
                mode = $TEXTBW80
          END SELECT
          IF (resln .EQ. 0) THEN
              FNAME = 'COURB.FON'
          ELSE
              FNAME = 'TMSRB.FON'
          END IF
          OK = (registerfonts (FNAME) .GT. 0)
          IF (.NOT. OK) THEN
               CALL FONTPATH (STRING, LL)
               IF (LL .GT. 0) THEN
                    CH = STRING (LL:LL)
                    IF (CH .NE. '\' .AND. CH .NE. ':') THEN
                         LL = LL + 1
                         STRING (LL:LL) = '\'
                    END IF
                    STRING (LL+1:LL+9) = FNAME
                    LL = LL + 9
                    OK = (registerfonts (STRING(1:LL)) .GT. 0)
               END IF
          END IF
          IF (.NOT. OK) THEN
               WRITE (*,*) ' ERROR: cannot register font file'
               mode = $TEXTBW80
          ELSE IF (resln .EQ. 0) THEN
               IF (setfont ('rfh10w8') .NE. 0) THEN
                    WRITE (*,*) ' ERROR: cannot set font'
                    mode = $TEXTBW80
               ELSE
                    charx = 8
                    chary = 10
               END IF
          ELSE
               IF (setfont ('rph15w8') .NE. 0) THEN
                    WRITE (*,*) ' ERROR: cannot set font'
                    mode = $TEXTBW80
               ELSE
                    charx = 8
                    chary = 15
               END IF
          END IF
      END IF
      IF (mode .NE. $TEXTBW80) THEN
          graphics = setvideomode (mode)
          IF( graphics .EQ. 0 ) THEN
               WRITE (*,*)  ' ERROR:  cannot set graphics mode'
               mode = $TEXTBW80
               graphOK = .FALSE.
          ELSE
C
C     Determine the minimum and maximum dimensions.
C
               graphOK = .TRUE.
               CALL getvideoconfig( myscreen )
               maxx = myscreen.numxpixels - 1
               maxy = myscreen.numypixels - 1
               mode = myscreen.mode
               IF (myscreen.numcolors .GT. 7) THEN
                    colour = 7
               ELSE
                    colour = 1
               END IF
               temp = setcolor (colour)

               IF (mode .EQ. $HERCMONO) THEN
                    graphics = 2
               ELSE
                    graphics = 1
C               ELSE
C                    WRITE (*,*) ' CONSISTENCY ERROR IN GRAPHICS'
C                    graphOK = .FALSE.
               END IF
          END IF
      ELSE
          graphics = 0
          graphOK = .FALSE.
      END IF

      RETURN
      END

      SUBROUTINE textmode

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN
      RECORD /rccoord/ rc

      IF (graphics .NE. 0) THEN
          graphics = setvideomode (tmode)
C         graphics = setvideomode( $DEFAULTMODE )
          graphics = 0
      END IF
      WRITE (*, '(1X\)')
      CALL clearscreen ($GCLEARSCREEN)
      CALL settextposition (1, 1, rc)
      RETURN
      END

      SUBROUTINE clrscrn

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      CALL CLEARSCREEN ($GCLEARSCREEN)
      RETURN
      END

      SUBROUTINE drawframe (X1, X2, Y1, Y2)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      REAL X1, X2, Y1, Y2
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      RECORD /xycoord/ xy
      INTEGER*2        dummy, XM, YM, sty

C
C     Draw the box.
C
      IF (graphics .EQ. 2) THEN
          XM = 9
          YM = 14
      ELSE
          XM = 8
          YM = (maxy + 1) / 25
      END IF
      sty = YM * Y1
      call setvieworg (XM * X1, sty, xy)
      topx = XM * (X2 - X1 + 1)
      topy = YM * (Y2 - Y1 + 1)
      IF (topy + sty .GT. maxy) topy = maxy - sty
      dummy = rectangle( $GBORDER, 0, 0, topx, topy )
      xmult = topx / 100.0
      ymult = topy / 100.0

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

      newx  = xcoord * xmult + 0.5
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

      newy  = topy - (ycoord * ymult + 0.5)
      RETURN
      END

      SUBROUTINE drawline (X1, Y1, X2, Y2)

C         draw the line from (X1, Y1) to (X2, Y2)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      REAL*4 X1, Y1, X2, Y2

      INTEGER*2 newx, newy, dummy
      RECORD /xycoord/ xy

      call moveto (newx (X1), newy (Y1), xy)
      dummy = lineto (newx (X2), newy (Y2))
      RETURN
      END

      SUBROUTINE drawcircle (X, Y, RADIUS)

C         draw the circle centred at (X, Y) with given radius

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      REAL*4 X, Y, RADIUS

      INTEGER*2 newx, newy, dummy
      dummy = ellipse ($GBORDER, newx (X - RADIUS), newy (Y - RADIUS),
     1                 newx (X + RADIUS), newy (Y + RADIUS))

      RETURN
      END

      SUBROUTINE drawarc (X, Y, RADIUS, X1, Y1, X2, Y2)

C         draw the arc of the circle centred at (X, Y) with given radius
C         counterclockwise from (X1, Y1) to (X2, Y2)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      REAL*4 X, Y, RADIUS, X1, Y1, X2, Y2

      INTEGER*2 newx, newy, dummy
      dummy = arc (newx (X - RADIUS), newy (Y - RADIUS),
     1             newx (X + RADIUS), newy (Y + RADIUS),
     2             newx (X1), newy (Y1), newx (X2), newy (Y2))

      RETURN
      END

      SUBROUTINE putnum (K, X, Y)

C         put the number K at (x, y)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      INTEGER*2 K, L
      REAL X, Y
      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN
      INTEGER*2 newx, newy
      RECORD /xycoord/ xy

      IF (K .LT. 10) THEN
          CALL moveto (newx (X) - charx/2, newy (Y) - chary/2, xy)
          CALL outgtext (CHAR (48 + K))
      ELSE
          CALL moveto (newx (X) - charx, newy (Y) - chary/2, xy)
          L = K / 10
          CALL outgtext (CHAR (48 + L))
          CALL outgtext (CHAR (48 + K - 10 * L))
      END IF
      RETURN
      END


      SUBROUTINE putgtext (text, X, Y, horalign, vertalign)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

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
      RECORD /xycoord/ xy
      INTEGER*2 xdiff, ydiff

      IF (horalign .EQ. 0) THEN
          xdiff = 0
      ELSE IF (horalign .EQ. 1) THEN
          xdiff = - getgtextextent (text) / 2
      ELSE IF (horalign .EQ. 2) THEN
          xdiff = - getgtextextent (text)
      ELSE
          CALL puttext ('BAD VALUE for horizontal alignment',
     1                   INT2(1), INT2(25))
          STOP
      ENDIF

      IF (vertalign .EQ. 0) THEN
          ydiff = - chary
      ELSE IF (vertalign .EQ. 1) THEN
          ydiff = - chary / 2
      ELSE IF (vertalign .EQ. 2) THEN
          ydiff = 0
      ELSE
          CALL puttext ('BAD VALUE for vertical alignment',
     1                   INT2(1), INT2(25))
          STOP
      ENDIF

      CALL moveto (newx (X) + xdiff, newy (Y) + ydiff, xy)
      CALL outgtext (text)
C
      RETURN
      END


      SUBROUTINE puttext (text, column, row)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      INTEGER*2 row, column
      CHARACTER*(*) text

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN
      RECORD /rccoord/ rc

      call settextposition (row, column, rc)
      call outtext (text)
C
      RETURN
      END


      SUBROUTINE endgraph

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      RECORD /rccoord/ rc

      call settextposition (25, 1, rc)

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
      INCLUDE  'FGRAPH.FD'

      INTEGER*2 XMAX, YMAX

      INTEGER*2 MAXCOLS
      PARAMETER (MAXCOLS = 720)

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      CHARACTER*1 PRDATA (MAXCOLS)
      CHARACTER*4 HEAD1, HEAD2
      INTEGER*2 PIN (8), THISPIN, PRNOUT, X, Y
      PARAMETER (PRNOUT = 22)
      INTEGER*2 NCOLS, NROWS,  NITER,  COL,  ROW,  J, K, BKGRD
      RECORD /xycoord/ xy
      DATA PIN /128, 64, 32, 16, 8, 4, 2, 1/

      IF (GRAPHICS .EQ. 0)  RETURN

      CALL setvieworg (0, 0, xy)
      HEAD1 (1:1) = CHAR (27)
      HEAD1 (2:2) = 'L'
      HEAD2 (1:1) = CHAR (13)
      HEAD2 (2:2) = CHAR (27)
      HEAD2 (3:3) = 'J'
      HEAD2 (4:4) = CHAR (24)

      NCOLS = MAXX + 1
      IF (NCOLS .GT. XMAX)  NCOLS = XMAX
      IF (NCOLS .GT. MAXCOLS) THEN
           WRITE (*,*) ' ERROR: Too many columns in print_screen.'
           RETURN
      END IF

      NROWS = MAXY + 1
      IF (NROWS .GT. YMAX)  NROWS = YMAX
      BKGRD = getbkcolor ()
      NITER = (NROWS + 7) / 8
      HEAD1 (3:3) = CHAR (IAND (NCOLS, 255))
      HEAD1 (4:4) = CHAR (NCOLS / 256)
      ROW = 0

      CALL SET_PRN_BINARY
      OPEN (UNIT = PRNOUT, FILE = 'PRN', ACCESS = 'SEQUENTIAL',
     1      FORM = 'BINARY', MODE = 'WRITE', ERR = 800)

      DO 60 K = 1, NITER
          DO 20 COL = 1, NCOLS
              PRDATA (COL) = CHAR (0)
 20       CONTINUE
          DO 40 J = 1, 8
              THISPIN = PIN (J)
              DO 30 COL = 1, NCOLS
                 IF (getpixel (INT2(COL-1), ROW) .NE. BKGRD)
     1             PRDATA (COL) = CHAR (ICHAR (PRDATA (COL)) + THISPIN)
 30           CONTINUE
              ROW = ROW + 1
              IF (ROW .EQ. NROWS)  GOTO 50
 40       CONTINUE
 50       CONTINUE
          WRITE (PRNOUT, ERR = 800)  HEAD1
          WRITE (PRNOUT, ERR = 800)  (PRDATA (J), J=1,NCOLS)
          WRITE (PRNOUT, ERR = 800)  HEAD2
 60   CONTINUE

      WRITE (PRNOUT, ERR = 800)  CHAR (12)
      CLOSE (UNIT = PRNOUT, ERR = 800)
      GOTO 100

 800  CONTINUE
      CALL puttext ('*** ERROR IN PRINTING ***', INT2 (1), INT2 (25))
 100  CONTINUE
      X = xy.xcoord
      Y = xy.ycoord
      CALL setvieworg (X, Y, xy)
      CALL RESET_PRN

      RETURN
      END


      SUBROUTINE printgraph2 (XMAX, YMAX)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      INTEGER*2 XMAX, YMAX

      INTEGER*2 MAXCOLS
      PARAMETER (MAXCOLS = 720)

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      CHARACTER*1 PRDATA (MAXCOLS, 2)
      CHARACTER*4 HEAD1, HEAD2, HEAD3
      INTEGER*2 PIN (8), THISPIN, PRNOUT, X, Y
      PARAMETER (PRNOUT = 22)
      INTEGER*2 NCOLS, NROWS,  NITER,  COL,  ROW,  J, K, L, BKGRD
      RECORD /xycoord/ xy
      DATA PIN /128, 64, 32, 16, 8, 4, 2, 1/

      IF (GRAPHICS .EQ. 0)  RETURN

      CALL setvieworg (0, 0, xy)
      HEAD1 (1:1) = CHAR (27)
      HEAD1 (2:2) = 'L'
      HEAD2 (1:1) = CHAR (13)
      HEAD2 (2:2) = CHAR (27)
      HEAD2 (3:3) = 'J'
      HEAD2 (4:4) = CHAR (1)
      HEAD3 (1:1) = CHAR (13)
      HEAD3 (2:2) = CHAR (27)
      HEAD3 (3:3) = 'J'
      HEAD3 (4:4) = CHAR (23)

      NCOLS = MAXX + 1
      IF (NCOLS .GT. XMAX)  NCOLS = XMAX
      IF (NCOLS .GT. MAXCOLS) THEN
           WRITE (*,*) ' ERROR: Too many columns in print_screen.'
           RETURN
      END IF

      NROWS = MAXY + 1
      IF (NROWS .GT. YMAX)  NROWS = YMAX
      BKGRD = getbkcolor ()
      NITER = (NROWS + 15) / 16
      HEAD1 (3:3) = CHAR (IAND (NCOLS, 255))
      HEAD1 (4:4) = CHAR (NCOLS / 256)
      ROW = 0

      CALL SET_PRN_BINARY
      OPEN (UNIT = PRNOUT, FILE = 'PRN', ACCESS = 'SEQUENTIAL',
     1      FORM = 'BINARY', MODE = 'WRITE', ERR = 800)

      DO 60 K = 1, NITER
          DO 20 COL = 1, NCOLS
              PRDATA (COL, 1) = CHAR (0)
              PRDATA (COL, 2) = CHAR (0)
 20       CONTINUE
          DO 40 J = 1, 8
              THISPIN = PIN (J)
              DO 35 L = 1, 2
                 DO 30 COL = 1, NCOLS
                    IF (getpixel (INT2(COL-1), ROW) .NE. BKGRD)
     1                 PRDATA (COL, L) =
     2                     CHAR (ICHAR (PRDATA (COL, L)) + THISPIN)
 30              CONTINUE
                 ROW = ROW + 1
                 IF (ROW .EQ. NROWS)  GOTO 50
 35           CONTINUE
 40       CONTINUE
 50       CONTINUE
          WRITE (PRNOUT, ERR = 800)  HEAD1
          WRITE (PRNOUT, ERR = 800)  (PRDATA (J, 1), J=1,NCOLS)
          WRITE (PRNOUT, ERR = 800)  HEAD2
          WRITE (PRNOUT, ERR = 800)  HEAD1
          WRITE (PRNOUT, ERR = 800)  (PRDATA (J, 2), J=1,NCOLS)
          WRITE (PRNOUT, ERR = 800)  HEAD3
 60   CONTINUE

      WRITE (PRNOUT, ERR = 800)  CHAR (12)
      CLOSE (UNIT = PRNOUT, ERR = 800)
      GOTO 100

 800  CONTINUE
      CALL puttext ('*** ERROR IN PRINTING ***', INT2 (1), INT2 (25))
 100  CONTINUE
      X = xy.xcoord
      Y = xy.ycoord
      CALL setvieworg (X, Y, xy)
      CALL RESET_PRN

      RETURN
      END


      SUBROUTINE printlaser (XMAX, YMAX)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      INTEGER*2 XMAX, YMAX

      INTEGER*2 MAXCOLS, MAXITER
      PARAMETER (MAXCOLS = 720)
      PARAMETER (MAXITER = (MAXCOLS + 7)/8)

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      CHARACTER*1 PRDATA (MAXITER)
      CHARACTER*13 HEAD1
      INTEGER*2 PIN (8), PRNOUT, X, Y
      PARAMETER (PRNOUT = 22)
      INTEGER*2 NCOLS, NROWS, NITER, COL, ROW, J, K, L, BKGRD
      RECORD /xycoord/ xy
      DATA PIN /128, 64, 32, 16, 8, 4, 2, 1/

      IF (GRAPHICS .EQ. 0)  RETURN

      CALL setvieworg (0, 0, xy)
      HEAD1 (1:1) = CHAR (27)
      HEAD1 (2:3) = '*r'
      HEAD1 (7:7) = 't'
      HEAD1 (11:13) = 's0A'

      NCOLS = MAXX + 1
      IF (NCOLS .GT. XMAX)  NCOLS = XMAX
      IF (NCOLS .GT. MAXCOLS) THEN
           WRITE (*,*) ' ERROR: Too many columns in print_screen.'
           RETURN
      END IF

      NROWS = MAXY + 1
      IF (NROWS .GT. YMAX)  NROWS = YMAX
      IF (RESLN .EQ. 0) THEN
          WRITE (HEAD1 (4:6), '(I3.3)') NROWS+NROWS
      ELSE
          WRITE (HEAD1 (4:6), '(I3.3)') NROWS
      END IF
      WRITE (HEAD1 (8:10), '(I3.3)') NCOLS

      BKGRD = getbkcolor ()
      NITER = (NCOLS + 7) / 8
      ROW = 0

      CALL SET_PRN_BINARY
      OPEN (UNIT = PRNOUT, FILE = 'PRN', ACCESS = 'SEQUENTIAL',
     1      FORM = 'BINARY', MODE = 'WRITE', ERR = 800)
      WRITE (PRNOUT, ERR = 800) CHAR (27), '*r3F', CHAR (27), '*t150R',
     1                          HEAD1 (1:13), CHAR (27), '*b0M'
      HEAD1 (2:3) = '*b'
      WRITE (HEAD1 (4:6), '(I3.3)') NITER
      HEAD1 (7:7) = 'W'
      DO 60 K = 1, NROWS
          COL = 0
          DO 40 L = 1, NITER
              PRDATA (L) = CHAR (0)
              DO 30 J = 1, 8
                  IF (getpixel (COL, ROW) .NE. BKGRD)
     1                PRDATA (L) = CHAR (ICHAR (PRDATA (L)) + PIN (J))
                  COL = COL + 1
 30           CONTINUE
 40       CONTINUE
          WRITE (PRNOUT, ERR = 800) HEAD1(1:7), (PRDATA (L), L=1,NITER)
          IF (RESLN .EQ. 0)   WRITE (PRNOUT, ERR = 800) 
     1                              HEAD1(1:7), (PRDATA (L), L=1,NITER)
          ROW = ROW + 1
 60   CONTINUE

      WRITE (PRNOUT, ERR = 800)  CHAR (27), '*rB', CHAR (12)
      CLOSE (UNIT = PRNOUT, ERR = 800)
      GOTO 100

 800  CONTINUE
      CALL puttext ('*** ERROR IN PRINTING ***', INT2 (1), INT2 (25))
 100  CONTINUE
      X = xy.xcoord
      Y = xy.ycoord
      CALL setvieworg (X, Y, xy)
      CALL RESET_PRN

      RETURN
      END


      SUBROUTINE Conv2PCX (FN, XMAX, YMAX)

      IMPLICIT NONE
      INCLUDE  'FGRAPH.FD'

      INTEGER*2 XMAX, YMAX
      CHARACTER*(*) FN

      INTEGER*2 MAXCOLS
      PARAMETER (MAXCOLS = 720)

      INTEGER*2  maxx, maxy, topx, topy, graphics, colour, tmode,
     1           charx, chary, resln
      REAL*4 xmult, ymult
      COMMON /GRAPHICS/ MAXX, MAXY, TOPX, TOPY, GRAPHICS, COLOUR, TMODE,
     1                  XMULT, YMULT, CHARX, CHARY, RESLN

      CHARACTER*1 PRDATA (MAXCOLS)
      INTEGER*2 PIN (8), PRNOUT, X, Y
      PARAMETER (PRNOUT = 22)
      INTEGER*2 NCOLS, NROWS, NBYTES, COL, ROW, BYTE, I, J, BKGRD
      INTEGER*2 COUNT, OLDBYTE, INDEX
      RECORD /xycoord/ xy
      DATA PIN /128, 64, 32, 16, 8, 4, 2, 1/

      IF (GRAPHICS .EQ. 0)  RETURN

      CALL setvieworg (0, 0, xy)

      NCOLS = MAXX + 1
      IF (NCOLS .GT. XMAX)  NCOLS = XMAX
      IF (NCOLS .GT. MAXCOLS) THEN
           WRITE (*,*) ' ERROR: Too many columns in conv2pcx.'
           RETURN
      END IF

      NROWS = MAXY + 1
      IF (NROWS .GT. YMAX)  NROWS = YMAX
      ROW = 0
      BKGRD = getbkcolor ()

      OPEN (UNIT = PRNOUT, FILE = FN, ACCESS = 'SEQUENTIAL',
     1      FORM = 'BINARY', MODE = 'WRITE', ERR = 800)

      NBYTES = (NCOLS + 7) / 8
      PRDATA (1) = CHAR (10)
      PRDATA (2) = CHAR (3)
      PRDATA (3) = CHAR (1)
      PRDATA (4) = CHAR (1)
      DO 5 J = 5, 128
          PRDATA (J) = CHAR (0)
 5    CONTINUE
      PRDATA (9) = CHAR (IAND ((NCOLS - 1), 255))
      PRDATA (10) = CHAR (ISHFT ((NCOLS - 1), -8))
      PRDATA (11) = CHAR (IAND ((NROWS - 1), 255))
      PRDATA (12) = CHAR (ISHFT ((NROWS - 1), -8))
      PRDATA (66) = CHAR (1)
      PRDATA (67) = CHAR (IAND (NBYTES, 255))
      PRDATA (68) = CHAR (ISHFT (NBYTES, -8))
      PRDATA (69) = CHAR (1)
      WRITE (PRNOUT, ERR = 800)  (PRDATA (J), J=1,128)      

      DO 60 ROW = 1, NROWS
          COL = 0
          COUNT = 0
          INDEX = 1
          DO 40 I = 0, NBYTES
               IF (I .LT. NBYTES) THEN
                    BYTE = 255
                    DO 30 J = 1, 8
                         IF (getpixel (COL, ROW) .NE. BKGRD)
     1                        BYTE = BYTE - PIN (J)
                         COL = COL + 1
                         IF (COL .GE. NCOLS)  GOTO 35
 30                 CONTINUE
               ELSE
                    BYTE = -1
               END IF
 35            CONTINUE
               IF (BYTE .EQ. OLDBYTE .AND. COUNT .LT. 63)  THEN
                    COUNT = COUNT + 1
               ELSE
                    IF (COUNT .GT. 1) THEN
                         PRDATA (INDEX) = CHAR (COUNT + 192)
                         PRDATA (INDEX+1) = CHAR (OLDBYTE)
                         INDEX = INDEX + 2
                    ELSE IF (COUNT .GT. 0) THEN
                         IF (OLDBYTE .GE. 192) THEN
                              PRDATA (INDEX) = CHAR (193)
                              PRDATA (INDEX+1) = CHAR (OLDBYTE)
                              INDEX = INDEX + 2
                         ELSE
                              PRDATA (INDEX) = CHAR (OLDBYTE)
                              INDEX = INDEX + 1
                         END IF
                    END IF
                    OLDBYTE = BYTE
                    COUNT = 1
               END IF
 40       CONTINUE
          INDEX = INDEX - 1
          WRITE (PRNOUT, ERR = 800)  (PRDATA (I), I=1,INDEX)
 60   CONTINUE

      CLOSE (UNIT = PRNOUT, ERR = 800)
      GOTO 100

 800  CONTINUE
      CALL puttext ('*** ERROR IN WRITING PCX FILE ***',
     1              INT2 (1), INT2 (25))
 100  CONTINUE
      X = xy.xcoord
      Y = xy.ycoord
      CALL setvieworg (X, Y, xy)

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

