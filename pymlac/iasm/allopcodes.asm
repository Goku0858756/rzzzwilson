;-------------------------------
; Assembler source containing all IMLAC opcodes.
;-------------------------------
	org	0100		; 
start	law	03777		; 007777
	lwc	03777		; 107777
	jmp	03777		; 013777
	jmp	*03777		; 113777
	dac	03777		; 023777
	dac	*03777		; 123777
	xam	03777		; 027777
	xam	*03777		; 127777
	isz	03777		; 033777
	isz	*03777		; 133777
	jms	03777		; 037777
	jms	*03777		; 137777
	and	03777		; 047777
	and	*03777		; 147777
	ior	03777		; 053777
	ior	*03777		; 153777
	xor	03777		; 057777
	xor	*03777		; 157777
	lac	03777		; 053777
	lac	*03777		; 153777
	add	03777		; 067777
	add	*03777		; 167777
	sub	03777		; 073777
	sub	*03777		; 173777
	sam	03777		; 077777
	sam	*03777		; 177777
;-------------------------------
	hlt			; 000000
	hlt	00001		; 000001
	hlt	03777		; 003777
	nop			; 100000
	cla			; 100001
	cma			; 100002
	sta			; 100003
	iac			; 100004
	coa			; 100005
	cia			; 100006
	cll			; 100010
	cml			; 100020
	stl			; 100030
	oda			; 100040
	lda			; 100041
	cal			; 100011
;-------------------------------
	ral	0		; 003000
	ral	3		; 003003
	rar	0		; 003020
	rar	3		; 003023
	sal	0		; 003040
	sal	3		; 003043
	sar	0		; 003060
	sar	3		; 003063
	don			; 003100
;-------------------------------
	asz			; 002001
	asn			; 102001
	asp			; 002002
	asm			; 102002
	lsz			; 002004
	lsn			; 102004
	dsf			; 002010
	dsn			; 102010
	ksf			; 002020
	ksn			; 102020
	rsf			; 002040
	rsn			; 102040
	tsf			; 002100
	tsn			; 102100
	ssf			; 002200
	ssn			; 102200
	hsf			; 002400
	hsn			; 102400
;-------------------------------
	dla			; 001003
	ctb			; 001011
	dof			; 001012
	krb			; 001021
	kcf			; 001022
	krc			; 001023
	rrb			; 001031
	rcf			; 001032
	rrc			; 001033
	tpr			; 001041
	tcf			; 001042
	tpc			; 001043
	hrb			; 001051
	hof			; 001052
	hon			; 001061
	stb			; 001062
	scf			; 001071
	ios			; 001072
;-------------------------------
	iot	0101		; 001101
	iot	0111		; 001111
	iot	0131		; 001131
	iot	0132		; 001132
	iot	0134		; 001134
	iot	0141		; 001141
	iof			; 001161
	ion			; 001162
	pun			; 001271
	psf			; 001274
;-------------------------------
	dlxa	07777		; 017777
	dlya	07777		; 027777
;	deim	07777		; 037777
	djms	07777		; 057777
	djmp	07777		; 067777
;-------------------------------
	dopr	015		; 004015
	dopr	014		; 004014
	dhlt			; 000000
	dsts	0		; 004004
	dsts	1		; 004005
	dsts	2		; 004006
	dsts	3		; 004007
	dstb	0		; 004010
	dstb	1		; 004011
	drjm			; 004040
	dixm			; 005000
	diym			; 004400
	ddxm			; 004200
	ddym			; 004100
	dhvc			; 006000
	ddsp			; 004020
	dnop			; 004000
;-------------------------------
	end