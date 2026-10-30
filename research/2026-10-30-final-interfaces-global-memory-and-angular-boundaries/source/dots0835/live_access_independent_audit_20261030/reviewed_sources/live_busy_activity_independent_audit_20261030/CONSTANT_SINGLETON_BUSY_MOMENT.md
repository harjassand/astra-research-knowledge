# Stronger constant-singleton BUSY moment
2026-10-30. Independent direct derivation by `challenge_live_busy_energy`, checked against the actual full-Hilbert block inputs. This is a separate strengthening of `DIRECT_FULL_HILBERT_BUSY_MOMENT.md`, not a substitution of A=epsilon^{-2} into a theorem whose constants depend on A.

## Statement
On the SAME accepted unified native generator, retain the original full-Hilbert positive finite-support witnesses

    x_-P_h<=X_h<=x_+P_h,
    L0*X_h<=-P_h,
    [X_h,P_j]=0 for all j.

The full native physical generator is L0+epsilon V, with only the first acquisition Hamiltonian weak, the later acquisition amplitude already fixed at zeta, and all new acquisition aborts/actual monitors retained. Take ALL owners as anchors. No pair gates, history guards, history potential or proof CP maps are required.

For a fixed sufficiently small delta>0, choose the same bounded-depth gate coloring and put

    Y=ordered product_h exp(delta X_h),   G=Y†Y.

Then there are fixed a,C>0, independent of N, runtime and sufficiently small delta,epsilon, such that the EXACT physical drift satisfies

    L_native*G <=[-a delta M1+C delta epsilon^2 N]G,
    M1=sum_h P_h.                                  (1)

The proof below supplies the uniform-delta assertion directly. Pair gates and the epsilon^2 singleton prefactor in the DATA-memory synthesis were needed to match its much smaller useful DATA service, not to control BUSY density alone.

## 1. Exact maskwise barrier and upper exponent
Every factor commutes every P_h. On a fixed joint P mask, the minimum singular values multiply and the maximum singular values multiply. Thus

    2 x_- delta M1 <= logG <= 2 x_+ delta M1.        (2)

In particular G>=exp(k delta M1), k=2x_->0. This remains true for noncommuting X_h and arbitrary DATA dependence on malformed histories. All-ready input has G=I exactly.

## 2. Fast part: remainder stays inside BUSY corners
Let C_Y(O)=Y†OY and write

    C_Y^{-1} L0* C_Y(I)
       = 2delta sum_h L0*X_h+R_delta.               (3)

This is an exact local analytic expansion. Disjoint gates cancel through a local generator term. The fixed number of color layers leaves a bounded local cone with a bounded number of gates and uniformly bounded local inverse norms. Hence each local second-order remainder has norm O(delta^2), uniformly in N; no extensive condition number is used.

The stronger corner statement is essential. For each joint active corner Q=product_{h in S}P_h, the actual L0* maps arbitrary operators supported in Q back into Q. This follows from the accepted resolved-reset/block proof; alternatively its positive semigroup is noncreating for each P_h, so T_t*(Q)<=Q, and domination/linearity give preservation of the full Q-corner algebra. Actual local Hamiltonian/complete-reset terms have the same property.

Expand the finite local similarity in multiplication superoperators M_X(O)=XO+OX. Every nonzero word on I contains exactly one L0* and at least one multiplication by an X_h. A word with L0* acting on I vanishes by unitality. In every other word, all X's before the generator restrict its argument to their joint active corner; L0* preserves that corner; all later X's further restrict it. Thus a word involving anchor h is supported in P_h, and a word involving several anchors is supported in their intersection. Every nonlinear remainder has at least two X factors, but importantly it still has at least one BUSY corner.

Grouping boundedly many connected words in each finite cone, or bounding its analytic remainder on each finite joint-mask block, therefore gives

    +/- R_delta <= C_F delta^2 sum_h P_h.           (4)

Bounded incidence of gate cones is what permits this sum; there is no N times M1 or M1^2 factor. The full block-algebra property ensures the local block bounds are operator inequalities, not estimates only on classical states.

Use sum L0*X_h<=-M1 in (3). Choose delta small enough that C_F delta<=1/2. Then

    C_Y^{-1} L0* C_Y(I) <= -(3/2)delta M1.          (5)

The numerical 3/2 is inessential; it merely reserves a fixed margin.

