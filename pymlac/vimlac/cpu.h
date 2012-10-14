/******************************************************************************\
 *                                  cpu.h                                     *
 *                                 -------                                    *
\******************************************************************************/

#ifndef CPU_H
#define CPU_H

#include "vimlac.h"

/******
 * Exported functions.
 ******/

void cpu_start(void);
void cpu_stop(void);
int cpu_execute_one(void);
WORD cpu_get_AC(void);
WORD cpu_get_L(void);
WORD cpu_get_PC(void);
void cpu_set_PC(WORD pc);


#endif
