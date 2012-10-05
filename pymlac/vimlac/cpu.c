/******************************************************************************\
 *                               main_cpu.c                                   *
 *                              ------------                                  *
 *                                                                            *
 *  This file is used to decode and execute a main processor instruction.     *
 *                                                                            *
\******************************************************************************/

#include "vimlac.h"
#include "cpu.h"


/******
 * Emulated registers, state, memory, etc.
 ******/

static WORD            r_AC;
static WORD            r_L;
static WORD            r_PC;
static WORD            Prev_r_PC;
static WORD            r_DS;	/* data switches */

static int             CycleCounter;     /* number of cycles for the instruction */

/* 40Hz sync stuff */
static LONG            Sync40HzCycles;
static BOOL            Sync40HzOn;

/******
 * Emulated memory.
 ******/

static WORD            Memory[MEMSIZE];


/******
 * Environment stuff.  PTR and TTY in and out files, etc
 ******/

static BOOL            MainOn;           /* TRUE if main processor is running */


/******************************************************************************
Description : Functions to get various registers.
 Parameters : 
    Returns : 
   Comments : 
 ******************************************************************************/
WORD
cpu_get_AC(void)
{
    return r_AC;
}


WORD
cpu_get_L(void)
{
    return r_L;
}


WORD
cpu_get_PC(void)
{
    return r_PC;
}


/******************************************************************************
Description : Function to handle unrecognized instruction.
 Parameters : 
    Returns : 
   Comments : 
 ******************************************************************************/
static void
illegal(void)
{
    WORD oldPC = Prev_r_PC & MEMMASK;

    Log("INTERNAL ERROR: "
        "unexpected main processor opcode %06.6o at address %06.6o",
        Memory[oldPC], oldPC);

    memdump(LogOut, oldPC - 8, 16);

    error("INTERNAL ERROR: "
          "unexpected main processor opcode %06.6o at address %06.6o",
          Memory[oldPC], oldPC);
}


/******************************************************************************
Description : Emulate the IMLAC LAW/LWC instructions.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Load AC with immediate value.
 ******************************************************************************/
static void
i_LAW_LWC(WORD indirect, WORD address)
{
    // here 'indirect' selects between LWC and LAW
    if (indirect)
    {
        // LWC
        r_AC = (~address + 1) & WORDMASK;
        trace("LWC\t %5.5o", address);
    }
    else
    {
        // LAW
        r_AC = address;
        trace("LAW\t %5.5o", address);
    }

    ADDCYCLES(1);
}


/******************************************************************************
Description : Emulate the JMP instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : PC set to new address.
 ******************************************************************************/