## 3. Weak part: an exact zero idle-idle block
Write the first-edge Hamiltonian as epsilon sum_h H_h with fixed bounded coefficients. In actual forest coordinates its only clock transitions are A0<->A1. For Q_h=I-P_h (true Ready),

    Q_h H_h Q_h=0,
    [H_h,P_j]=0 for j!=h.                          (6)

The first statement holds even on malformed sectors: an idle-idle matrix element cannot connect to A1, which is always BUSY. Both endpoints of some other first-edge blocks may be BUSY; they are allowed. The first-edge gauge is identity and no DATA factor changes this clock statement.

Define the exact transformed contribution

    K_h=C_Y^{-1}(i[H_h,C_Y(I)])
       =i(Htilde_h†-Htilde_h),
    Htilde_h=Y H_h Y^{-1}.                         (7)

The finite-depth local cancellation and K_h=0 at delta=0 imply

    ||K_h||<=C_W delta,

with bounded support and a uniform constant. Since Y commutes P_h, equation (6) gives the EXACT identity

    Q_h K_h Q_h=0.                                 (8)

Also [K_h,P_j]=0 for every j!=h. There is no uncontrolled weak ready-diagonal term.

Resolve K_h into its P_h diagonal and its P_h/Q_h cross block. The diagonal costs at most C_W epsilon delta P_h. For any fixed theta>0, block Young gives

    epsilon(P_hK_hQ_h+Q_hK_hP_h)
       <=theta delta P_h
          +(C_W^2/theta)delta epsilon^2 Q_h.        (9)

Choose theta=1/4 and then epsilon small enough that C_W epsilon<=1/4. Summing h, using |H|<=nu_H N, yields

    epsilon sum_h K_h
       <=(1/2)delta M1+C delta epsilon^2 N I.      (10)

Combining (5) and (10) gives the transformed version of (1) with a=1; taking a smaller fixed a covers different harmless reservations. Congruence back is legitimate and exact because M1 commutes Y. No inverse of a nonpositive proof map is involved: C_Y and its inverse are both CP congruences, generally nonunital.

## 4. Entropy contraction, actual noise and tail
Equation (2) and (1) imply, with lambda=a/(2x_+)>0,

    L_native*G<=-lambda GlogG+C delta epsilon^2 N G.

The SAME direct nonunital finite-cone cb-noise calculation as in the governing pair/singleton corollary gives

    N_u*G<=C_noise eta N G.

It includes retained common bath/reference and bounded-body, incident-cb-norm physical perturbations, after the fixed-depth forest-frame support enlargement. Assume the actual normal CPTP dynamics exists. Bath-only terms annihilate the system observable.

Let rho=C delta epsilon^2+C_noise eta. For full normalized evolution, spectral Jensen yields

    d log Tr(rho_u G)/du <=-lambda log Tr(rho_u G)+rho N.

All-ready initialization gives x(0)=1, so uniformly at every u>=0,

    Pr(M1>=beta N)
       <=exp{-[k delta beta-rho/lambda]N}.          (11)

Choose the SAME actual epsilon small enough for the accepted memory theorem and C epsilon^2<=lambda k beta/4. Choose the permitted noise threshold below both the memory threshold and C_noise eta<=lambda k delta beta/4. Then

    Pr(M1>=beta N)<=exp[-(k/2)delta beta N]          (12)

for every elapsed time. Delta is a mathematical fixed-small parameter; no physical rate changes when it is chosen. This yields a fixed positive exponent with source/barrier ratio O(epsilon^2)+O(eta/delta), rather than the weaker inherited pair/singleton ratio O(epsilon^2)+O(eta/(delta A epsilon^2)). The one physical apparatus is selected once to meet the simultaneous inequalities.

## 5. Scope and proof status
This is a direct, fully written strengthening using accepted original full-Hilbert witness and actual block/first-edge properties. It does not claim to be literally the epsilon-scaled singleton specialization with uniform constants after A=epsilon^{-2}; that shortcut would be unjustified. Every relevant estimate above was rederived at constant singleton strength.

It remains only a BUSY-density theorem. The separate canonical DATA-memory and forest-prefix support arguments are still required to infer live bare-DATA correctability. It does not assert that all controllers are idle, control infinite-time hitting probability, implement a physical handoff/decoder, or replace noisy preparation/readout contracts. The retained pair/singleton governing corollary is already sufficient and remains available without this strengthening.
