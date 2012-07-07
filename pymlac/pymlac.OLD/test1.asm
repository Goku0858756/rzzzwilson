	org	00100
	law	1	; load AC with 1
	sam	one	; check it's actually 1
	hlt	01	;
	law	2	; load AC with 2
	sam	two	; check it's actually 2
	hlt	02	;
	lwc	0	; load AC with complement of 0
	sam	zero	; check -0 is 0
	hlt	03	;
	lwc	1	; load AC with complement of 1
	sam	minus1	; check -1 is 0177777
	hlt	04	;
	jmp	jmptest	;
	hlt	05	;
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
	hlt	06	;
	jms	jmstest	;
	lac	minus1	;
	and	one	;
	sam	one	;
	hlt	07	;
        law	0123	;
	ior	iortest	;
	sam	expior	;
	hlt	010	;
	law	0123	;
	xor	xortest	;
	sam	expxor	;
	hlt	011	;
	cla		;
	add	one	;
	sam	one	;
	hlt	012	;
	lac	minus1	;
	add	one	;
	sam	zero	;
	hlt	013	;
	cll		;
	cla		;
	iac		;
	sam	one	;
	hlt	014	;
	cma		;
	sam	minus2	;
	hlt	015	;
	sta		;
	sam	minus1	;
	hlt	016	;
	iac		;
	sam	zero	;
	hlt	017	;
	coa		;
	sam	one	;
	hlt	020	;
	cla		;
	cia		;
	sam	zero	;
	hlt	021	;
	cll		;
	cml		;
	law	1	;
	cal		;
	sam	zero	;
	hlt	022	;
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
