/******************************************************************************\
 *                                  cpu.h                                     *
 *                                 -------                                    *
\******************************************************************************/

#ifndef CPU_H
#define CPU_H

/******
 * Exported functions.
 ******/

void cpu_start(void);
void cpu_stop(void);
void cpu_execute_one(void);
WORD cpu_get_AC(void)
WORD cpu_get_L(void)
WORD cpu_get_PC(void)


#endif
