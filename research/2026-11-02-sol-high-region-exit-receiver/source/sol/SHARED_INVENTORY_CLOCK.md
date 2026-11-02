# A global shared-inventory clock for every normal cell

Author derivation continuing the preserved subgeometric packet. This is a global clock/occupation operation for the entire normal-cell family, including large pair differences and signed packet states. It does not by itself prove the global return drift or unrestricted recurrence.

## 1. Conserved variables and the structural restriction exposed

For the raw two-block/coupling diagnostic use the exact normal cell

    x(i,j,k)=rho+k(0,-2,-2,0,2,2)+y_i+z_j,
    i,j in {0,1,2,3}, x>=0.

Residual anchors are zero. Residual hidden differences r=rho_B-rho_C and s=rho_E-rho_F and total n=|rho| are invariant under every normal channel. The additional useful invariant is

    T=min(rho_B,rho_C)+min(rho_E,rho_F)
       =(n-|r|-|s|)/2.                                   (H1)

It is unchanged by each core transfer, even for signed residuals. The permitted packet buffers imply T>=-4. When a phase00 state is feasible its residual is nonnegative and T>=0. A normal cell has O(1+T_+) fiber locations, despite arbitrarily large n,r,s. This is the correct size parameter for the degenerate large-difference faces.

The normal reference mu=2^k/[alpha_i beta_j x!] and all genuine unexpected killing hazards h are exactly those proved in the preserved BALANCED_NORMAL_CELL_PHYSICAL_EPISODE.md. No stationary entrance or mixing estimate is used.

## 2. Forward killing mean depends on T, not total population

At any off00 state, the mean time until killing or phase00 is <=1/h0, h0=min(alpha_0,beta_0), because at least one own zero-source channel is unexpected. This is true in the full cell, including signed residual boundaries. If phase00 is never reached it already proves the desired bound.

At a genuine phase00 return, choose the I normal input, which has a fixed positive probability alpha_0/(alpha_0+beta_0). Its residual b,c is nonnegative. Put t=min(b,c)<=T.

* If b<=c, the physical phase10 has B=b+1<=T+1. The total rate there is alpha_1(b+1)+alpha_0+beta_0. The conservative pair is disabled because D=0. Thus an immediate unexpected own zero-source event has probability >=c/(T+1).
* If b>c, first take the actual normal I1 step. Its probability at phase10 is bounded below by a positive raw constant, since its rate alpha_1(b+1) is at least alpha_1 and its only competitors have constant rates. At phase20, the normal rate is 2alpha_2(b+1)(c+1), the killing rate is alpha_0+2alpha_1(b+1), and peer input is beta_0. Since c<=T, killing at this point has probability >=c'/(T+1).

Consequently every actual phase00 excursion kills with probability >=c/(T+1), before any core activation on the displayed successful path. Its physical mean is bounded by a raw constant: the phase00 holding mean plus the off00 bound. Geometric renewal, retaining all other paths, gives

    sup_x E_x sigma <= C(1+T_+).                         (H2)

This bounds the ACTUAL first-unexpected-source clock from every normal-cell state. The cell is finite for each input, so a.s. finite physical absorption also has finitely many genuine jumps a.s.; expected activity is not the universal contract.

## 3. The adjoint has the SAME shared-inventory clock

The derived reverse normal process follows phase i->i-1 at rate alpha_i(x)_y_i, and similarly for II; the core is unchanged. It has the SAME killing h. Off00 its killed mean is again <=1/h0.

From phase00 choose the reverse I input into30, with fixed positive probability. While D=0 there are no core jumps. Exact nested factorial ratios bound the probability of the reverse normal transition30->20 below by a positive raw constant, uniformly in b,c: all lower-source and peer-zero competitors are bounded multiples of the normal phase3 rate.

If b>c, kill at20 with probability >=c/(T+1), as above. If b<=c, take the reverse normal step20->10, whose probability is again bounded below by a raw constant using exact source divisibility. Then kill at10 with probability >=c/(T+1). Thus geometric renewal gives

    sup_x E_x sigma* <= C_*(1+T_+).                      (H3)

There is no gap premise, asymptotic stationary approximation or growing head. All successful paths contain at most three genuine adjoint phase transitions at D=0, and every other path is paid by the killed off00 time.

## 4. Actual occupation consequence and unsolved sign

Let G=(-Q+diag h)^(-1) and G* its mu-adjoint. The finite exact identity gives

    mu(i)G(i,j)=mu(j)G*(j,i),
    G(i,j)<=C_*(1+T_+) mu(j)/mu(i).                       (H4)

This improves the former total-population polynomial factor to the true shared-inventory size and holds on every difference face. It is an acquired physical operation, not a supplied fiber transport law.

It does NOT allow one to replace an actual exit distribution by mu. Raw source hazards and signed packet end states must still be included when using (H4). In particular a source-weighted boundary mass can carry large factors from a large unpaired inventory. The global common receiving drift remains to be proved.

## 5. Raw-policy form beyond this grammar

The proof uses a finite regeneration mode, positive killing away from it, and an explicit raw forward/adjoint word that exposes killing with probability inverse-linear in a conserved minority inventory. The direction of the word is selected by which source factor is small. Any finite raw normal policy with those proved properties inherits the same physical renewal bound. This is a finite operation criterion; arbitrary weak reversibility has not been shown to supply the policy or its minority invariant.
