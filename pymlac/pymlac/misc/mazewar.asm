TITLE MAZE.3 GREG THOMPSON (GAT) 04/11/74

;				     MAZE

;       Maze  is  a  experiment  in  3  dimensional  graphics  and  intertask
;   teleconferencing.	 It is a hunt  and seek game that  can involve up to
;   eight Imlacs.   The Imlac user is  placed in a 16  by 32 square maze  and
;   attempts  to hunt down and destroy the other inhabitents of the maze (the
;   other Imlac  users) before  they do  the same  to him.   Each  player  is
;   represented by his uname (1 through 8 characters) as he moves through the
;   maze.   The  various keys that are  used to move through  the maze and to
;   fire are described below.
;
;      UP ARROW   - Move forward 1 square.
;      DOWN ARROW - Back up one square.
;      LEFT ARROW - Turn 90 degrees to the left.
;      RIGHT ARROW- Turn 90 degrees to the right.
;      FUNCTION 4 - Turn 180 degrees around.
;      PAGE XMIT  - Peek around the corner to the left.
;      XMIT	  - Peek around the corner to the right.
;      ESC	  - Fire.
;      CTRL -Z	  - Exit maze program.
;      FORM	  - Erase dispay buffer.
;      FUNCTION 7 - Look at maze from top.
;
;	The player enters the maze by typing MAZE<cr>; to monit or MAZE^k  to
;   DDT,  while at an imlac.   The  screen will be blank  for a minute or two
;   while the imlac side of the maze program is loaded after which the player
;   is placed in to the maze along with any other players.   A letter on  the
;   top of the screen indicates the direction you are currently facing.   The
;   unames of the other players are listed on the sides followed their  score
;   and  the number of times  they were shot.   Anytime a  player is shot the
;   bell will ring and  an '!' will  be placed next  to the shooting  players
;   score  and an '*' will be placed next to the number of times shot counter
;   of the player that was just shot.  Holding down the up or down arrow keys
;   will cause them to repeat.  After a shot is fired the player who is being
;   shot at has  two seconds  to get  out of view  of the  position that  the
;   shooting  player  was  at at  the  time  he fired  the  shot.   All other
;   characters typed are placed in a display buffer at the bottom of all  the
;   imlac's  screen.   Holding the Function-7 (or TAB as the case my be) will
;   allow you to view your position in the maze from the top.
;        The  3 buttons on the mouse and the 5 keyset buttons  may be used as
;   controls and have the following functions, starting from the left of  the
;   mouse;  peek  left,  fire,  peek  right,  turn  around,  turn  left, move
;   forward, turn right, and move backwards.
;        Users may specify their own mazes if they are the first player in  a
;   maze by giving a file name after 'maze to use: '.  Just a CR will default
;   to the standard maze.  User mazes must have a specific format if they are
;   to be able to work. They must begin with a LOC 10020 followed by the label
;   MAZE:  on  the first of  32.   octal words which  form a bit  map for the
;   maze.   The maze must  end with  LOC 17713, JMP @.+1, 101,  and an  END.
;   After assembling the maze must be imtraned by using the 'IMTRAN' command.
;   A  muddle function exists for printing out formated source mazes.   It is
;   initiated by  floading 'imlac;maze  print'  in  muddle and  then  issuing
;   <PRINT-MAZE  'input file spec' 'output file spec'>$ where the output file
;   spec defaults to the TTY.   An example of a formated source maze is given
;   below:

;.INSRT IMSRC;IMDEFS >
;
;	   LOC   10020'
;
; MAZE:	   177777	   ; HERE IS THE 32 WORD MAZE.
;	   106401	   ; NO FOUR SQUARES MAY BE EMPTY.
;	   124675	   ; AND SHARE A COMMON CORNER.
;	   121205	   ; ALL OUTSIDE WALLS MUST BE FILLED IN.
;	   132055	   ; THIS IS THE DEFAULT MAZE.
;	   122741
;	   106415
;	   124161
;	   121405
;	   135775
;	   101005
;	   135365
;	   121205
;	   127261
;	   120205
;	   106765
;	   124405
;	   166575
;	   122005
;	   107735
;	   120001
;	   135575
;	   105005
;	   125365
;	   125225
;	   121265
;	   105005
;	   135375
;	   100201
;	   135675
;	   110041
;	   177777
;
;	   END	101'	; AUTO START BACK INTO CONSOLE PROGRAM
;
;   Players start in random loctions.

;   The current default maze is:
;
;			      N O R T H
;
;
;	     $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
;	     $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
;	     $$$	 $$$$$$   $$$   		  $$$
;	     $$$	 $$$$$$   $$$   		  $$$
;	     $$$   $$$   $$$	  $$$$$$   $$$$$$$$$$$$   $$$
;	     $$$   $$$   $$$	  $$$$$$   $$$$$$$$$$$$   $$$
;	     $$$   $$$         $$$   $$$	    $$$   $$$
;	     $$$   $$$         $$$   $$$	    $$$   $$$
;	     $$$   $$$$$$   $$$ 	   $$$   $$$$$$   $$$
;	     $$$   $$$$$$   $$$ 	   $$$   $$$$$$   $$$
;	     $$$   $$$      $$$   $$$$$$$$$$$$  	  $$$
;	     $$$   $$$      $$$   $$$$$$$$$$$$  	  $$$
;	     $$$	 $$$$$$   $$$   	 $$$$$$   $$$
;	     $$$	 $$$$$$   $$$   	 $$$$$$   $$$
;	     $$$   $$$   $$$		$$$$$$$$$	  $$$
;	     $$$   $$$   $$$		$$$$$$$$$	  $$$
;	     $$$   $$$         $$$$$$   	    $$$   $$$
;	     $$$   $$$         $$$$$$   	    $$$   $$$
;	     $$$   $$$$$$$$$   $$$$$$$$$$$$$$$$$$$$$$$$   $$$
;	     $$$   $$$$$$$$$   $$$$$$$$$$$$$$$$$$$$$$$$   $$$
;	     $$$	       $$$		    $$$   $$$
;	     $$$	       $$$		    $$$   $$$
;	     $$$   $$$$$$$$$   $$$   $$$$$$$$$$$$   $$$   $$$
;	     $$$   $$$$$$$$$   $$$   $$$$$$$$$$$$   $$$   $$$
;	     $$$   $$$         $$$   $$$	    $$$   $$$
;	     $$$   $$$         $$$   $$$	    $$$   $$$
; 	W    $$$   $$$   $$$$$$$$$   $$$   $$$$$$	  $$$     E
;	     $$$   $$$   $$$$$$$$$   $$$   $$$$$$	  $$$
;	E    $$$   $$$  	     $$$	    $$$   $$$     A
;	     $$$   $$$  	     $$$	    $$$   $$$
;	S    $$$	 $$$$$$   $$$$$$$$$$$$$$$   $$$   $$$     S
;	     $$$	 $$$$$$   $$$$$$$$$$$$$$$   $$$   $$$
;	T    $$$   $$$   $$$	  $$$   	    $$$   $$$     T
;	     $$$   $$$   $$$	  $$$   	    $$$   $$$
;	     $$$$$$$$$   $$$$$$   $$$   $$$$$$$$$$$$$$$   $$$
;	     $$$$$$$$$   $$$$$$   $$$   $$$$$$$$$$$$$$$   $$$
;	     $$$   $$$      $$$ 		    $$$   $$$
;	     $$$   $$$      $$$ 		    $$$   $$$
;	     $$$	 $$$$$$$$$$$$$$$$$$   $$$$$$$$$   $$$
;	     $$$	 $$$$$$$$$$$$$$$$$$   $$$$$$$$$   $$$
;	     $$$   $$$  				  $$$
;	     $$$   $$$  				  $$$
;	     $$$   $$$$$$$$$   $$$$$$   $$$$$$$$$$$$$$$   $$$
;	     $$$   $$$$$$$$$   $$$$$$   $$$$$$$$$$$$$$$   $$$
;	     $$$	 $$$   $$$		    $$$   $$$
;	     $$$	 $$$   $$$		    $$$   $$$
;	     $$$   $$$   $$$   $$$   $$$$$$$$$$$$   $$$   $$$
;	     $$$   $$$   $$$   $$$   $$$$$$$$$$$$   $$$   $$$
;	     $$$   $$$   $$$   $$$   $$$      $$$   $$$   $$$
;	     $$$   $$$   $$$   $$$   $$$      $$$   $$$   $$$
;	     $$$   $$$         $$$   $$$   $$$$$$   $$$   $$$
;	     $$$   $$$         $$$   $$$   $$$$$$   $$$   $$$
;	     $$$	 $$$   $$$		    $$$   $$$
;	     $$$	 $$$   $$$		    $$$   $$$
;	     $$$   $$$$$$$$$   $$$   $$$$$$$$$$$$$$$$$$   $$$
;	     $$$   $$$$$$$$$   $$$   $$$$$$$$$$$$$$$$$$   $$$
;	     $$$		     $$$		  $$$
;	     $$$		     $$$		  $$$
;	     $$$   $$$$$$$$$   $$$$$$$$$   $$$$$$$$$$$$   $$$
;	     $$$   $$$$$$$$$   $$$$$$$$$   $$$$$$$$$$$$   $$$
;	     $$$      $$$		   $$$  	  $$$
;	     $$$      $$$		   $$$  	  $$$
;	     $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
;	     $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
;
;
;			       S O U T H
;

; MAZE PROTOCOL:	MESSAGES ARE SENT TO ALL OTHER IMLACS
;			DO NOT SEND TO ORIGINATING IMLAC
;
; 001 -- PLAYER LEAVES GAME
;  <ID>
;
; 002 -- PLAYER MOVED
;  <ID>
;  <NEW DIRECTION  WITH 100 BIT ON>
;  <NEW XLOC WITH 100 BIT ON>
;  <NEW YLOC WITH 100 BIT ON>
;
; 003 -- PLAYER DIED
;  <ID>
;  <ID OF WHO DIED>
;
; 004 -- ANNOUNCE NEW PLAYER
;  <ID # OF NEW PLAYER>
;  <6 CHARS OF ID NAME>
;  <2 CHAR # OF HITS WITH 100 BIT ON>  (HIGH ORDER 6 BITS THEN LOW ORDER 6 BITS)
;  <2 CHAR # OF DEATHS WITH 100 BIT ON>
;
; 014 -- ERASE DISPLAY RING BUFFER
;
;
; IDS MUST BE >= 1 AND <= 8.
;
; ALL INCOMING MESSAGES ARE CHECKED FOR LEGALITY.  BAD MESSAGES ARE FLUSHED.
; A NUMBER IN THE STATUS LINE INDICATES THE NUMBER OF BAD MESSAGES RECIEVED.
; INFORMATION CONCERNING THE LAST BAD MESSAGE RECIEVED IS SAVED FOR LATER EVALUATION.
;
; ALL CHARACTERS SUBROUTINES AND THE DJMS TABLE IS UP IN THE CONSOLE PROGRAM (SSV).
; THE DJMS TABLE IS ACCESSED THROUGH LOCATION 24 OCTAL WHICH STARTS WITH THE ENTRY
; FOR OCTAL CODE 40 (SPACE).
;
; ANY CHARACTERS TYPED ON CONSOLE (>014') ARE SENT TO PDP-10 AND SHOULD
; BE ECHOED TO ALL! CONSOLES INCLUDING THE ORIGINATOR.
;
; ANY OTHER CHARACTERS RECEIVED BY IMLAC ARE DISPLAYED IN A
; RING BUFFER AT THE BOTTOM OF THE PICTURE.
;
; THE FIRST ANNOUNCE NEW PLAYER MESSAGE THE IMLAC RECIEVES DEFINES ITS ID.
;
; THIS VERSION REQUIRES A GRAPHICS IMLAC WITH LONG VECTOR HARDWARE
; MULTI-LEVEL SUBROUTINING, AND 8K DISPLAY ADDRESSING MOD.
;
; THE MESSAGE SWITCHING PROGRAM ON THE 10 MUST ALSO KEEP TRACK
; OF THE CURRENT SCORES OF ALL THE PLAYERS SO WHEN A NEW PLAYER
; JOINS INTO A ALREADY EXISTING GAME HE MAY RECIEVE THE CURRECT
; SCORES OF ALL THE PLAYERS.
;
; WHEN AN IMLAC WANTS TO JOIN AN EXISTING MAZE THE FOLLOWING OCCURS:
;	1) THE MAZE PROGRAM IS LOADED INTO HIS IMLAC.
;	2) THE CURRENT MAZE IS LOADED ON TOP OF THE DEFAULT MAZE
;	   IF THE DEFAULT MAZE IS NOT BEING USED.
;	3) A TYPE 4 MESSAGE IS SENT TO ALL IMLACS ANOUNCING THE
;	   NEW IMLAC.  THE NEW IMLAC GETS HIS ID FROM THIS MESSAGE.
;	4) TYPE 4 MESSAGES FOR ALL THE OTHER PLAYERS ARE SENT TO
;	   THE NEW IMLAC.
;
; WRITTEN BY:
;
; HOWARD PALMER		STANFORD	ORIGINAL IDEA & STAND-ALONE VERSION OF MAZE
; STEVE COLLEY 		CAL TECH	ORIGINAL IDEA OF MAZE, STAND-ALONE MAZE
;					& CRUDE MULTIPLE PLAYERS
; GREG THOMPSON		M.I.T.		FULL MULTIPLE PLAYERS ADDITIONS
; DAVE LEBLING		M.I.T.		PDP-10 MESSAGE SWITCHER AND ROBOTS
; KEN HARRENSTEIN	M.I.T.		PDP-10 part of fast interaction protocol
; CHARLES FRANKSTON	M.I.T.		IMLAC part of fast interaction protocol.

