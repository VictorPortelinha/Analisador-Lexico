.global _start

.data

SOMA: .word 0

.text
_start:

    @ Linha 1
    LDR r0, =3
    PUSH {r0}
    LDR r0, =2
    PUSH {r0}
    POP {r1}
    POP {r0}
    ADD r0, r0, r1
    PUSH {r0}

    @ Linha 2
    LDR r0, =10
    PUSH {r0}
    LDR r0, =4
    PUSH {r0}
    POP {r1}
    POP {r0}
    SUB r0, r0, r1
    PUSH {r0}

    @ Linha 3
    LDR r0, =7
    PUSH {r0}
    LDR r0, =3
    PUSH {r0}
    POP {r1}
    POP {r0}
    MUL r0, r0, r1
    PUSH {r0}

    @ Linha 4
    LDR r0, =15
    PUSH {r0}
    LDR r0, =4
    PUSH {r0}
    POP {r1}
    POP {r0}
    MOV r2, #0
div_loop_0:
    CMP r0, r1
    BLT div_end_0
    SUB r0, r0, r1
    ADD r2, r2, #1
    B div_loop_0
div_end_0:
    MOV r0, r2
    PUSH {r0}

    @ Linha 5
    LDR r0, =17
    PUSH {r0}
    LDR r0, =5
    PUSH {r0}
    POP {r1}
    POP {r0}
    MOV r2, #0
div_loop_1:
    CMP r0, r1
    BLT div_end_1
    SUB r0, r0, r1
    ADD r2, r2, #1
    B div_loop_1
div_end_1:
    MOV r0, r2
    PUSH {r0}

    @ Linha 6
    LDR r0, =17
    PUSH {r0}
    LDR r0, =5
    PUSH {r0}
    POP {r1}
    POP {r0}
mod_loop_2:
    CMP r0, r1
    BLT mod_end_2
    SUB r0, r0, r1
    B mod_loop_2
mod_end_2:
    PUSH {r0}

    @ Linha 7
    LDR r0, =2
    PUSH {r0}
    LDR r0, =8
    PUSH {r0}
    POP {r1}
    POP {r0}
    MOV r2, #1
pow_loop_3:
    CMP r1, #0
    BEQ pow_end_3
    MUL r2, r2, r0
    SUB r1, r1, #1
    B pow_loop_3
pow_end_3:
    PUSH {r2}

    @ Linha 8
    LDR r0, =10
    PUSH {r0}
    LDR r0, =SOMA
    LDR r0, [r0]
    PUSH {r0}

    @ Linha 9
    LDR r0, =SOMA
    LDR r0, [r0]
    PUSH {r0}

    @ Linha 10
    LDR r0, =3
    PUSH {r0}
    LDR r0, =2
    PUSH {r0}
    POP {r1}
    POP {r0}
    MUL r0, r0, r1
    PUSH {r0}
    LDR r0, =4
    PUSH {r0}
    LDR r0, =5
    PUSH {r0}
    POP {r1}
    POP {r0}
    ADD r0, r0, r1
    PUSH {r0}
    POP {r1}
    POP {r0}
    MOV r2, #0
div_loop_4:
    CMP r0, r1
    BLT div_end_4
    SUB r0, r0, r1
    ADD r2, r2, #1
    B div_loop_4
div_end_4:
    MOV r0, r2
    PUSH {r0}

    @ Linha 11
    LDR r0, =1
    PUSH {r0}
    LDR r0, =2
    PUSH {r0}
    POP {r1}
    POP {r0}
    ADD r0, r0, r1
    PUSH {r0}
    LDR r0, =3
    PUSH {r0}
    LDR r0, =2
    PUSH {r0}
    POP {r1}
    POP {r0}
    MUL r0, r0, r1
    PUSH {r0}
    POP {r1}
    POP {r0}
    SUB r0, r0, r1
    PUSH {r0}

    @ Linha 12
    LDR r0, =1
    PUSH {r0}
    @ RES - duplica topo da pilha
    POP {r0}
    PUSH {r0}
    PUSH {r0}

    POP {r0}
end:
    B end
