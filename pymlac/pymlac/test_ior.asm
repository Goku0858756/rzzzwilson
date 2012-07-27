;;;;;;;;;;;;;;;;;;;;;;;;;
; check the IOR instruction
;;;;;;;;;;;;;;;;;;;;;;;;;
	org	00100
; first, simple IOR
	law	0	;
	ior	one	;
	sam	one	; 0 | 1 -> 1
	hlt		;
	law	1	;
	ior	zero	;
	sam	one	; 1 | 0 -> 1
	hlt		;
	lac	hbit	;
	ior	one	;
	sam	hbit1	; 0100000 | 1 -> 0100001
	hlt		;
; now some indirect IORs
	law	0	;
	ior	*indone	;
	sam	one	; 0 | 1 -> 1
	hlt		;
	law	1	;
	ior	*indzero;
	sam	one	; 1 | 0 -> 1
	hlt		;
	lac	hbit	;
	ior	*indone	;
	sam	hbit1	; 0100000 | 1 -> 0100001
	hlt		;
	hlt		;
; data for tests
zero	data	0	;
one	data	1	;
hbit	data	0100000	; just high bit
hbit1	data	0100001	; high bit plus 1
indzero	data	zero	;
indone	data	one	;
	end