; actual program begins here

.INSRT IMSRC;IMDEFS >
			; To keep midas from barfing 'RES' at use of these syms in prg.
IF1 EXPUNGE FIX,MOVE,PTR,EXP

FAST==1			; to assemble fast-protocol version.
CHEAT==0		; conditional to assemble cheater stuff

.MLLIT==1

	LOC	10000'

.ADDR.=1	; 8k addressing for display opcodes

	JMP	START		; starting point
	JMP	RESTART		; restarting entry point
	JMP	LEAVE		; entry to return to ssv (on error)
	JMP	RETN		; reenter maze main loop

			; auto increment register definitions 
DPTR=10'		; index loc 10 used as pointer
VISPT=11'
VISPT2=12'
VISPT3=13'
VISPT4=14'
VISPT5=15'
			; index location 16' and 17' used by interupt routine

	LOC	10020'

; here is the 32 word maze:  no four squares may be empty and share a
; common corner, and all outside walls must be filled in

MAZE:	177777 ? 106401 ? 124675 ? 121205 ? 132055 ? 122741 ? 106415 ? 124161
	121405 ? 135775 ? 101005 ? 135365 ? 121205 ? 127261 ? 120205 ? 106765
	124405 ? 166575 ? 122005 ? 107735 ? 120001 ? 135575 ? 105005 ? 125365
	125225 ? 121265 ? 105005 ? 135375 ? 100201 ? 135675 ? 110041 ? 177777


; here to wait for the loader signal

LOADER:	RSF
	 JMP .-1
	CLA
	RRC
	AND [177]
	SAM [^A]
	 JMP LOADER
	RSF
	 JMP .-1
	CLA
	RRC
	AND [177]
	SAM [^A]
	 JMP LOADER
	JMP @[40]

;	dstat, dx, dy, dir	is my position and point into info table

DSTAT:	0			; status flag
DX:	0				; x position of this imlac
DY:	0				; y position of this imlac
				; start out big so we won't show up on map
DIR:	0				; direction he is pointing
				; bits 14 and 15 have meaning
				;  bit 14,bit 15
				;	0 0  north
				;	0 1  east
				;	1 0  south
				;	1 1  west

NEXTBIT:0	
ETEM:	0	
WPTR:	0	
WPTR2:	0
CNT:	0			; counters
CNT2:	0	
KILL:	0			; last player killed by this imlac
PTR4:	0			; pointers
PTR3:	0
PTR2:	0
PTR:	0	
XDELTA:	0	
YDELTA:	0	
BEAMBIT:0	
LASTRIG:0	
LASTLEF:0	
HALLNGTH:0	
MYREAL:	0			; the real id of this imlac
MYBIT:	0			; the id of this imlac
MYBIT1:	0			; mybit-1 (normalize to 0-7)
IID:	0			; temporary imlac id used for see routine
MPTR:	0	
BIT:	0	

		; keyboard and keyset input data

KEY:	0			; last key read in
KEYSET:	0			; last value from keyset
KSCNT:	0			; keyset repeat counter

HOME:	1372'			; ctrl z	[exits program]
BACKUP:	204'			; down arrow	(backup one square)
RTURN:	205'			; right arrow	(turn 90 degrees right)
MOVE:	206'			; up arrow	(move forward one square)
LTURN:	210'			; left arrow	(turn 90 degrees left)
TURNA:	234'			; function 4	(turn 180 degrees around)
PEEKR:	202'			; xmit	(peek to the right)
FIRE:	233'			; esc	(fire)
PEEKL:	216'			; page xmit	(peek to the left)
ERING:	214'			; form	(erase ring buffer)
TOPVW:	211'			; tab	(get a top view of maze)

TEM1:	0			; temporarys
TEM2:	0
TEM3:	0

TOPSW:	-1			; indicates whether a top or inside view

IFN FAST,[
RELCNT:	0			;counter of rel positions between abs
]

;	start of game

