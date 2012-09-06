;;;;;;;;;;;;;;;;;;;;;;;;;
; test ISZ instruction
;;;;;;;;;;;;;;;;;;;;;;;;;
	org	00100
; check simple ISZ
	lwc	2	; put -2 into ISZ target
	dac	isztest	;
	law	0	; set skpflg = 0
	dac	skpflg	;
	law	1	; if no skip, 1 -> skpflg
	isz	isztest	; first ISZ, no skip
	dac	skpflg	; if no skip, store 1 to skpflg
	lac	skpflg	; check we didn't skip
	sam	one	; skpflg should be 1 = no skip
	hlt		;
	law	0	; set up skpflg
	dac	skpflg	;
	law	1	; if skip, no 1 -> skpflg
	isz	isztest	; second ISZ, skip
	dac	skpflg	; if no skip, store 1 to skpflg
	lac	skpflg	; check we didn't skip
	sam	zero	; skpflg should be 0 = skip
	hlt		;
; check indirect ISZ
	lwc	2	; put -2 into ISZ target
	dac	isztest	;
	law	0	; set skpflg = 0
	dac	skpflg	;
	law	1	; if no skip, 1 -> skpflg
	isz	*indisz	; first ISZ, no skip
	dac	skpflg	; if no skip, store 1 to skpflg
	lac	skpflg	; check we didn't skip
	sam	one	; skpflg should be 1 = no skip
	hlt		;
	law	0	; set up skpflg
	dac	skpflg	;
	law	1	; if skip, no 1 -> skpflg
	isz	*indisz	; second ISZ, skip
	dac	skpflg	; if no skip, store 1 to skpflg
	lac	skpflg	; check we didn't skip
	sam	zero	; skpflg should be 0 = skip
	hlt		;
	hlt		;
; data for tests
skpflg	data	0	;
isztest	data	0	;
zero	data	0	;
one	data	1	;
indisz	data	isztest	;
	end