static void
i_JMP(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    r_PC = newaddress;

    ADDCYCLES(indirect ? 3 :  2);
    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("JMP\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the DAC instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Deposit AC in MEM.
 ******************************************************************************/
static void
i_DAC(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    if (AddressWritable(newaddress))
        Memory[newaddress] = r_AC;

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("DAC\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC XAM instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Exchange AC with MEM.
 ******************************************************************************/
static void
i_XAM(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);
    WORD tmp;

    tmp = Memory[newaddress];
    if (AddressWritable(newaddress))
        Memory[newaddress] = r_AC;
    r_AC = tmp;

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("XAM\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the ISZ instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Increment MEM and skip if MEM == 0.
 ******************************************************************************/
static void
i_ISZ(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    if (AddressWritable(newaddress))
        Memory[newaddress] = ++Memory[newaddress] & WORDMASK;
    if (Memory[newaddress] == 0)
        r_PC = (r_PC + 1) & MEMMASK;

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("ISZ\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC JMS instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Store PC in MEM, jump to MEM + 1.
 ******************************************************************************/
static void
i_JMS(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    if (AddressWritable(newaddress))
        Memory[newaddress] = r_PC;
    r_PC = ++newaddress & MEMMASK;

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("JMS\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC AND instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : AND MEM with AC.
 ******************************************************************************/
static void
i_AND(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    r_AC = r_AC & Memory[newaddress];

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("AND\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC IOR instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Inclusive OR MEM with AC.
 ******************************************************************************/
static void
i_IOR(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    r_AC |= Memory[newaddress];

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("IOR\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC XOR instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : XOR AC and MEM.  LINK unchanged.
 ******************************************************************************/
static void
i_XOR(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    r_AC ^= Memory[newaddress];

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("XOR\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC LAC instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Load AC from MEM.
 ******************************************************************************/
static void
i_LAC(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    r_AC = Memory[newaddress];

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("LAC\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the ADD instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Add value at MEM to AC.
 ******************************************************************************/
static void
i_ADD(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    r_AC += Memory[newaddress];
    if (r_AC & OVERFLOWMASK)
        r_L = r_L ^ 1;
    r_AC = r_AC & WORDMASK;

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("ADD\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC SUB instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Subtract MEM from AC.  LINK complemented if carry.
 ******************************************************************************/
static void
i_SUB(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    r_AC -= Memory[newaddress];
    if (r_AC & OVERFLOWMASK)
        r_L = r_L ^ 1;
    r_AC = r_AC & WORDMASK;

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("SUB\t%c%5.5o", (indirect) ? '*' : ' ', address);
}


/******************************************************************************
Description : Emulate the IMLAC SAM instruction.
 Parameters : indirect - TRUE if address is indirect, FALSE if immediate
            : address  - the memory address
    Returns : 
   Comments : Skip if AC same as MEM.
 ******************************************************************************/
static void
i_SAM(WORD indirect, WORD address)
{
    WORD newaddress = GetEffAddress(indirect, address);

    if (r_AC == Memory[newaddress])
        r_PC = (r_PC + 1) & MEMMASK;

    if (indirect)
        ADDCYCLES(3);
    else
        ADDCYCLES(2);

    trace("SAM\t%c%5.5o", (indirect) ? '*' : ' ', address);
}

/******************************************************************************
Description : Emulate the DSF instruction.
 Parameters : 
    Returns : 
   Comments : Skip if display is ON.
 ******************************************************************************/
static void
i_DSF(void)
{
    if (DisplayOn != FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("DSF\t");
}


/******************************************************************************
Description : Emulate the IMLAC HRB instruction.
 Parameters : 
    Returns : 
   Comments : Read PTR value into AC.
            : If PTR motor off return 0.
            : If PTR motor on return byte from file.
 ******************************************************************************/
static void
i_HRB(void)
{
    if (PTR_isready())   /* get char from PTR file */
        r_AC = r_AC | PTR_getvalue();

    ADDCYCLES(1);

    trace("HRB\t");
}


/******************************************************************************
Description : Emulate the DSN instruction.
 Parameters : 
    Returns : 
   Comments : Skip if display is OFF.
 ******************************************************************************/
static void
i_DSN(void)
{
    if (DisplayOn == FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("DSN\t");
}


/******************************************************************************
Description : Emulate the IMLAC HSF instruction.
 Parameters : 
    Returns : 
   Comments : Skip if PTR has data.
   Comments : No data until cycle counter >= 'char ready' number.
 ******************************************************************************/
static void
i_HSF(void)
{
    if (PTR_isready() != FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("HSF\t");
}


/******************************************************************************
Description : Emulate the IMLAC HSN instruction.
 Parameters : 
    Returns : 
   Comments : Skip if PTR has no data.
            : There is no data until cycle counter >= 'char ready' number.
 ******************************************************************************/
static void
i_HSN(void)
{
    if (PTR_isready() == FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("HSN\t");
}


/******************************************************************************
Description : Emulate the IMLAC KCF instruction.
 Parameters : 
    Returns : 
   Comments : Clear the keyboard flag.
 ******************************************************************************/
static void
i_KCF(void)
{
    KB_clearflag();

    ADDCYCLES(1);

    trace("KCF\t");
}


/******************************************************************************
Description : Emulate the IMLAC KRB instruction.
 Parameters : 
    Returns : 
   Comments : Read a character from the keyboard into bits 5-15 of AC.
 ******************************************************************************/
static void
i_KRB(void)
{
    r_AC = r_AC | KB_getchar();

    ADDCYCLES(1);

    trace("KRB\t");
}


/******************************************************************************
Description : Emulate the IMLAC KRC instruction.
 Parameters : 
    Returns : 
   Comments : Combine the KCF and KRB instruction: Read keyboard and clear flag.
 ******************************************************************************/
static void
i_KRC(void)
{
    r_AC = r_AC | KB_getchar();
    KB_clearflag();

    ADDCYCLES(1);

    trace("KRC\t");
}


/******************************************************************************
Description : Emulate the IMLAC KSF instruction.
 Parameters : 
    Returns : 
   Comments : Skip if keyboard char available.
 ******************************************************************************/
static void
i_KSF(void)
{
    if (KB_isready() != FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("KSF\t");
}


/******************************************************************************
Description : Emulate the IMLAC instruction.
 Parameters : 
    Returns : 
   Comments : Skip if no keyboard char available.
 ******************************************************************************/
static void
i_KSN(void)
{
    if (KB_isready() == FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("KSN\t");
}


/******************************************************************************
Description : Emulate the IMLAC LDA instruction.
 Parameters : 
    Returns : 
   Comments : Load AC with value from data switches.
 ******************************************************************************/
static void
i_LDA(void)
{
    r_AC = r_DS;

    ADDCYCLES(1);

    trace("LDA\t");
}


/******************************************************************************
Description : Emulate the IMLAC ODA instruction.
 Parameters : 
    Returns : 
   Comments : OR data switches value into AC.
 ******************************************************************************/
static void
i_ODA(void)
{
    r_AC |= r_DS;

    ADDCYCLES(1);

    trace("ODA\t");
}


/******************************************************************************
Description : Emulate the IMLAC PSF instruction.
 Parameters : 
    Returns : 
   Comments : Skip if PTP ready.
 ******************************************************************************/
static void
i_PSF(void)
{
    if (PTPFilename == NULL)
        Log("PSF: No PTP output set up, can't do PSF!?");

    if (PTPCycleReady <= 0L)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("PSF\t");
}


/******************************************************************************
Description : Emulate the IMLAC PUN instruction.
 Parameters : 
    Returns : 
   Comments : Punch AC low byte to tape.
 ******************************************************************************/
static void
i_PUN(void)
{
    if (PTPFilename != NULL)
    {
        int value =  r_AC & 0xff;

        EmitPTP(value);
        PTPCycleReady = PTPCHAR_CYCLES;
    }
    else
        Log("PUN: No PTP file, can't punch '%c'", r_AC & 0xff);

    ADDCYCLES(1);

    trace("PUN\t");
}


/******************************************************************************
Description : Emulate the IMLAC RAL instruction.
 Parameters : shift - the number of bits to shift by [0,3]
    Returns : 
   Comments : Rotate AC+L left 'shift' bits.
 ******************************************************************************/
static void
i_RAL(int shift)
{
    int i;

    for (i = 0; i < shift; ++i)
    {
        WORD oldlink = r_L;

        r_L = (r_AC >> 15) & LOWBITMASK;
        r_AC = ((r_AC << 1) + oldlink) & WORDMASK;
    }

    ADDCYCLES(1);

    trace("RAL\t %d", shift);
}


/******************************************************************************
Description : Emulate the RAL instruction.
 Parameters : shift - number of bits to rotate [0,3]
    Returns : 
   Comments : Rotate right AC+L 'shift' bits.
 ******************************************************************************/
static void
i_RAR(int shift)
{
    int i;

    for (i = 0; i < shift; ++i)
    {
        WORD oldlink = r_L;

        r_L = r_AC & LOWBITMASK;
        r_AC = ((r_AC >> 1) | (oldlink << 15)) & WORDMASK;
    }

    ADDCYCLES(1);

    trace("RAR\t %d", shift);
}


/******************************************************************************
Description : Emulate the IMLAC RCF instruction.
 Parameters : 
    Returns : 
   Comments : Clear the TTY buffer flag.
 ******************************************************************************/
static void
i_RCF(void)
{
    TTYIN_resetflag();

    ADDCYCLES(1);

    trace("RCF\t");
}


/******************************************************************************
Description : Emulate the IMLAC RRB instruction.
 Parameters : 
    Returns : 
   Comments : Read a character from the TTY into bits 5-15 of AC.
 ******************************************************************************/
static void
i_RRB(void)
{
    r_AC = r_AC | TTYIN_getvalue();

    ADDCYCLES(1);

    trace("RRB\t");
}


/******************************************************************************
Description : Emulate the IMLAC RRC instruction.
 Parameters : 
    Returns : 
   Comments : Read a character from the TTY and clear buffer flag.
 ******************************************************************************/
static void
i_RRC(void)
{
    r_AC = r_AC | TTYIN_getvalue();
    TTYIN_resetflag();

    ADDCYCLES(1);

    trace("RRC\t");
}


/******************************************************************************
Description : Emulate the IMLAC RSF instruction.
 Parameters : 
    Returns : 
   Comments : Skip if TTY char available.
 ******************************************************************************/
static void
i_RSF(void)
{
    if (TTYIN_isready())
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("RSF\t");
}


/******************************************************************************
Description : Emulate the IMLAC RSN instruction.
 Parameters : 
    Returns : 
   Comments : Skip if no TTY char available.
 ******************************************************************************/
static void
i_RSN(void)
{
    if (! TTYIN_isready())
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("RSN\t");
}


/******************************************************************************
Description : Emulate the IMLAC SAL instruction.
 Parameters : shift - the number of bits to shift by
    Returns : 
   Comments : Shift AC left n places.  LINK unchanged.
 ******************************************************************************/
static void
i_SAL(int shift)
{
    WORD oldbit0 = r_AC & HIGHBITMASK;

    r_AC = (((r_AC << shift) & ~HIGHBITMASK) | oldbit0) & WORDMASK;

    ADDCYCLES(1);

    trace("SAL\t %d", shift);
}


/******************************************************************************
Description : Emulate the IMLAC SAR instruction.
 Parameters : shift - the number of bits to shift by
    Returns : 
   Comments : Shift AC right n places.
 ******************************************************************************/
static void
i_SAR(int shift)
{
    int i;

    for (i = shift; i > 0; --i)
    {
        WORD oldbit0 = r_AC & HIGHBITMASK;

        r_AC = ((r_AC >> 1) | oldbit0) & WORDMASK;
    }

    ADDCYCLES(1);

    trace("SAR\t %d", shift);
}


/******************************************************************************
Description : Emulate the IMLAC SSF instruction.
 Parameters : 
    Returns : 
   Comments : Skip if 40Hz sync flip-flop is set.
 ******************************************************************************/
static void
i_SSF(void)
{
    if (Sync40HzOn != FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("SSF\t");
}


/******************************************************************************
Description : Emulate the IMLAC SSN instruction.
 Parameters : 
    Returns : 
   Comments : Skip if 40Hz sync flip-flop is NOT set.
 ******************************************************************************/
static void
i_SSN(void)
{
    if (Sync40HzOn == FALSE)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("SSN\t");
}


/******************************************************************************
Description : Emulate the IMLAC TCF instruction.
 Parameters : 
    Returns : 
   Comments : Reset the TTY "output done" flag.
 ******************************************************************************/
static void
i_TCF(void)
{
    TTYoutOutputReady = TRUE;

    ADDCYCLES(1);

    trace("TCF\t");
}


/******************************************************************************
Description : Emulate the IMLAC TPC instruction.
 Parameters : 
    Returns : 
   Comments : Transmit char in AC and clear TTY ready flag
 ******************************************************************************/
static void
i_TPC(void)
{
    if (TTYoutFilename != NULL)
    {
        int value = r_AC & 0xff;

        EmitTTY(value);
        TTYoutCycleReady += TTYOUTCHAR_CYCLES;
    }
    else
        Log("TPC: No TTY file, can't emit '%c'", r_AC & 0xff);

    TTYoutOutputReady = FALSE;

    ADDCYCLES(1);

    trace("TPC\t");
}


/******************************************************************************
Description : Emulate the IMLAC TPR instruction.
 Parameters : 
    Returns : 
   Comments : Send low byte in AC to TTY output.
 ******************************************************************************/
static void
i_TPR(void)
{
    if (TTYoutFilename != NULL)
    {
        int value = r_AC & 0xff;

        EmitTTY(value);
        TTYoutCycleReady += TTYOUTCHAR_CYCLES;
    }
    else
        Log("TPR: No TTY file, can't emit '%c'", r_AC & 0xff);

    ADDCYCLES(1);

    trace("TPR\t");
}


/******************************************************************************
Description : Emulate the IMLAC TSF instruction.
 Parameters : 
    Returns : 
   Comments : Skip if TTY done sending
 ******************************************************************************/
static void
i_TSF(void)
{
    if (TTYoutFilename == NULL)
        Log("TSF: No TTY output set up, can't do TSF!?");

    if (TTYoutCycleReady <= 0L)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("TSF\t");
}


/******************************************************************************
Description : Emulate the IMLAC TSN instruction.
 Parameters : 
    Returns : 
   Comments : Skip if TTY not done sending
 ******************************************************************************/
static void
i_TSN(void)
{
    if (TTYoutFilename == NULL)
        Log("TSN: No TTY output set up, can't do TSN!?");

    if (TTYoutCycleReady > 0L)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("TSN\t");
}


/******************************************************************************
Description : Emulate the ASZ instruction.
 Parameters : 
    Returns : 
   Comments : Skip if AC == 0.
 ******************************************************************************/
static void
i_ASZ(void)
{
    if (r_AC == 0)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("ASZ\t");
}


/******************************************************************************
Description : Emulate the ASN instruction.
 Parameters : 
    Returns : 
   Comments : Skip if AC != 0.
 ******************************************************************************/
static void
i_ASN(void)
{
    if (r_AC != 0)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("ASN\t");
}


/******************************************************************************
Description : Emulate the IMLAC ASP instruction.
 Parameters : 
    Returns : 
   Comments : Skip if AC is positive.
 ******************************************************************************/
static void
i_ASP(void)
{
    if ((r_AC & HIGHBITMASK) == 0)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("ASP\t");
}


/******************************************************************************
Description : Emulate the LSZ instruction.
 Parameters : 
    Returns : 
   Comments : Skip if LINK is zero.
 ******************************************************************************/
static void
i_LSZ(void)
{
    if (r_L == 0)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("LSZ\t");
}


/******************************************************************************
Description : Emulate the IMLAC ASM instruction.
 Parameters : 
    Returns : 
   Comments : Skip if AC is negative.
 ******************************************************************************/
static void
i_ASM(void)
{
    if (r_AC & HIGHBITMASK)
        r_PC = (r_PC + 1) & MEMMASK;

    ADDCYCLES(1);

    trace("ASM\t");
}


/******************************************************************************
Description : Emulate the IMLAC DON instruction.
 Parameters : 
    Returns : 
   Comments : Turn the display processor on.
 ******************************************************************************/
static void
i_DON(void)
{
    dcpu_set_drsindex(0);
    dcpu_start();

    ADDCYCLES(1);

    trace("DON\t");
}


/******************************************************************************
Description : Decode the 'microcode' instructions.
 Parameters : instruction - the complete instruction word
    Returns : 
   Comments : 
 ******************************************************************************/
static void
microcode(WORD instruction)
{
    WORD  newac;

    // T1
    if (instruction & 001)
        r_AC = 0;
    if (instruction & 010)
        r_L = 0;

    // T2
    if (instruction & 002)
        r_AC = (~r_AC) & WORDMASK;
    if (instruction & 020)
        r_L = (~r_L) & 01;

    // T3
    if (instruction & 004)
        newac = r_AC + 1;
        if (newac & OVERFLOWMASK)
            r_L = (~r_L) & 01;
        r_AC = newac & WORDMASK;
    if (instruction & 040)
        r_AC |= r_DS;
        r_L = (~r_L) & 1;

    // do some sort of trace
//    combine = []
//    opcode = micro_opcodes.get(instruction, None)
//    if opcode:
//        combine.append(opcode)

    if ((instruction & 0100000) == 0)
        // bit 0 is clear, it's HLT
        MainOn == FALSE;
//    else:
//        for (k, op) in micro_singles.items():
//            if instruction & k:
//                combine.append(op)

    ADDCYCLES(1);
}


/******************************************************************************
Description : Further decode the initial '02' opcode instruction.
 Parameters : instruction - the complete instruction word
    Returns : 
   Comments : 
 ******************************************************************************/
static void
page02(WORD instruction)
{
    switch (instruction)
    {
        case 0002001: i_ASZ(); break;
        case 0102001: i_ASN(); break;
        case 0002002: i_ASP(); break;
        case 0102002: i_ASM(); break;
        case 0002004: i_LSZ(); break;
        case 0102004: i_LSN(); break;
        case 0002010: i_DSF(); break;
        case 0102010: i_DSN(); break;
        case 0002020: i_KSF(); break;
        case 0102020: i_KSN(); break;
        case 0002040: i_RSF(); break;
        case 0102040: i_RSN(); break;
        case 0002100: i_TSF(); break;
        case 0102100: i_TSN(); break;
        case 0002200: i_SSF(); break;
        case 0102200: i_SSN(); break;
        case 0002400: i_HSF(); break;
        case 0102400: i_HSN(); break;
        default:      illegal();
    }
}


/******************************************************************************
Description : Further decode the initial '00' opcode instruction.
 Parameters : instruction - the complete instruction word
    Returns : 
   Comments : 
 ******************************************************************************/
static void
page00(WORD instruction)
{
/******
 * Pick out microcode or page 2 instructions.
 ******/

    if ((instruction & 0077700) == 000000)
        microcode(instruction);

    if ((instruction & 0077000) == 002000)
        page02(instruction);

/******
 * Decode a page 00 instruction
 ******/

    switch (instruction)
    {
        case 001003: i_DLA(); break;
        case 001011: i_CTB(); break;
        case 001012: i_DOF(); break;
        case 001021: i_KRB(); break;
        case 001022: i_KCF(); break;
        case 001023: i_KRC(); break;
        case 001031: i_RRB(); break;
        case 001032: i_RCF(); break;
        case 001033: i_RRC(); break;
        case 001041: i_TPR(); break;
        case 001042: i_TCF(); break;
        case 001043: i_TPC(); break;
        case 001051: i_HRB(); break;
        case 001052: i_HOF(); break;
        case 001061: i_HON(); break;
        case 001062: i_STB(); break;
        case 001071: i_SCF(); break;
        case 001072: i_IOS(); break;
        case 001101: i_IOT101(); break;
        case 001111: i_IOT111(); break;
        case 001131: i_IOT131(); break;
        case 001132: i_IOT132(); break;
        case 001134: i_IOT134(); break;
        case 001141: i_IOT141(); break;
        case 001161: i_IOF(); break;
        case 001162: i_ION(); break;
        case 001271: i_PUN(); break;
        case 001274: i_PSF(); break;
        case 003001: i_RAL1(); break;
        case 003002: i_RAL2(); break;
        case 003003: i_RAL3(); break;
        case 003021: i_RAR1(); break;
        case 003022: i_RAR2(); break;
        case 003023: i_RAR3(); break;
        case 003041: i_SAL1(); break;
        case 003042: i_SAL2(); break;
        case 003043: i_SAL3(); break;
        case 003061: i_SAR1(); break;
        case 003062: i_SAR2(); break;
        case 003063: i_SAR3(); break;
        case 003100: i_DON(); break;
	default:
	    illegal();
    }
}


/******************************************************************************
Description : Function to execute one main processor instruction.
 Parameters : 
    Returns : 
   Comments : Perform initial decode of 5 bit opcode and either call
            : appropriate emulating function or call further decode function.
 ******************************************************************************/
void
cpu_execute_one(void)
{
    WORD instruction;
    WORD indirect;
    WORD opcode;
    WORD address;

/******
 * If main processor not running, return immediately.
 ******/

    if (MainOn == FALSE)
        return;

/******
 * If interrupt pending, force JMS 0.
 ******/

#ifdef JUNK
    if (InterruptsEnabled && (InterruptWait <= 0) && InterruptsPending)
    {
        InterruptsEnabled = FALSE;
        i_JMS(FALSE, 0);
        return;
    }
#endif

/******
 * Fetch the instruction.  Split into initial opcode and address.
 ******/

    Prev_r_PC = r_PC;
    instruction = Memory[r_PC++];
    r_PC = r_PC & MEMMASK;

    indirect = (instruction & 0100000);		/* high bit */
    opcode = (instruction >> 11) & 017;		/* high 5 bits */
    address = instruction & 03777;		/* low 11 bits */

/******
 * Now decode it.
 ******/

    switch (opcode)
    {
        case 000:
            page00(instruction);
            break;
        case 001:				/* LAW/LWC n */
            i_LAW_LWC(indirect, address);
            break;
        case 002:				/* JMP q */
            i_JMP(indirect, address);
            break;
        case 003:
            illegal();
            break;
        case 004:				/* DAC q */
            i_DAC(indirect, address);
            break;
        case 005:				/* XAM q */
            i_XAM(indirect, address);
            break;
        case 006:				/* ISZ q */
            i_ISZ(indirect, address);
            break;
        case 007:				/* JMS q */
            i_JMS(indirect, address);
            break;
        case 010:
            illegal();
            break;
        case 011:				/* AND q */
            i_AND(indirect, address);
            break;
        case 012:				/* IOR q */
            i_IOR(indirect, address);
            break;
        case 013:				/* XOR q */
            i_XOR(indirect, address);
            break;
        case 014:				/* LAC q */
            i_LAC(indirect, address);
            break;
        case 015:				/* ADD q */
            i_ADD(indirect, address);
            break;
        case 016:				/* SUB q */
            i_SUB(indirect, address);
            break;
        case 017:				/* SAM q */
            i_SAM(indirect, address);
            break;
    }
}


/******************************************************************************
Description : Function to start the main CPU.
 Parameters : 
    Returns : 
   Comments : 
 ******************************************************************************/
void
cpu_start(void)
{
    MainOn = TRUE;
}