START:	IOF			; disable any interupts
	CLA
	DAC	ICNT		; set no message pending
	DAC	MYBIT		; indicate we have no id
	MSW			; set initial keyset value
	DAC	KEYSET
	LAC	[7776']		; limit ssv's display list
	DAC	@[25']
	JMS	ERASE		; reset ring buffer
	LAC	[MESAGE-1]	; set up you were shot message
	DAC	11'
	LAC	[YWSB-1]
	DAC	12'
	LWC	17.
	DAC	CNT2
SETUPN:	LAC	@12'
	JMS	GETCHR
	DAC	@11'
	ISZ	CNT2
	JMP	SETUPN
;
;	now wait for our id
;
	JMS	CHARIN
	LAC	MYBIT		; wait for identifier message to come in
	ASN			; has it been set yet?
	 JMP	.-3		; no, keep waiting
	STA
	DAC	TOPSW		; display top view
;
;	place player in maze
;
RESTART:KCF			; reset keyboard
RESET1:	JMS	RANDOM
	AND	[17']
	DAC	@DX
	JMS	RANDOM
	AND	[37']
	DAC	@DY
	JMS	PNTBIT
	LAC	@MPTR
	AND	BIT
	ASZ
	 JMP	RESET1
	JMS	RANDOM
	AND	[3]
	DAC	@DIR
	LAC	[AD1]		; reset to main screen
	DAC	WHICHD
IFN FAST,[
	CLA
	DAC	RELCNT		; force abs. position out first thing.
]
	JMP	RETN4

RETN2:	CLA			; look from inside maze
	DAC	TOPSW
;
;	send new position to 10
;
RETN4:	STA			; set to playing status
	DAC	@DSTAT
	JMS	PRINT		; build current display
IFE FAST,[
	JMS	ABSMSG		; send out absolute position
	JMP	RETN
]
IFN	FAST,[
	LAC	RELCNT
	ASM			; if ge 0, something wants an abs pos sent out.
	 JMS	ABSMSG		; sigh, send absolute
	JMP	RETN		; and continue

RELMSG:	0
	IOR MYBIT1
	JMS SEND1
	ISZ RELCNT
	 NOP
	JMP @RELMSG

] ;end of ifn fast

; send new absolute position
ABSMSG:	0
IFN FAST,[
	LWC	20		;number of rel messages before an abs
	DAC	RELCNT		;set counter
]
	LAW	2			; send moved message code
	JMS	SEND1
	LAC	MYBIT		; send my id
	JMS	SEND1
	LAC	@DIR		; send new direction
	AND	[3]		; send only lower 2 bits!
	IOR	[100']
	JMS	SEND1
	LAC	@DX		; send new x location
	IOR	[100']
	JMS	SEND1
	LAC	@DY		; send new y location
	IOR	[100']
	JMS	SEND1
	JMP	@ABSMSG		;return

;
;	main loop
;
RETN:	JMS	CHARIN		; get stuff from ten
	JMS	DISP		; maintain display
RETN3:	KSF			; no, is there a key down?
	 JMP	KSCHK		; no, now check keyset
	CAL			; yes, read the key
	KRC
	DAC	KEY
	LWC	8.		; set up to rept key (time before start repeating)
	DAC	REPTCNT
REPT:	LAC	KEY
KEYREPT:SAM	HOME		; is it ctrl-z?
	 JMP	KEYCHK
	LAC	MYBIT		; remove me from maze
	DAC	ININFO
	JMP	GONER
;
;	check keyset
;
KSCHK:	CLA
	MSW
	SAM	KEYSET		; has it changed?
	 JMP	.+2		; yes, so do something about it
	  JMP	RETN		; no, re-enter main loop
	DAC	KEYSET		; save new value
	LWC	15.		; set up to repeat
	DAC	KSCNT
KSREPT:	LAC	[BACKUP]		; now figure which key to simulate
	DAC	PTR
	LAC	KEYSET
	IOR	[174340']		; turn on bits to ignore
	CMA\CLL
	ASN
	 JMP	RETN
	RAR	1
	LSZ
	 JMP	GOTIT
	XAM	PTR
	IAC
	XAM	PTR
	JMP	.-6

GOTIT:	LAC	@PTR		; get appropriate key
	DAC	KEY
	JMP	KEYREPT
;
;	see if we are blowing up
;
KEYCHK:	LAC	BIGEXP		; if so then ignore keys
	ASZ
	 JMP	RETN		; yes, so wait it out
;
;	check for various keyboard commands
;
KEY1:	LAC	KEY
	SAM	RTURN		; turn right?
	 JMP	KEY2
	ISZ	@DIR
	 NOP
IFN FAST,[
	LAC	[20']		; new protocol for right turn
	JMS	RELMSG
]
	JMP	RETN2

KEY2:	SAM	LTURN		; left turn?
	 JMP	KEY3
	LAC	@DIR
	SUB	[1]
	DAC	@DIR
IFN FAST,[
	LAC	[30']		; new protocol for left turn
	JMS	RELMSG
]
	JMP	RETN2

KEY3:	SAM	MOVE		; move forward?
	 JMP	KEY4
	JMS	MOVER
	JMP	RETN
IFN FAST,[
	LAC	[150']		; new protocol for move forward
	JMS	RELMSG
]
	JMP	RETN2

KEY4:	SAM	PEEKL		; peek left?
	 JMP	KEY5
	JMS	MOVER
	JMP	RETN
;ifn fast,[
;	lac	[150']		; new protocol for move forward
;	ior	mybit1		; insert id
;	jms send1
;]
	LAC	@DIR
	SUB	[1]
	DAC	@DIR
	JMS	HOLD
	LAC	@DIR
	SUB	[1]
	DAC	@DIR
PEEKER:	JMS	MOVER
	JMP	RETN
	JMS	ADIR2
	JMP	RETN2

KEY5:	SAM	PEEKR		; peek right?
	 JMP	KEY6
	JMS	MOVER
	JMP	RETN
	ISZ	@DIR
	 NOP
	JMS	HOLD
	ISZ	@DIR
	 NOP
	JMP	PEEKER

KEY6:	SAM	TURNA		; turn around?
	 JMP	KEY7
	JMS	ADIR2
IFN FAST,[
	LAC	[140']		; new protocol for turn-around
	JMS	RELMSG
]
	JMP	RETN2

KEY7:	SAM	BACKUP		; back up?
	 JMP	KEY8
	JMS	ADIR2
	JMS	MOVER
	JMP	KEY7NP
	JMS	ADIR2
IFN FAST,[
	LAC	[160']		; new protocol for move backwards.
	JMS RELMSG
]
	JMP	RETN2

KEY7NP:	JMS	ADIR2		; can't move backwards, restore direction.
	JMP	RETN

ADIR2:	0
	LAC	@DIR
	ADD	[2]
	DAC	@DIR
	JMP	@ADIR2

KEY8:	SAM	FIRE		; fire?
	 JMP	KEY9
;
;	look for visible opponent to shoot at
;
	LAC	[THING+4]		; set display list pointer
	DAC	PTR
	LWC	8.		; 8 possible imlacs
	DAC	CNT2
	LAC	[IM1+4]		; set info table pointer
	DAC	VISPT
	IAC
	DAC	PTR2
CHKNEXT:LAC	@PTR		; get display body
	SAM	[DNOP]		; is he visible?
	 JMP	NOTDNOP
NOTHIM:	LAC	VISPT		; no, bump pointers to next player
	ADD	[11.]
BUMPTRS:DAC	VISPT
	IAC
	DAC	PTR2
	LAC	PTR
	ADD	[6]
	DAC	PTR
	ISZ	CNT2		; did we check them all
	 JMP	CHKNEXT		; no
	JMP	RETN		; yes, return

NOTDNOP:SAM	JMSEXP		; could he already be exploding?
	 JMP	FOUNONE		; no, so we found a opponent to shoot at
	JMP	NOTHIM		; yes, so don't fire at him
FOUNONE:LAC	@PTR2		; are we already firing on this guy?
	ASZ			; if so then don't fire again
	 JMP	NOTHIM
	LWC	80.		; set 2 second delay to allow player to dodge it
	DAC	@VISPT
	LAC	@DIR
	DAC	@VISPT
	LAC	@DX		; save our location
	DAC	@VISPT
	LAC	@DY
	DAC	@VISPT
	LAC	VISPT		; now check next player
	ADD	[7]
	JMP	BUMPTRS
;
;	does he want screen erased?
;
KEY9:	SAM	ERING
	 JMP	VIEWTOP		; no
	JMS	ERASE		; yes, so erase it
	JMP	RETN		; then return to main loop
;
;	look at maze from top
;
VIEWTOP:SAM	TOPVW		; look at maze from top?
IFE CHEAT,	JMP SENDIT
IFN CHEAT,	JMP CHNGP
	STA			; yes, set flag for top view
	DAC	TOPSW
	JMS	PRINT		; and build display
VTWAIT:	JMS	CHARIN
	JMS	DISP
	CAL
	KRB
	SAM	TOPVW		; display top view as long 
	 JMP	.+2		; as key is held down
	  JMP	VTWAIT
	CLA			; look inside again
	DAC	TOPSW
	JMS	PRINT
	JMP	RETN

IFN CHEAT,[
;
;	secret id switching keys
;
;	ctrl-rept 0 to :
;	0	return to original id
;	n	changes to id n
;	:	complement forward square
;
CHNGP:	SUB	[3260']
	ASP
	 JMP	SENDIT
	SAM	[10.]		; ctrl-rept : ?
	 JMP	.+2		; no
	  JMP	ZAP		; yes
	ASN			; ctrl-repeat 0?
	LAC	MYREAL		; if so get my real id
	SUB	[9.]
	ASM
	 JMP	RETN
	ADD	[9.]
	DAC	TEM1
	SAL	3
	ADD	[IML1-8.]		; see if this player is playing
	DAC	TEM2		; by seeing if his name exists
	LAC	[DJMS D040,]
	SAM	@TEM2
	 JMP	.+2
	  JMP	RETN
	LAC	TEM1
	JMS	GETD		; change us to new id
	JMS	PRINT		; display new view
	JMP	RETN

ZAP:	JMS	MOV		; set up ptrs to next square
	LAC	@MPTR		; now flip bit
	XOR	BIT
	DAC	@MPTR
	JMS	PRINT		; rebuild display
	JMP	RETN
] ;end of ifn cheat.

;
;	send other characters to 10
;
SENDIT:
IFN CHEAT,	ADD	[3260']
	AND	[177']
	SAM	[15']		; cr?
	 JMP	.+2
	  JMP	SENDOK
	SUB	[40']		; control code?
	ASP
	 JMP	RETN		; yes, so ignore it
	SUB [100']		;it's a 40-177 char, see if it's 140-177
	ASP
	ADD [40']		;no, it's 40-137, get char back.
	ADD [100']		;yes, 140-177.	make it uppercase.
	
SENDOK:	JMS	SEND1		; now send it to 10. char is either 40-137 or 15.
	JMP	RETN
;
;	hold a position for as long as the same key is held down
;
HOLD:	0	
	JMS	PRINT		; update display
HOLD1:	JMS	CHARIN		; get stuff from ten
	JMS	DISP		; maintain display
	CAL
	KRB
	SAM	KEY		; is the same key down?
	 JMP	.+2		; no, test key set for key still down
	  JMP	HOLD1		; yes, hold this location
TSTKS:	CLA
	MSW
	ASN			; do we have the hardware?
	 JMP	@HOLD		; no, just return
	AND	[2400']		; if either peek left or right still
	XOR	[2400']
	ASZ			; down then hold position
	 JMP	HOLD1
	JMP	@HOLD		; return

;
;	point mptr to appropriate word maze (y)
;	and bit to appropriate bit in word for our
;	current location
;
PNTBIT:	0	
	LAC	[MAZE]
	ADD	@DY
	DAC	MPTR
	LAC	@DX
	ASZ
	 JMP	PNT1
	LAC	[100000']
	JMP	PNT2

PNT1:	CIA
	DAC	CNT
	CLL
	LAC	[100000']
	RAR	1
	ISZ	CNT
	 JMP	.-2
PNT2:	DAC	BIT
	JMP	@PNTBIT
;
;	move forward one square
;
MOV:	0	
	CLA			; clear out increments
	DAC	TEM1		; y increment
	DAC	TEM2		; x increment
	JMS	PNTBIT		; position to current position
	LAC	@DIR		; see which direction we are heading
	AND	[1]
	ASZ
	 JMP	MOVEWE
	JMS	CREMENT		; move north or south
	DAC	TEM1
	ADD	MPTR
	DAC	MPTR
	JMP	@MOV		; return

MOVEWE:	JMS	CREMENT		; move west or east
	AND	[20']
	IOR	[RAL 1]
	DAC	NOPER
	LAC	BIT
	CLL
NOPER:	NOP
	DAC	BIT
	JMS	CREMENT
	CIA
	DAC	TEM2		; set x increment
	JMP	@MOV

MOVER:	0
	JMS	MOV		; move forwards one square 
	LAC	@MPTR		; see if it is a wall
	AND	BIT
	ASZ
	 JMP	@MOVER		; a open square
	LAC	TEM2		; update x to this square
	ADD	@DX
	DAC	@DX
	LAC	TEM1		; update y
	ADD	@DY
	DAC	@DY
	ISZ	MOVER		; and indicate we moved by skipping
	JMP	@MOVER
;
;	return 1 or -1 according to which direction we are heading
;
CREMENT:	0	
	LAC	@DIR
	SAR	1
	AND	[1]
	ASN
	 LAC	[-1]
	JMP	@CREMENT

;
;	refreshing routine
;
REFR:	0	
	DSF
	 SSF
	  JMP	@REFR
	SCF
	LAC	WHICHD		; get appropriate display list address
	DLA
	DON
	STA			; indicate 40 cycle sync
	DAC	SYNC
	JMP	@REFR

WHICHD:	AD1			; contains address of current display
SYNC:	0			; 40 cycle sync flag
BIGEXP:	0			; our explosion counter
JMSEXP:	DJMS	EXPLOSIN

EXP:	DDSP
	DDSP
	DDSP
INC1:	DDSP
INC2:	DDSP
INC3:	DDSP
	DRJM

EXPLOSIN:DLXA 1000
	DJMS	WAIT
	DSTS	3
	INC	E,D03
	INC	D03,100'
	DJMS	EXP
	INC	E,D00
INC4:	INC	D00,D00
	INC	100',100'
	DJMS	EXP
	INC	E,D00
INC5:	INC	D00,D00
INC6:	INC	D00,D00
	INC	100',100'
	DJMP	EXP
;
;	keep display and timed occurances running
;
DISP:	0
	JMS	REFR		; keep up display
	LAC	SYNC		; has the 40 cycle sync occured yet?
	ASM
	 JMP	@DISP		; no, just return
	CLA			; yes, reset it
	DAC	SYNC
;
;	check for our blowing up
;
	LAC	BIGEXP		; are we blowing up?
	ASN
	 JMP	CHKOPP		; no
	ISZ	BIGEXP		; is it finshed?
	 JMP	UPDTBIG		; no, update it
	JMP	RESTART		; yes, now restart the imlac
;
;	update 4 pointers
;
BUMPPTS:0
	LAC	VISPT2
	ADD	[5]
	DAC	VISPT2
	LAC	VISPT3
	ADD	[5]
	DAC	VISPT3
	LAC	VISPT4
	ADD	[5]
	DAC	VISPT4
	LAC	VISPT5
	ADD	[5]
	DAC	VISPT5
	JMP	@BUMPPTS
;
;	update a dlxa or dlya
;
UPDTSUB:0
	LAC	@VISPT2		; get old dlxa or dlya
	ADD	@VISPT		; add in increment
	AND	[1777']		; mask to position bits
	DAC	TEM2		; save new position
	LAC	@VISPT3		; get old dlxa or dlya again
	AND	[30000']		; get dlxa or dlya opcode bit
	IOR	TEM2		; or in position
	DAC	@VISPT4		; store it back on top of old dlxa or dlya
	JMP	@UPDTSUB		; return
;
;	update our explosion routine
;
UPDTBIG:LWC	8.		; eight pieces to update
	DAC	CNT		; set counter
	LAC	[BIGX1INC-1]	; set pointer to update list
	DAC	VISPT
	LAC	[BIGX1-1]		; set pointers to display list
	DAC	VISPT2
	DAC	VISPT3
	DAC	VISPT4
UPDTLOOP:JMS	UPDTSUB		; update x
	JMS	UPDTSUB		; update y
	JMS	BUMPPTS		; update pointers
	ISZ	CNT		; have i done all 8 bits?
	 JMP	UPDTLOOP		; no, do next one
;				yes, fall through
;	opponents explosion routine
;
CHKOPP:	LAC	[THING-2]		; check explosion timers
	DAC	PTR
	LAC	[IM1-2]
	DAC	PTR2
	LWC	9.
	DAC	CNT2
OPPBUMP:LAC	PTR
	ADD	[6.]
	DAC	PTR
	LAC	PTR2
	ADD	[11.]
	DAC	PTR2
	SUB	[9.]
	DAC	PTR3
	ISZ	CNT2
	 JMP	OPPLOOP
	JMP	UPDATE

OPPLOOP:LAC	@PTR2		; see if there is an explosion on this player
	ASN
	 JMP	OPPBUMP
	ISZ	@PTR2		; yes, but has it run out?
	 JMP	OPPBUMP
	CLA
	DAC	@PTR3		; yes, so indicate player unactive
	LAC	[DNOP]
	DAC	@PTR		; turn his explosion off
	JMP	OPPBUMP
;
;	keep updateing random explosion
;
UPDATE:	JMS	RANDOM		; update explosion (get random number)
	AND	[77']
	DAC	TEM1
	IOR	[INC E,B00]
	DAC	INC1
	AND	[77']
	SAL	3
	SAL	3
	SAL	2
	DAC	TEM2
	ADD	TEM1
	XOR	[INC 344,344]
	DAC	INC2
	LAC	TEM2
	IOR	[INC B00,100']
	DAC	INC3
	JMS	RANDOM
	AND	[77']
	DAC	TEM1
	SAL	3
	SAL	3
	SAL	2
	IOR	TEM1
	IOR	[140300']
	DAC	INC4
	XOR	[22044']
	DAC	INC5
	DAC	INC6
			; falls through to bullet checking routine

;
;	check for bullet fired and if it hits its mark
;
CHKBULL:LAC	[THING+3]
	DAC	PTR2
	IAC
	DAC	PTR3
	LAC	[IM1+5]
	DAC	PTR
	SUB	[5]
	DAC	SEEPT
	LWC	8.		; 8 imlacs to check
	DAC	CNT2
DISP1:	LAC	@PTR
	ASZ
	 JMP	DISP2
DISPNO:	LAW	11.
	ADD	PTR
	DAC	PTR
	SUB	[5]
	DAC	SEEPT
	LAW	6
	ADD	PTR2
	DAC	PTR2
	IAC
	DAC	PTR3
	ISZ	CNT2
	 JMP	DISP1
;
;	now check for repting keys
;
	LAC	REPTCNT		; rept on?
	ASN
	 JMP	CHKKS		; no, but check for keyset repeat
	ISZ	REPTCNT
	 JMP	CHKKS
	CLA
	KRB
	SAM	KEY
	 JMP	CHKKS
	SAM	MOVE		; only repeat :	move forwards?
	 JMP	.+2
	  JMP	.+3
	SAM	BACKUP		; move backwards?
	 JMP	CHKKS
	LWC	3.
	DAC	REPTCNT
	JMP	REPT		; do key again

REPTCNT:0

CHKKS:	LAC	KSCNT		; keyset rept on?
	ASN
	 JMP	@DISP		; no, so return
	ISZ	KSCNT
	 JMP	@DISP
	CLA
	MSW
	SAM	KEYSET		; is it the same??
	 JMP	@DISP
	SAM	[3433']		; move forwards?
	 JMP	.+2
	  JMP	.+3
	SAM	[3436']		; move backwards?
	 JMP	@DISP
	LWC	3.
	DAC	KSCNT
	JMP	KSREPT
;
;	if there is still a player visible then kill it
;
DISP2:	ISZ	@PTR		; is it totally fired yet?
	 JMP	DISPNO
	LAC	@SEEPT		; is he still alive
	ASM
	 JMP	DISPNO
	ISZ	PTR
	LAC	@PTR		; get our old direction
	AND	[3]
	DAC	@[SAVEDIR]
	ISZ	PTR
	LAC	@PTR		; get our old x
	DAC	@[SAVEDX]
	ISZ	PTR
	LAC	@PTR		; get our old y
	DAC	@[SAVEDY]
	LAC	PTR		; reset pointer
	SUB	[3]
	DAC	PTR
	SUB	[5]
	DAC	PTR4		; set up pointer for see routine
	LAW	9.
	ADD	CNT2
	DAC	KILL
	DAC	IID
	JMS	@[SEE]		; see if player hasn't moved out of the way
	 JMP	DISPNO		; he made it in time
	COA			; no, so shoot him down
	DAC	@PTR4		; indicate that he is now dying
	LAW	3			; send player killed message
	JMS	SEND1
	LAC	MYBIT		; send my id
	JMS	SEND1
	LAC	KILL		; send id of player killed
	JMS	SEND1
	LAC	[DNOP]
	DAC	@PTR2		; turn off eyes
	LAC	JMSEXP		; put in explosion in place of id
	DAC	@PTR3
	LAC	PTR4		; point to explosion count
	ADD	[9.]
	DAC	PTR4
	LWC	60.		; set explosion to last 1 1/2 sec.
	DAC	@PTR4
	LAC	MYBIT		; bump our score
	JMS	UPSCORE
	JMP	DISPNO

;
;	send a word to the 10
;
SEND1:	0
	DAC	TEM1		; save character
	JMS	REFR		; keep display up
	TSF			; wait for output flag
	 JMP	.-2		; not ready yet
	LAC	TEM1		; get character back
	TPC			; transmit character
	LAC	TEM1
	JMP	@SEND1		; return
;
;	random number generator
;
RANDOM:	0
	LAC RND
	ADD MYBIT
	RAL 2
	DAC RND
	XOR @RND
	DAC RND
	JMP @RANDOM

RND:	0

;
;	update score in info tables and in display list
;	enter with id in ac
;
UPSCORE:0
	DAC	SAVEID		; save id
	LWC	8.		; now turn all ! and  * off
	DAC	UPCNT
	LAC	[SCORE+3]
	DAC	PTSCORE
CLRALL:	LAC	[DNOP]
	DAC	@PTSCORE
	LAW	5
	ADD	PTSCORE
	DAC	PTSCORE
	LAC	[DNOP]
	DAC	@PTSCORE
	LAW	9.
	ADD	PTSCORE
	DAC	PTSCORE
	ISZ	UPCNT
	 JMP	CLRALL
	LAC	SAVEID		; now bump shooting players score
	JMS	POSITION		; position us to correct table
	LAC	ITEMP1		; bump pointer to count
	ADD	[4]
	DAC	ITEMP1
	ISZ	@ITEMP1		; bump score by one
	 NOP
	LAC	SAVEID		; point to shooting players score in display
	JMS	POINTSC
	JMS	SCOREIT
	LAW	41'		; insert exclamation mark
	JMS	GETCHR
	DAC	@PTSCORE
	LAC	KILL		; now do shot player shot count
	JMS	POSITION
	ADD	[10.]
	DAC	ITEMP1
	ISZ	@ITEMP1		; bump it also
	 NOP
	LAC	KILL		; next update the shot count in display
	JMS	POINTSC
	ADD	[5]
	DAC	PTSCORE
	JMS	SCOREIT
	LAW	52'		; insert asteric
	JMS	GETCHR
	DAC	@PTSCORE
	BEL			; ring bell indicating player shot
	JMP	@UPSCORE		; return

POINTSC:0
	CIA
	DAC	UPCNT
	LAC	[SCORE-14.]		; point to display list to update score
	ADD	[14.]
	ISZ	UPCNT
	 JMP	.-2
	DAC	PTSCORE
	JMP	@POINTSC
;
;	score generator subroutine
;	enter with	itemp1 -> score to be converted
;			ptscore -> 3 words where djmses are to be placed
;	leave with ptscore -> word 4 (one past the 3 djmses)
;
SCOREIT:0
	CLA
	DAC	HUNDR
	DAC	TENS
	DAC	ONES
	LAC	@ITEMP1		; get current score
	SUB	[1000.]		; make it mod 1000
	ASM
	 JMP	.-2
	ADD	[1000.]
	DAC	@ITEMP1		; store it back for posterity
	SUB	[100.]
	ASP
	 JMP	DOTENS
	ISZ	HUNDR
	 JMP	.-4

DOTENS:	ADD	[100.]
	SUB	[10.]
	ASP
	 JMP	DOONES
	ISZ	TENS
	 JMP	.-4

DOONES:	ADD	[10.]
	DAC	ONES
	LAC	HUNDR
	ASN
	 JMP	ZROSUP
	JMS	DODIGIT
	LAC	TENS
DTENS:	JMS	DODIGIT
	LAC	ONES
	JMS	DODIGIT
	JMP	@SCOREIT
ZROSUP:	LWC	20'
	JMS	DODIGIT
	LAC	TENS
	ASN
	 LWC	20'
	JMP	DTENS

DODIGIT:0
	ADD	[60'-40']
	ADD	@[24']
	DAC	UPCNT
	LAC	@UPCNT
DACIT:	DAC	@PTSCORE
	ISZ	PTSCORE
	JMP	@DODIGIT

SAVEID:	0
PTSCORE:0
UPCNT:	0
ONES:	0
TENS:	0
HUNDR:	0

;
;	build a long vector instruction
;
LV:	0	
	LAC	XDELTA
	AND	[40000']
	DAC	TEM3
	LAC	XDELTA
	ASP
	CIA
	DAC	XDELTA
	LAC	YDELTA
	AND	[20000']
	IOR	TEM3
	DAC	TEM3
	LAC	YDELTA
	ASP
	 CIA
	DAC	YDELTA
	SUB	XDELTA
	ASM
	 JMP	LV1
	AND	[7777']
	IOR	[40000']
	DAC	@DPTR
	LAC	XDELTA
	IOR	BEAMBIT
	DAC	@DPTR
	LAC	YDELTA
	JMP	LV2

LV1:	CIA
	AND	[7777']
	IOR	[40000']
	DAC	@DPTR
	LAC	YDELTA
	IOR	BEAMBIT
	DAC	@DPTR
	LAC	XDELTA
	IOR	[10000']
LV2:	IOR	TEM3
	DAC	@DPTR
	JMP	@LV

;
;	generate new display
;	send i moved message to 10
;	set up possible visible opponents
;
PRINT:	0	
	LAC	@DSTAT		; check status of player
	ASZ			; is he not playing?
	 JMP	INGAME		; no
	LAW	116'		; yes, display a 'n' then
	JMP	SETST

HEACT:	LAC	[DJMS D040,]	; if he is active then don't display anything
	JMP	SETST2

INGAME:	ASP			; is he dying?
	 JMP	HEACT		; no, then he is active!
	LAW	104'		; yes, then display a 'd' for dead
SETST:	JMS	GETCHR		; get the character
SETST2:	DAC	@[DEAD]		; put it in display
	LAC	@DIR		; first do direction letter
	AND	[3]
	ADD	[DIRLET]
	DAC	TEM1
	LAC	@TEM1
	JMS	GETCHR
	DAC	@[LETTER]
	LAC	TOPSW		; see if top or inside view
	ASN
	 JMP	INSIDE
TOPV:	LAC	[DLIST-1]		;write over maze display list
	DAC	DPTR
	LAC	[DLYA 1600',]
	DAC	@DPTR
	LAC	[DJMS DNL3,]
	DAC	@DPTR
	LWC	32.
	DAC	CNT
	LAC	[MAZE-1]
	DAC	PTR
	LAC	@DY
	SAL	3
	SAL	1
	ADD	@DX
	IAC
	CIA
	DAC	PTR4
NXTW:	LWC	16.
	DAC	CNT2
	LAC	[100000']
	DAC	BIT
	ISZ	PTR
NXTB:	ISZ	PTR4		; have we reached our location?
	 JMP	.+2
	  JMP	ME
	LAC	@PTR		; see is square open or closed
	AND	BIT
	ASZ
	 JMP	ON
	LAC	[DJMS SPMAZE,]
	JMP	ON+1

ME:	LAC	@DIR		; figure out which arrow to use
	AND	[3]
	ADD	[ARROWS]
	DAC	PTR3
	LAC	@PTR3
	JMP	ON+1

ON:	LAC	[DJMS CHARMZE,]
	DAC	@DPTR
	CLL
	LAC	BIT
	RAR	1
	DAC	BIT
	ISZ	CNT2		; this line done?
	JMP	NXTB
	LAC	[DJMS DNL3,]
	DAC	@DPTR
	ISZ	CNT
	 JMP	NXTW		; this row done?
	CLA			; dhlt at end
	DAC	@DPTR
	JMP	@PRINT

INSIDE:	JMS	PNTBIT
	LAC	[WALLS]
	DAC	WPTR
	IAC
	DAC	WPTR2
	CLA
	DAC	CNT
	LAC	[DLIST-1]
	DAC	DPTR
	LAC	[20000']
	DAC	BEAMBIT
	DSN
	 JMP	.-1
	LAC	@DIR
	AND	[1]
	ASZ
	 JMP	EW
	JMS	CREMENT
	DAC	TEM1
	CIA
	AND	[20']
	IOR	[RAL 1]
	DAC	NOP2
	XOR	[20']
	DAC	NOP3
PRNT1:	LAC	MPTR
	ADD	TEM1
	DAC	NEXTBIT
	LAC	@NEXTBIT
	AND	BIT
	DAC	NEXTBIT
	LAC	BIT
	CLL
NOP2:	NOP
	AND	@MPTR
	JMS	LBIT
	LAC	BIT
	CLL
NOP3:	NOP
	AND	@MPTR
	JMS	RBIT
	LAC	MPTR
	ADD	TEM1
	DAC	MPTR
	LAC	NEXTBIT
	JMS	ENDCHECK
	LAC	CNT
	SAM	[31.]		; special check
	 JMP	.+2
	  JMP	CLOSEOUT
	ISZ	WPTR
	ISZ	WPTR2
	ISZ	CNT
	 JMP	PRNT1
EW:	JMS	CREMENT
	DAC	TEM1
	AND	[20']
	IOR	[RAL 1]
	DAC	NOP4
	DAC	NOP5
PRNT2:	LAC	BIT
	CLL
NOP5:	NOP
	AND	@MPTR
	DAC	NEXTBIT
	LAC	MPTR
	ADD	TEM1
	DAC	TEM2
	LAC	BIT
	AND	@TEM2
	JMS	LBIT
	LAC	MPTR
	SUB	TEM1
	DAC	TEM2
	LAC	BIT
	AND	@TEM2
	JMS	RBIT
	LAC	BIT
	CLL
NOP4:	NOP
	DAC	BIT
	LAC	NEXTBIT
	JMS	ENDCHECK
	ISZ	WPTR
	ISZ	WPTR2
	ISZ	CNT
	JMP	PRNT2

LBIT:	0	
	DAC	LASTLEF
	ASZ
	 JMP	LB1
	LAC	@WPTR		 ; hallway
	CIA
	ADD	WALLS
	IOR	[10000']
	DAC	@DPTR
	LAC	@WPTR
	ADD	WALLS
	IOR	[20000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	LAC	CNT
	ASN
	 JMP	LB2
	CAL
	DAC	XDELTA
	LAC	@WPTR
	SAL	1
	CIA
	DAC	YDELTA
	JMS	LV
LB2:	LAC	@WPTR2
	CIA
	ADD	WALLS
	IOR	[20000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	CAL
	DAC	YDELTA
	LAC	@WPTR
	SUB	@WPTR2
	DAC	XDELTA
	JMS	LV
	JMS	FIX
	CAL
	DAC	XDELTA
	LAC	@WPTR2
	SAL	1
	DAC	YDELTA
	JMS	LV
	LAC	[20000']
	DAC	BEAMBIT
	CAL
	DAC	YDELTA
	LAC	@WPTR2
	SUB	@WPTR
	DAC	XDELTA
	JMS	LV
	JMP	@LBIT

LB1:	LAC	@WPTR2		; wall
	CIA
	ADD	WALLS
	IOR	[10000']
	DAC	@DPTR
	LAC	@WPTR2
	ADD	WALLS
	IOR	[20000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	LAC	@WPTR
	SUB	@WPTR2
	DAC	YDELTA
	CIA
	DAC	XDELTA
	JMS	LV
	LAC	@WPTR
	CIA
	ADD	WALLS
	IOR	[10000']
	DAC	@DPTR
	XOR	[30000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	LAC	@WPTR
	SUB	@WPTR2
	DAC	XDELTA
	DAC	YDELTA
	JMS	LV
	JMP	@LBIT

RBIT:	0	
	DAC	LASTRIG
	ASZ
	 JMP	RB1
	LAC	@WPTR		 ; hallway
	ADD	WALLS
	IOR	[10000']
	DAC	@DPTR
	XOR	[30000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	LAC	CNT
	ASN
	 JMP	RB2
	CAL
	DAC	XDELTA
	LAC	@WPTR
	SAL	1
	CIA
	DAC	YDELTA
	JMS	LV
RB2:	LAC	@WPTR2
	CIA
	ADD	WALLS
	IOR	[20000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	CAL
	DAC	YDELTA
	LAC	@WPTR2
	SUB	@WPTR
	DAC	XDELTA
	JMS	LV
	JMS	FIX
	CAL
	DAC	XDELTA
	LAC	@WPTR2
	SAL	1
	DAC	YDELTA
	JMS	LV
	LAC	[20000']
	DAC	BEAMBIT
	CAL
	DAC	YDELTA
	LAC	@WPTR
	SUB	@WPTR2
	DAC	XDELTA
	JMS	LV
	JMP	@RBIT

RB1:	LAC	@WPTR2		; wall
	ADD	WALLS
	IOR	[10000']
	DAC	@DPTR
	XOR	[30000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	LAC	@WPTR
	SUB	@WPTR2
	DAC	XDELTA
	DAC	YDELTA
	JMS	LV
	LAC	@WPTR2
	ADD	WALLS
	IOR	[10000']
	DAC	@DPTR
	LAC	@WPTR2
	CIA
	ADD	WALLS
	IOR	[20000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	LAC	@WPTR
	SUB	@WPTR2
	DAC	XDELTA
	CIA
	DAC	YDELTA
	JMS	LV
	JMP	@RBIT

FIX:	0	
	CLL
	LAC	NEXTBIT
	ASN
	 STL
	CLA
	RAR	3
	DAC	BEAMBIT
	JMP	@FIX

ENDCHECK:0	
	ASN
	 JMP	@ENDCHECK
CLOSEOUT:LAC	CNT		; set length of hallway
	DAC	HALLNGTH
	LAC	@WPTR2
	ADD	WALLS
	IOR	[20000']
	DAC	@DPTR
	XOR	[30000']
	DAC	@DPTR
	LAC	[DJMS WAIT,]
	DAC	@DPTR
	CAL
	DAC	YDELTA
	LAC	@WPTR2
	SAL	1
	DAC	ETEM
	CIA
	DAC	XDELTA
	JMS	LV
	LAC	LASTLEF
	ASZ
	 LAC	[20000']
	DAC	BEAMBIT
	CAL
	DAC	XDELTA
	LAC	ETEM
	CIA
	DAC	YDELTA
	JMS	LV
	LAC	[20000']
	DAC	BEAMBIT
	CAL
	DAC	YDELTA
	LAC	ETEM
	DAC	XDELTA
	JMS	LV
	LAC	LASTRIG
	ASN
	 JMP	EN1
	CAL
	DAC	XDELTA
	LAC	ETEM
	DAC	YDELTA
	JMS	LV
EN1:	CAL
	DAC	@DPTR		; insert the dhlt
	JMS	VISIBLE		; now check for visible opponents
	JMP	@PRINT

;
;	check for visible opponents
;
VISIBLE:0
	LWC	9.		; 8 imlacs to do
	DAC	CNT2
	LAC	[DSPTCH-1]	; set pointer to imlac info tables
	DAC	VISPT
	LAC	[THING-1]		; set up pointer to dlya's
	DAC	VISPT2
	IAC			; point to dsts's
	DAC	VISPT3
	ADD	[2]		; point to djms's eyes
	DAC	VISPT4
	IAC			; point to djms's body (name)
	DAC	VISPT5
VISLOOP:ISZ	CNT2		; have we checked all 8?
	 JMP	.+2		; no
	  JMP	@VISIBLE		; yes, return
	LAC	@VISPT		; get address of imlac's info table
	DAC	SEEPT
	DAC	PTR4
	LAC	@SEEPT		; may change it on us, so get status
	ASZ			; is this imlac playing?
	 JMP	PLAYING		; yes
	JMP	.+3
BLOWING:LAC	JMSEXP
	JMP	.+2
NOSEE:	LAC	[DNOP]		; no, so make him invisble or exploding
	ISZ	VISPT2		; don't change y
	ISZ	VISPT3		; don't change dsts
	DAC	@VISPT5		; set to invisible or exploding
	LAC	[DNOP]		; no eyes wanted
	DAC	@VISPT4
BUMP:	JMS	BUMPPTS		; update pointers to next imlac
	JMP	VISLOOP		; now do next imlac
;
;	active player
;
PLAYING:LAW	9.		; set id
	ADD	CNT2
	DAC	IID
	JMS	SEEUS		; see if it can be seen
	 JMP	NOSEE		; can't be seen
	LAC	@PTR4		; could he be blowing up?
	ASP
	 JMP	HEVIS		; he is visible
	JMP	BLOWING		; he is blowing up

SEEUS:	0
	LAC	@DIR
	AND	[3]
	DAC	@[SAVEDIR]
	LAC	@DX
	DAC	@[SAVEDX]
	LAC	@DY
	DAC	@[SAVEDY]
	JMS	@[SEE]
	JMP	@SEEUS
	ISZ	SEEUS
	JMP	@SEEUS

SEEPT:	0
FTEMP:	0

;
;	visible opponnent!
;
FIGX:	0
	LAC	@[DISTAN]		; now i know i see him
	ADD	[WALLS]		; get currect position for name
	DAC	FTEMP
	LAC	@FTEMP
	CIA
	ADD	WALLS
	IOR	[20000']		; make it a dlya
	JMP	@FIGX
HEVIS:	JMS	FIGX		; figure the new dlxa
	DAC	@VISPT2		; stick it in
	LAC	@[DISTAN]		; get distance to opponent
	SAR	3			; scale it to 2 significant bits
	XOR	[3]		; complement meanning
	IOR	[DSTS 0]		; make it a dsts instruction
	DAC	@VISPT3		; stick it in display
	JMS	FIGEYES		; figure out whether or not eyes should be displayed
	DAC	@VISPT4
	LAC	IID		; now see which opponent we can see
	ADD	[TNUM-1]		; get appropriate name
	DAC	TEM2
	LAC	@TEM2
	DAC	@VISPT5		; stick appropriate djmp to name in display list
	JMP	BUMP		; now do next opponent

FIGEYES:0
	LAC	@DIR		; see if we are facing each other
	AND	[3]
	ADD	[4]
	SUB	@[IDIR]
	AND	[3]
	ADD	[EYTAB]
	DAC	FTEMP
	LAC	@FTEMP
	JMP	@FIGEYES
;
;	shift to the left 13 subroutine
;
SAR13:	0
	SAR	3
	SAR	3
	SAR	3
	SAR	3
	SAR	1
	ASN
	 LAW	1
	JMP	@SAR13
;
;	blow us up and start again
;
ENDER:	CLA			; return to inside display
	DAC	TOPSW
	LAC	[AD2]		; set blow up display as current display
	DAC	WHICHD
	LAC	[BIGX1INC-1]	; set pointer to increment table
	DAC	VISPT
	LWC	4.		; 8 pieces to do but we will set up 2 at a time
	DAC	CNT
BLOWLOOP:JMS	RANDOM		; get random number
	JMS	SAR13		; scale it to 2 +- sig bits
	DAC	TEM1		; save for next bit
	DAC	@VISPT		; store delta in first x
	JMS	RANDOM		; get another random number
	JMS	SAR13		; scale it too
	DAC	TEM2		; also save it
	DAC	@VISPT		; store delta in first y
	LAC	TEM1		; get back first delta x
	CIA			; we want to balance explosion so
	DAC	@VISPT		; make next bit go opposite direction
	LAC	TEM2		; store second y also in opposite direction
	CIA
	DAC	@VISPT
	ISZ	CNT		; are we done with setting up deltas
	 JMP	BLOWLOOP		; no, do next 2
	LAC	[BIGX1-1]		; now reset display list dlxas and dlyas
	DAC	TEM1
	LWC	8.		; eight bits to do
	DAC	CNT
CLRLOOP:JMS	CLRSUB		; reset the dlxa
	JMS	CLRSUB		; reset the dlya
	LAC	TEM1		; update pointer to next bit of explosion
	ADD	[5]
	DAC	TEM1
	ISZ	CNT		; did we do all eight bits?
	 JMP	CLRLOOP		; no, do the rest
	JMP	RETN		; wait explosion out

CLRSUB:	0
	ISZ	TEM1		; position pointer
	LAC	@TEM1		; get dlxa or dlya
	AND	[30000']		; get opcode bits
	IOR	[1000']		; position to center of screen
	DAC	@TEM1		; stuff it back
	JMP	@CLRSUB		; return

;
;	tty input handler
;
CHARIN:	0
	RSF			; tty input?
	 JMP	EXIT		; no, so ignore interupt
	CLA
	RRC			; get character
	AND	[177']		; mask to 7 characters
	DAC	INCHAR		; save it
;
;	check to see if we are waiting for characters
;
	LAC	ICNT
	ASN
	 JMP	SETUP		; no so interpret character we got
	LAC	INCHAR		; yes, so stuff character in info table
	DAC	@17'
	ISZ	ICNT		; was that all we wanted?
	 JMP	EXIT		; no, wait for more
	JMP	@IDSPTCH		; yes, go to routine now

SETUP:	LAC	[ININFO-1]	; set up input buffer
	DAC	17`
;
;	check for imlac wants out message
;	if he does then do the following:
;	1)	indicate imlac non-active in info table
;	2)	dnop his score, body, eyes and name
;
CHK1:	LAC	INCHAR		; get character read back
	SAM	[1]		; is it type 1?
	 JMP	CHK2		; no, check next type
	LWC	1			; wait for one more word [id]
	DAC	ICNT
	LAC	[DTYP1]		; set up dispatch address
SETOUT:	DAC	IDSPTCH
	JMP	EXIT		; wait for characters to come in

DTYP1:	JMS	TESTID		; get id of imlac that wants out
GONER:	ASN
	 JMS	ERROR		; error if id = 0
	JMS	POSITION		; get position into info table
	DAC	17'
	LWC	10.
	DAC	ICNT2		; clear info entry
	CLA
	DAC	@ITEMP1		; clear status
	DAC	@17'		; clear the rest
	ISZ	ICNT2
	 JMP	.-2
	JMS	GETCNT		; now clear display list score
	LAC	[SCORE-15.]
	ADD	[14.]
	ISZ	ICNT2
	 JMP	.-2
	DAC	17'
	LAC	[DNOP]		; dnop all digits
	DAC	@17'
	DAC	@17'
	DAC	@17'
	DAC	@17'
	ISZ	17'
	DAC	@17'
	DAC	@17'
	DAC	@17'
	DAC	@17'
	JMS	GETCNT		; now clear displayed name
	LAC	[IML1-9.]
	ADD	[8.]
	ISZ	ICNT2
	 JMP	.-2
	DAC	17'
	LAC	[DJMS D040,]	; get space
	DAC	@17'
	DAC	@17'
	DAC	@17'
	DAC	@17'
	DAC	@17'
	DAC	@17'
	DAC	@17'
	JMS	GETCNT		; finally make him invisible
	LAC	[THING-4]
	ADD	[6]
	ISZ	ICNT2
	 JMP	.-2
	DAC	17'
	LAC	[DNOP]
	DAC	@17'		; clear eyes
	DAC	@17'		; clear body (name)
	LAC	ININFO		; see if it is my real it that is leaving
	SAM	MYREAL		; if so then exit program, return to ssv
	 JMP	CHKNR
;
;	exit routine
;	send player wants out to 10
;	then return to ssv
;
	LAW	1			; send i want out code
	JMS	SEND1
	LAC	MYREAL		; send my id
	JMS	SEND1
	LAC	[17776']		; restore ssv's buffer to full buffer
	DAC	@[25']
LEAVE:	IOF			; turn off interupts
	JMP	@.+1		; now exit to ssv
	101'			; address of where to exit to

CHKNR:	SAM	MYBIT		; see if it is the guy we are sim.
	 JMP	EXIT		; if not then we are done
	LAW	1			; sent leaving message to 10 for him
	JMS	SEND1
	LAC	MYBIT
	JMS	SEND1
	LAC	MYREAL		; return to our real id
	JMS	GETD
	JMS	PRINT		; rebuild display
	JMP	EXIT
;
;	check for moved to new location message
;	if it is then do the folowing:
;	1)	indicate player active in info table
;	2)	update dir, x, and y in info table
;	3)	check visibility and set it correctly
;
CHK2:
IFN FAST,[
	SUB	[20']		; no chance of move if <20
	ASP			; skip if 0 or +
	 JMP CHK23		; negative, not a new protocol move.
	SUB [20']		; a move if 17< x <40
	ASP
	 JMP CHK22		;ah, if 20=< and <40, definitely new-ptcl move.
	SUB [100']		;	a move if ge 140
	ASP
	 JMP INSRTCH		; 40=< and <140, a char.
CHK22:	LAC INCHAR
	JMP @[CHKI20]		;new ptcl move. go hack.
CHK23:
]	
	LAC INCHAR
	SAM	[2]		; is it type 2?
	 JMP	CHK3		; no but see if it is type 3
	LWC	4			; 4 more words to come
	DAC	ICNT
	LAC	[DTYP2]		; set up dispatch location
	JMP	SETOUT

DTYP2:	JMS	TESTID
	DAC	IID
	JMS	POSITION		; indicate player is active in info tables
	LAC	@ITEMP1		; get current status
	ASZ
	 ASP			; ignore message if he is exploding
	  JMP	.+2
	   JMP	EXIT
	STA
	DAC	@ITEMP1		; say player is active
	ISZ	ITEMP1
	LAC	ININFO+1		; save new direction
	IOR	[100']
	AND	[103']
	SAM	ININFO+1
	 JMS	ERROR		; direction greater than 3
	AND	[3]		; or not in 10n format
	DAC	@ITEMP1
	ISZ	ITEMP1
	LAC	ININFO+2		; save new x location
	JMS	TESTLOC		; make sure it is legal
	DAC	@ITEMP1
	ISZ	ITEMP1
	LAC	ININFO+3		; save new y location
	JMS	TESTLOC
	DAC	@ITEMP1

	;re-entry pt from higher 2k

CHK25:	JMS	GETCNT		; set up pointer to his display list slot
	LAC	[THING-7]
	ADD	[6]
	ISZ	ICNT2
	 JMP	.-2
	DAC	17'
	JMS	SEEUS		; can he be seen?
	 JMP	NOTVIS		; no
	JMS	FIGX		; yes, now figure dlxa
	DAC	@17'		; store it away
	LAC	@[DISTAN]		; now figure dsts 
	SAR	3
	XOR	[3]
	IOR	[DSTS 0]
	DAC	@17'
	ISZ	17'		; skip over wait
	JMS	FIGEYES		; next do eyes
	DAC	@17'		; store them
	LAC	IID		; last is name
	ADD	[TNUM-1]
	DAC	ITEMP1
	LAC	@ITEMP1
	DAC	@17'
	JMP	MCHK		; see if id is ours
NOTVIS:	LAC	[DNOP]		; if not visible then make it so
	ISZ	17'		; skip dlxa
	ISZ	17'		; skip dsts
	ISZ	17'		; skip over wait
	DAC	@17'		; clear eyes
	DAC	@17'		; clear body (name)
MCHK:	LAC	IID		; see if it is us
	SAM	MYBIT
	 JMP	EXIT		; no, done
	JMS	PRINT		; if so then update display
	JMP	EXIT		; done

;
;	check for player shot message
;	if so then do the following:
;	1)	indicate in table that he is blowing up
;	2)	bump shooting players score
;	3)	generate explosion if visible
;	4)	if this imlac got hit then:
;		a)	set life flag to shot
;		b)	put name of who shot us in whodidit
;
CHK3:	SAM	[3]		; type 3?
	 JMP	CHK4		; no, but try type 4
	LWC	2			; two words to wait for
	DAC	ICNT
	LAC	[DTYP3]		; set dispatch address
	JMP	SETOUT

DTYP3:	JMS	TESTID
	LAC	ININFO+1
	ASN
	 JMS	ERROR		; id zero
	SUB	[9.]
	ASP
	 JMP	.+3
	ADD	[9.]
	JMS	ERROR		; id greater than 8
	ADD	[9.]
	DAC	KILL		; save dying id for upscore
	JMS	POSITION		; indicate player is dying
	COA
	DAC	@ITEMP1
	LAC	ITEMP1
	ADD	[5]
	DAC	ITEMP1
	ADD	[4]
	DAC	ITEMP2
	CAL			;turn off any firing we have on him
	DAC	@ITEMP1
	LWC	60.		; set explosion to last 1 1/2 sec
	DAC	@ITEMP2
	LAC	ININFO+1		; see if i was shot
	SAM	MYBIT
	 JMP	NOTME
	LAC	ININFO
	ADD	[TNUM-1]		; say who did it in whodidit
	DAC	ITEMP2
	LAC	@ITEMP2
	DAC	@[WHODIDIT]
	LAC	ININFO		; wait longer in big 
	DAC	BIGEXP		; explosion if we are playing ourselves
	SAM	MYREAL		; so our new starting loc will be in effect
	 JMP	.+3
	LWC	120.
	JMP	.+2
	 LWC	80.
	XAM	BIGEXP
	JMS	UPSCORE		; update scores
	JMP	ENDER

NOTME:	LAC	ININFO+1		; now point into display list
	CIA
	DAC	ICNT2
	LAC	[THING-2]
	ADD	[6]
	ISZ	ICNT2
	 JMP	.-2
	DAC	ITEMP2
	SUB	[1]		; set pointer to eyes
	DAC	ITEMP1
	LAC	@ITEMP2		; is he currently visible?
	SAM	[DNOP]
	 JMP	VIS1		; yes
	JMP	NOEXPLO		; no

VIS1:	LAC	[DNOP]
	DAC	@ITEMP1		; yes, clear eyes
	LAC	JMSEXP		; stick in jms to explosion
	DAC	@ITEMP2
NOEXPLO:LAC	ININFO		; bump scores
	JMS	UPSCORE		; and update scores in display list
	JMP	EXIT

;
;	check to see if new name specified
;	if so then do the following:
;	1)	fill in approprate name display subroutine
;	2)	if mybit = 0 then assign the id to mybit
;
CHK4:	SAM	[4]		; type 4?
	 JMP	ERASER		; no, keep looking
	LWC	11.		; 11. more characters to wait for
	DAC	ICNT
	LAC	[DTYP4]		; set dispatch address
	JMP	SETOUT

DTYP4:	JMS	TESTID
	LAC	MYBIT		; see if mybit is zero
	ASZ
	 JMP	GOTMINE
	LAC	ININFO		; yes, so set our id
	DAC	MYREAL
	JMS	GETD
IFE FAST,	DAC	@[ORIG]		; indicate origional id in display
GOTMINE:LAC	[ININFO]		; set up pointers for transfer
	DAC	16'
	JMS	GETCNT
	LAC	[IML1-8.]		; remember 1st char is offset char
	ADD	[8.]
	ISZ	ICNT2
	 JMP	.-2
	DAC	17'
	DAC	ITEMP2
	CLA
	DAC	SPACES
	LWC	6			; move 6 character name
	DAC	ICNT2
CONVNXT:LAC	@16'
	SUB	[140']		; translate to lower case
	ASM
	 SUB	[40']
	ADD	[140']
	SAM	[40']		; space?
	 JMP	.+2		; no
	ISZ	SPACES		; yes	count them for offset char
	JMS	GETCHR		; convert to djms
	DAC	@17'
	ISZ	ICNT2
	 JMP	CONVNXT
	LAC	SPACES		; now fix offset character
	ADD	[CENTER]
	DAC	ITEMP1
	LAC	@ITEMP1
	DAC	@ITEMP2
	LAC	ININFO		; now store scores
	JMS	POSITION
	ADD	[4]
	DAC	ITEMP1
	JMS	FIXSCO		; do # of opponents shot
	LAC	ININFO
	JMS	POINTSC
	JMS	SCOREIT
	LAC	ITEMP1
	ADD	[6]
	DAC	ITEMP1
	JMS	FIXSCO		; now do # of times shot
	LAC	ININFO
	JMS	POINTSC
	ADD	[5]
	DAC	PTSCORE
	JMS	SCOREIT
	JMP	EXIT

FIXSCO:	0
	LAC	@16'
	AND	[77']
	SAL	3
	SAL	3
	DAC	ITEMP2
	LAC	@16'
	AND	[77']
	IOR	ITEMP2
	DAC	@ITEMP1
	JMP	@FIXSCO

SPACES:	0

;
;	set up our id
;
;	enter with id in ac
;
GETD:	0
	DAC	MYBIT
	SUB	[1]
	DAC	MYBIT1		; store normalized 0-7 id.
	ADD	[DSPTCH]
	DAC	ITEMP1
	LAC	@ITEMP1		; set up dstat, dx, dy, and dir ptrs
	DAC	DSTAT
	IAC
	DAC	DIR
	IAC
	DAC	DX
	IAC
	DAC	DY
IFE FAST,[
	LAC	MYBIT		; now get our id in character
	IOR	[60']
	JMS	GETCHR
	DAC	@[CURENT]		; say our current id in display
]
	JMP	@GETD
;
;
;	erase ring buffer?
;
ERASER:	SAM	[14']		; type 4?
	 JMP	INSRTCH		; no, just insert into ring buffer
	JMS	ERASE
	JMP	EXIT

ERASE:	0
	LWC	4			; reset line count
	DAC	RINGLC
	LAC	[RINGST]		; reset both pointers
	DAC	RNGPT
	IAC
	DAC	RNGPT2
	LAC	[DJMS D012,]	; replace djmp to curser
	DAC	@RNGPT
	LAC	[DJMS CUR,]
	DAC	@RNGPT2
	LAC	[DJMP RINGST,]
	DAC	@[RING]
	DAC	@[RINGEND]
	JMP	@ERASE

;
;	get djms for a character
;
GETCHR:	0
	AND	[177']		; mask to 7 bits
	SAM	[12']		; line feed?
	 JMP	.+3
	LAC	[DJMS D012,]
	JMP	STORECH
	SAM	[10']		; back space?
	 JMP	.+3
	LAC	[DJMS D010,]
	JMP	STORECH
	SAM	[15']		; cr?
	 JMP	.+3
	LAC	[DJMS D015,]
	JMP	STORECH
	SUB	[40']		; don't allow anything below 40
	ASP
	CLA
	ADD	[40']
	SUB	[140']		; translate to lower case
	ASM
	 SUB	[40']
	ADD	[140'-40']
	ADD	@[24']		; convert to djms
	DAC	ITEMP1
	LAC	@ITEMP1
STORECH:DAC	ITEMP1
	JMP	@GETCHR
;
;	insert character into ring buffer
;
INSRTCH:JMS	FORWARD
	LAC	INCHAR
	JMS	GETCHR		; get djms for character
	SAM	[DJMS D012,]
	 JMP	NOTNL		; no
	ISZ	RINGLC		; yes, but is there room on screen?
	 JMP	NOTNL
	JMS	ROLL
	JMP	OK

NOTNL:	LAC	RNGPT2
	SAM	RNGPT		; have we filled entire buffer?
	 JMP	OK		; no
	JMS	ROLL		; yes, roll top line off
OK:	LAC	[DJMP CUR,]
	DAC	@RNGPT2
	JMS	BACK		; back up pointer
	LAC	ITEMP1		; get djms again
	DAC	@RNGPT2		; stick in on top of old djmp cur
	JMS	FORWARD		; move pointer back up
	LAC	INCHAR
	SAM	[15']
	 JMP	EXIT		; done
	LAW	12'
	DAC	INCHAR
	JMP	INSRTCH

FORWARD:0			; roll rngpt2 forward one slot
	LAC	RNGPT2
	IAC
	SAM	[RINGEND]
	 JMP	.+2
	LAC	[RINGST]
	DAC	RNGPT2
	JMP	@FORWARD

BACK:	0
	STA
	ADD	RNGPT2
	SAM	[RING]
	JMP	.+2
	LAC	[RINGEND-1]
	DAC	RNGPT2
	JMP	@BACK

ROLL:	0			; roll ringpt forward one line
LOOK:	LAC	RNGPT
	IAC
	SAM	[RINGEND]
	 JMP	.+2
	LAC	[RINGST]
	SAM	RNGPT2
	 JMP	.+4
	JMS	ERASE
	JMS	FORWARD
	 JMP	@ROLL
	DAC	RNGPT
	LAC	@RNGPT
	SAM	[DJMS D012,]
	 JMP	LOOK
MOVED:	LAC	RNGPT
	AND	[7777']
	IOR	[160000']
	DAC	@[RING]
	STA
	ADD	RINGLC
	DAC	RINGLC
	JMP	@ROLL

;
;	return from character read
;
EXIT:	JMP	@CHARIN

GETCNT:	0
	LAC	ININFO		; get id of message originator
	CIA			; make it into a count
	DAC	ICNT2
	JMP	@GETCNT

POSITION:0
	ADD	[DSPTCH-1]	; point to correct status indicator
	DAC	ITEMP1
	LAC	@ITEMP1
	DAC	ITEMP1
	DAC	SEEPT		; also set seept for type 2 command
	JMP	@POSITION

TESTID:	0			; test for valid id in ininfo
	LAC	ININFO
	ASN			; also can't be zero
	 JMS	ERROR		; id zero or same as mybit
	SUB	[9.]		; can't be > or = to 9.
	ASP
	 JMP	TESTOK
	LAC	ININFO
	JMS	ERROR		; id greater than 8
TESTOK:	LAC	ININFO		; all ok so return with id in ac
	JMP	@TESTID

TESTLOC:0			; test to see if legal location
	AND	[77']		; minimum is location 1
	ASN
	 JMS	ERROR		; location zero
	SUB	[32.]
	ASP
	 JMP	.+3
	ADD	[32.]
	JMS	ERROR		; location greater than 31.
	ADD	[32.]
	JMP	@TESTLOC
;
;	error handling routine
;
ERROR:	0			; address of where the error was found
	DAC	ERRAC		; save ac error message
	LAC	IDSPTCH		; save dispatch address
	DAC	ERRDSP
	LWC	11.
	DAC	ICNT2		; now save info area
	LAC	[ININFO-1]
	DAC	17'
	LAC	[ERRINFO-1]
	DAC	16'
SVELOP:	LAC	@17'
	DAC	@16'
	ISZ	ICNT2
	 JMP	SVELOP
	ISZ	ERRCNT		; bump the error count
	 NOP
	LAC	ERRCNT		; now display it
	JMS	GETCHR
	DAC	@[ERRCHAR]
	JMP	EXIT		; now ignore bad message

ERRAC:	0			; saved ac
ERRDSP:	0			; saved dispatch address
ERRCNT:	60'			; error count

;
;	routines variables
;
INCHAR:	0			; last character read in
ICNT:	0			; the number of characters we are waiting for
ICNT2:	0			; general purpose counter used in routine
ITEMP1:	0			; temporary locations
ITEMP2:	0			; another temporary location
IDSPTCH:0			; dispatching address for command routines
RNGPT:	RINGST			; first character of ring buffer pointer
RNGPT2:	RINGST+1		; last character of ring buffer pointer
RINGLC:	-4			; ring buffer line counter
ININFO:	0			; input information from 10 buffer
	0
	0
	0
	0
	0
	0
	0
	0
	0
	0
;
;	constants go here at end of this 2k !!!!! any refs to or from
;	succeeding 2k must be indirect-address! bleah!!!!!! (klh)
;

	CONSTANTS

;loc 14000		;happens about here anyway, just needs precision.

;
;	distances to walls table
;
WALLS:	511.			; distances to walls
	450.
	358.
	281.
	225.
	184.
	155.
	133.
	116.
	103.
	92.
	83.
	75.
	70.
	64.
	60.
	56.
	53.
	50.
	47.
	45.
	43.
	41.
	39.
	37.
	35.
	33.
	31.
	29.
	27.
	25.
;
;	error saving of info information area
;
ERRINFO:0		; holds 2nd character of last bad message
	0		; holds the rest of the message
	0
	0
	0
	0
	0
	0
	0
	0
	0
;
;	n direction letter table
;	e
;	s
;	w
;
DIRLET:	116'
	105'
	123'
	127'
;
;	you were shot by: message
;
YWSB:	131'
	117'
	125'
	40'
	127'
	105'
	122'
	105'
	40'
	123'
	110'
	117'
	124'
	40'
	102'
	131'
	72'
;
;	eyes and arrows table
;
EYTAB:	DJMS	AWAY
	DJMS	TOLEFT
	DJMS	EYES
	DJMS	TORIGHT
;
;	offset for name table
;
CENTER:	DJMS	OFF6
	DJMS	OFF5
	DJMS	OFF4
	DJMS	OFF3
	DJMS	OFF2
	DJMS	OFF1
	DNOP
OFF6:	INC E,DM30
	INC DM30,100'
OFF5:	INC E,DM30
	INC DM20,100'
OFF4:	INC E,DM30
	INC DM30,100'
OFF3:	INC E,DM30
	INC DM20,100'
OFF2:	INC E,DM30
	INC DM30,100'
OFF1:	INC E,DM30
	INC DM20,140'
;
;	djmses to name labels routines
;
TNUM:	DJMS	IML1
	DJMS	IML2
	DJMS	IML3
	DJMS	IML4
	DJMS	IML5
	DJMS	IML6
	DJMS	IML7
	DJMS	IML8
;
;	big explosion info table
;
BIGX1INC:0
BIGY1INC:0
BIGX2INC:0
BIGY2INC:0
BIGX3INC:0
BIGY3INC:0
BIGX4INC:0
BIGY4INC:0
BIGX5INC:0
BIGY5INC:0
BIGX6INC:0
BIGY6INC:0
BIGX7INC:0
BIGY7INC:0
BIGX8INC:0
BIGY8INC:0
;
;	imlac information tables
;
DSPTCH:	IM1
	IM2
	IM3
	IM4
	IM5
	IM6
	IM7
	IM8

IM1:	0			; status word: -1 active, 1 dying, 0 not in game
	0			; direction
	0			; x location
	0			; y location
	0			; players score
	0			; bullet counter
	0			; my direction at time of fire
	0			; my x location at time of fire
	0			; my y location at time of fire
	0			; explosion timer
	0			; shot dead counter

IM2:	REPEAT 11., 0
IM3:	REPEAT 11., 0
IM4:	REPEAT 11., 0
IM5:	REPEAT 11., 0
IM6:	REPEAT 11., 0
IM7:	REPEAT 11., 0
IM8:	REPEAT 11., 0

;
;	test to see if player whose id is in iid is visible
;	seept should point to status word in info table
;	distan will contain distance to opponent on return if visible
;	skips if player seen
;
SEE:	0
	CLA
	DAC	DISTAN
	LAC	@[SEEPT]		; set up local seept
	DAC	SEEPT2
	ISZ	SEEPT2		; point to direction
	LAC	@SEEPT2
	DAC	IDIR		; save direction in idir
	ISZ	SEEPT2		; point to x location
	LAC	@SEEPT2
	DAC	IX		; save it in ix
	ISZ	SEEPT2
	LAC	@SEEPT2		; now get y loc
	DAC	IY
	LAC	SAVEDIR		; see which way we are pointing
	AND	[1]
	ASZ
	 JMP	WEAST		; west or east
SNORTH:	LAC	IX		; south or north	check his x to my x
	SAM	SAVEDX		; does it match?
	 JMP	@SEE		; no
	LAC	IY		; yes, now get the y difference
	SUB	SAVEDY
	ASN			; is he in my square?
	 JMP	@SEE		; yes, then i can't see him
	DAC	SEEPT2		; save distance to him
	ASP			; see if distance positive
	 JMP	HENORTH		; no, he must be north of me
	CIA			; yes, so he is south of me
	DAC	SEEPT2		; make distance negative
	JMP	HESOUTH

HEEAST:	LAW	2
HENORTH=HEEAST
	AND	SAVEDIR		; see if i am looking north
	ASZ			; if not then i can't see him
	 JMP	@SEE		; i look south so i can't see him
	JMP	CHKLN		; ok so far, now check length of hall

HESOUTH:LAW	2
HEWEST=HESOUTH
	AND	SAVEDIR		; see if i am looking south
	ASN			; if not then i can't see him
	 JMP	@SEE		; i no see him
	JMP	CHKLN		; so far so good, but check hallway length

WEAST:	LAC	IY		; check his y to my y
	SAM	SAVEDY		; it must match
	 JMP	@SEE		; can't see him
	LAC	IX		; now get the x difference
	SUB	SAVEDX
	ASN			; is he in my square?
	 JMP	@SEE		; yes, so i can't see him
	DAC	SEEPT2		; save the distance to him
	ASP			; but see if positive distance
	 JMP	HEWEST		; no, negative so he is west of me
	CIA
	DAC	SEEPT2
	JMP	HEEAST		; he is east of me

CHKLN:	LAC	SEEPT2
	CIA			; set distance to opponent
	DAC	DISTAN
CHKLN1:	LAW	1
	AND	SAVEDIR
	ASZ
	 JMP	CHKLN3
	JMS	CREM2
	ADD	SAVEDY
	DAC	SAVEDY
CHKLN2:	LAC	[MAZE]
	ADD	SAVEDY
	DAC	MPTR2
	LAC	SAVEDX
	ASZ
	 JMP	PT1
	LAC	[100000']
	JMP	PT2

PT1:	CIA
	DAC	MCNT
	CLL
	LAC	[100000']
	RAR	1
	ISZ	MCNT
	 JMP	.-2
PT2:	DAC	BIT2
	LAC	@MPTR2
	AND	BIT2		; see if it is an open square
	ASZ
	 JMP	@SEE
	ISZ	SEEPT2		; are we as far as the opponent?
	 JMP	CHKLN1		; no
	LAC	@[IID]		; yes, see if he is me
	SAM	@[MYBIT]
	 ISZ	SEE		; don't skip if so (can't see me)
	  JMP	@SEE
CHKLN3:	JMS	CREM2
	CIA
	ADD	SAVEDX
	DAC	SAVEDX
	JMP	CHKLN2

CREM2:	0
	LAC	SAVEDIR
	SAR	1
	AND	[1]
	ASN
	 LAC	[-1]
	JMP	@CREM2

DISTAN:	0
SAVEDIR:0
SAVEDX:	0
SAVEDY:	0
SEEPT2:	0
MCNT:	0
MPTR2:	0
IY:	0					; object id y location
IX:	0					; object id x location
IDIR:	0			; object id imlac direction
BIT2:	0

; chki20 -- routine to handle new-protocol checking and munching,
; as well as old.
; put here since no room in lower 2k of core.	

IFN FAST,[

CHKI20:	AND [7]			;get normalized id, no need to test range!
	IAC			;make it 1-8.
	DAC @[IID]			;store for what wants it.
	JMS @[POSITION]		;set up itemp1 and seept pointers into info tabs
	LAC @[ITEMP1]
	DAC CTEMP1		;get itemp1 into a var within our 2k.
	LAC @CTEMP1		;get current status
	ASZ
	 ASP			;ignore this msg if he's exploding
	  JMP .+2
	   JMP @[EXIT]
	STA
	DAC @CTEMP1		;say player is active
	LAC CTEMP1
	IAC
	DAC PLRD		;save ptr to direction
	IAC
	DAC PLRX		;save ptr to x coord
	IAC
	DAC PLRY		;save ptr to y coord
	DAC CTEMP1
	DAC @[ITEMP1]
			;itemp1 is now satisfactorily updated, and
			;indices into position tables done, now do function.
	LAC @[INCHAR]
	AND [70']		;only interested in function digit
	SAR 3
	ADD [JMP PLRVEC]
	DAC PLRJMP

PLRJMP:	0

PLRVEC:	JMP BADVEC
	JMP BADVEC
	JMP PLRTRN		; 2 - right turn
	JMP PLLTRN		; 3 - left turn
	JMP PLFLIP		; 4 - turn around
	JMP PLMOVE		; 5 - move forward
	JMP PLBACK		; 6 - move backward
BADVEC:	JMS @[ERROR]		; 7 - bad
	JMP @[EXIT]

PLRD:	0		;pointer to direction
PLRX:	0		;pointer to x coord
PLRY:	0		;guess what

PLRTRN:	LAC @PLRD	;get direction
	IAC		;right turn
	AND [3]
	DAC @PLRD
	JMP PLRDON

PLLTRN:	LAC @PLRD
	SUB [1]		;left turn
	AND [3]
	DAC @PLRD
	JMP PLRDON

PLFLIP:	LAC @PLRD
	ADD [2]		;turn right twice to turn-around
	AND [3]
	DAC @PLRD
	JMP PLRDON

PLBACK:	LAC @PLRD	;backward-- reverse direction then move.
	ADD [2]
	JMP .+2

PLMOVE:	LAC @PLRD
	AND [3]
	ADD [JMP PLDVEC]
	DAC PLMJMP

PLMJMP:	0

PLDVEC:	JMP PLMNOR	;north
	JMP PLMEA	;east
	JMP PLMSOU	;south
	JMP PLMWES	;west

PLMNOR:	LAC @PLRY
	SUB [1]		;decrement y coord for north moving
	JMS @[TESTLOC]
	DAC @PLRY
	JMP PLRDON

PLMEA:	LAC @PLRX
	IAC		;increment x coord for east
	JMS @[TESTLOC]
	DAC @PLRX
	JMP PLRDON

PLMSOU:	LAC @PLRY
	IAC		; incrment y coord for south
	JMS @[TESTLOC]
	DAC @PLRY
	JMP PLRDON

PLMWES:	LAC @PLRX
	SUB [1]		; decrement x coord for west
	JMS @[TESTLOC]
	DAC @PLRX
	JMP PLRDON

PLRDON:	LAC @[IID]	;get player id again
	DAC @[ININFO]	;and fake out stupid routine
	JMP @[CHK25]	;done with new ptcl handling.

CTEMP1:	0	;pointer substi. for itemp1
] ;end of ifn fast

			; high 2k constants
	CONSTANTS

;
;	name subroutines
;	5 character name
;
IML1:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM			; return jump
IML2:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM
IML3:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM
IML4:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM
IML5:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM
IML6:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM
IML7:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM
IML8:	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DJMS	D040
	DRJM

;
;	gsv character subroutines
;
CUR:	INC E,D0M1
	INC D0M3,B30
	INC B30,B30
	INC D03,D20
	INC D01,T
	DJMP DLIST
WAIT:	INC E,P			; 40 microsecond wait
	INC P,P
	INC P,P
	INC P,P
	INC P,P
	INC P,P
	INC P,P
	INC P,P
	INC P,P
	INC P,140
D010:	INC E,DM30
	INC DM30,DM30
	INC DM20,140'
D012:	INC E,D0M3 		; end_of_line
	INC D0M3,D0M3
	INC D0M3,D0M3
	INC D0M3,D0M3
	INC X,X
D015:	DLXA 200
	DJMS WAIT
	DRJM
DNL3:	DLXA	540
	DJMP	DNL+1
DNL2:	DLXA 1710
	DJMP .+2
DNL:	DLXA 10
	DJMS WAIT
	DJMP D012
D040:	INC E,D30 		; space
	INC D30,D30
	INC D20,X
EYES:	INC E,D03		; eyes
	INC D03,D03
	INC D03,DM33
	INC B00,B00
	INC D30,D30
	INC B00,B00
	INC DM30,D00
	INC D0M3,D0M3
	INC D0M3,D0M3
	INC D0M3,140'
CMZE:	INC E,B03
	INC B03,B03
	INC B03,B03
	INC B03,B02
	INC B30,B30
	INC B30,B10
	INC B0M3,B0M3
	INC B0M3,B0M3
	INC B0M3,B0M3
	INC B0M2,BM30
	INC BM30,BM30
	INC BM10,B12
	INC B12,B12
	INC B12,B12
	INC B12,B12
	INC B12,B12
	INC B12,DM30
	INC DM30,DM30
	INC DM10,B1M2
	INC B1M2,B1M2
	INC B1M2,B1M2
	INC B1M2,B1M2
	INC B1M2,B1M2
	INC B1M2,D10
	INC 140',140'
CHARMZE:DJMS CMZE
	DJMP CMZE
SPMAZE:	INC E,D30
	INC D30,D30
	INC D30,D30
	INC D30,D30
	INC D10,140'
ARROWS:	DJMS UPARR
	DJMS RIGHTARR
	DJMS DOWNARR
	DJMS LEFTARR
RIGHTARR:INC E,D33
	INC D03,D33
	INC B30,B30
	INC B30,B10
	INC BM2M2,B02
	INC B02,B2M2
	INC D3M3,D3M3
	INC D0M3,140'
LEFTARR:INC E,D33
	INC D03,D33
	INC B22,B0M2
	INC B0M2,BM22
	INC B30,B30
	INC B30,B10
	INC D3M3,D3M3
	INC D0M3,140'

UPARR:	INC E,D30
	INC D30,D30
	INC D23,B03
	INC B03,B03
	INC B01,BM2M2
	INC B20,B20
	INC BM22,D00
	INC D3M3,D3M3
	INC D3M3,D2M3
	INC D0M1,140'

DOWNARR:INC E,D30
	INC D30,D30
	INC D23,B12
	INC BM20,B1M2
	INC B03,B03
	INC B03,B01
	INC D3M3,D3M3
	INC D3M3,D2M3
	INC D0M1,140'

AWAY:	DLV D,0,20.
	DLV B,0,15.
	DLV B,-2,-5.
	DLV B,4.,0
	DLV B,-2.,5.
	DLV D,0,-35.
	DRJM

TOLEFT:	DLV D,0,20.
	DLV B,-15.,0
	DLV B,5.,2
	DLV B,0,-4.
	DLV B,-5.,2
	DLV D,15.,-20.
	DRJM

TORIGHT:DLV D,0,20.
	DLV B,15.,0
	DLV B,-5.,2.
	DLV B,0,-4.
	DLV B,5.,2.
	DLV D,-15.,-20.
	DRJM

;
;
;	big explosion display list
;
AD2:	DHVS	2
	DADR			; turn on 8k display addressing
	DLXA	500
	DLYA	1200
	DJMS	WAIT
;
;	you were shot by:
;
MESAGE:	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DJMS	DNOP
	DLXA	1000
	DLYA	1000
	DJMS	WAIT
;
;	djms to player who did the killing
;
WHODIDIT:DJMS	D040
	DSTS	3
BIGX1:	DLXA	1000
BIGY1:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
BIGX2:	DLXA	1000
BIGY2:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
BIGX3:	DLXA	1000
BIGY3:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
BIGX4:	DLXA	1000
BIGY4:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
BIGX5:	DLXA	1000
BIGY5:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
BIGX6:	DLXA	1000
BIGY6:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
BIGX7:	DLXA	1000
BIGY7:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
BIGX8:	DLXA	1000
BIGY8:	DLYA	1000
	DJMS	WAIT
	DNOP
	DNOP
	DNOP
	DJMS	EXPLOSIN+2
	DHLT

;
;	start of main display list
;
AD1:	DHVS	1
	DADR			; turn on 8k display addressing
				; (use 0 bit to indicate which 4k)
	DLXA	50
	DLYA	1300
	DJMS	WAIT
	DJMS	IML1
	DJMS	DNL
SCORE:	DNOP			; display names and scores here
	DNOP
	DNOP
	DNOP
	DJMS	DNL
	DNOP
	DNOP
	DNOP
	DNOP
	DLXA	50
	DLYA	1100
	DJMS	WAIT
	DJMS	IML2
	DJMS	DNL
	DNOP
	DNOP
	DNOP
	DNOP
	DJMS	DNL
	DNOP
	DNOP
	DNOP
	DNOP
	DLXA	50
	DLYA	700
	DJMS	WAIT
	DJMS	IML3
	DJMS	DNL
	DNOP
	DNOP
	DNOP
	DNOP
	DJMS	DNL
	DNOP
	DNOP
	DNOP
	DNOP
	DLXA	50
	DLYA	500
	DJMS	WAIT
	DJMS	IML4
	DJMS	DNL
	DNOP
	DNOP
	DNOP
	DNOP
	DJMS	DNL
	DNOP
	DNOP
	DNOP
	DNOP
	DLXA	1724
	DLYA	1300
	DJMS	WAIT
	DJMS	IML5
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DLXA	1724
	DLYA	1100
	DJMS	WAIT
	DJMS	IML6
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DLXA	1724
	DLYA	700
	DJMS	WAIT
	DJMS	IML7
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DLXA	1724
	DLYA	500
	DJMS	WAIT
	DJMS	IML8
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DJMS	DNL2
	DNOP
	DNOP
	DNOP
	DNOP
	DLYA	1720
;
;	status line
;
	DLXA	60
	DJMS	WAIT
IFE FAST,[
ORIG:	DJMS	D040	; origional id
	DJMS	D040
CURENT:	DJMS	D040	; current id
	DJMS	D040
]
DEAD:	DJMS	D040	; status of player
	DJMS	D040
ERRCHAR:DJMS	D040	; number of messages in error
;
;
;	n, s, e, or w letter
;
	DLXA	1000
	DJMS	WAIT
	DSTS	3
LETTER:	DJMS	D040
;
;	this is where the 8 possible players appear
;
;	dlxa 1000
;	dlya <position>
;	dsts <scale>
;	djms wait
;	djms <eyes or dnop>
;	djms <name or dnop or explosion>
;
	DLXA	1000
THING:	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
	DLXA	1000
	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
	DLXA	1000
	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
	DLXA	1000
	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
	DLXA	1000
	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
	DLXA	1000
	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
	DLXA	1000
	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
	DLXA	1000
	DJMS	D040
	DJMS	D040
	DJMS	WAIT
	DJMS	D040
	DJMS	D040
;
;	ring buffer
;
	DSTS	1
	DLXA	200
	DLYA	130
	DJMS	WAIT
RING:	DJMP	RINGST
RINGST:	DJMS	D012
	DJMP	CUR

	BLOCK	160.

RINGEND:DJMP	RINGST
;
;	display list for maze starts here
;
DLIST:	DHLT
;
;	return to console program after loading
;
	END LOADER
