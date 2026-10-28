# Independent angular-momentum control of the P0 dimer source

For two physical spin-two systems, J=S1+S2 decomposes into J=0,1,2,3,4,
with multiplicities1,3,5,7,9. For H=3S1 dot S2, beta_eff=1, the energies
are E_J=(-18,-15,-9,0,12). Put M=Sz1+Sz2, D=Sz1-Sz2.

D is a vector under J, so it connects only J' in{J-1,J,J+1}. This is the
standard vector selection rule, explicitly stated at printed p.3 of
[MIT's Wigner-Eckart notes](https://ocw.mit.edu/courses/5-73-quantum-mechanics-i-fall-2018/2d6852b352732a9b75832477a364e993_MIT5_73F18_Lec27.pdf).
Exchange parity(-1)^J and exchange-odd D remove its same-J block. Isotropy
and D_vector²=24-J² give

    Tr[P_J D²]=(2J+1)[24-J(J+1)]/3.

Thus the adjacent transition traces W_J=Tr[P_J D P_(J+1)D] obey
W_(J-1)+W_J=(2J+1)[24-J(J+1)]/3, with zero endpoint weights. The exact
solution is W=(8,14,16,12).

Let L(a,b)=(a-b)/(log a-log b), continuously L(a,a)=a. Then

    C_DD=2 sum_(J=0)^3 W_J L(exp(-E_J),exp(-E_(J+1))),
    C_MM=2exp15+10exp9+28+60exp(-12),
    C_LR=(C_MM-C_DD)/4
        =-4exp18/3+2exp15/3+25exp9/9+133/18+31exp(-12)/2.

This formula is for the specified effective beta1 and coupling3; changing
temperature requires changing the logarithmic means, not merely replacing
the exponential arguments in the last already-specialized expression.

Root's independent rational exponential enclosure gives
C_LR approximately-85344764.64600967 with absolute interval width below
8.748e-20. It lies inside the generic dyadic certificate and overlaps the
separate exact-projector control. The partition trace formula
exp18+3exp15+5exp9+7+9exp(-12) also passes. The P0 source is -C_LR, with
no Gibbs quotient or extra beta or factor5. This controls one actual
25-state component; it acquires no later connected thermal input.
