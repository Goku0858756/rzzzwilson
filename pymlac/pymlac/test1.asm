	org	00100
	law	1	; load AC with 1
	sam	one	; check it's actually 1
	hlt		;
	law	2	; load AC with 2
	sam	two	; check it's actually 2
	hlt		;
	lwc	0	; load AC with complement of 0
	sam	zero	; check -0 is 0
	hlt		;
	lwc	1	; load AC with complement of 1
	sam	minus1	; check -1 is 0177777
	hlt		;
	jmp	jmptest	;
	hlt		;
jmptest	dac	dactest	; store AC (0177777)
	cla		; clear AC
	lac	dactest	; did we store -1?
	cla		;
	xam	dactest ; exchange AC with dactest get -1
	lac     dactest ; dactest should now be 0
	lac	isztest	;
	isz	isztest	; no skip first time
	nop		;
	lac	isztest	;
	isz	isztest	; should skip this time
	hlt		;
	jms	jmstest	;
	lac	minus1	;
	and	one	;
	sam	one	;
	hlt		;
        law	0123	;
	ior	iortest	;
	sam	expior	;
	hlt		;
	law	0123	;
	xor	xortest	;
	sam	expxor	;
	hlt		;
	cla		;
	add	one	;
	sam	one	;
	hlt		;
	lac	minus1	;
	add	one	;
	sam	zero	;
	hlt		;
	cll		;
	cla		;
	iac		;
	sam	one	;
	hlt		;
	cma		;
	sam	minus2	;
	hlt		;
	sta		;
	sam	minus1	;
	hlt		;
	iac		;
	sam	zero	;
	hlt		;
	coa		;
	sam	one	;
	hlt		;
	cla		;
	cia		;
	sam	zero	;
	hlt		;
	cll		;
	cml		;
	law	1	;
	cal		;
	sam	zero	;
	hlt		;
	stl		;
	hlt 		;
			;
jmstest	data	0	;
	nop		;
	jmp	*jmstest;
			;
dactest	data	0	;
zero	data	0	;
one	data	1	;
two	data	2	;
minus1	data	0177777	;
minus2	data	0177776	;
isztest	data	0177776	;
iortest	data	0157	;
xortest	data	0734	;
expior	data	0177	;
expxor	data	0617	;
	end
