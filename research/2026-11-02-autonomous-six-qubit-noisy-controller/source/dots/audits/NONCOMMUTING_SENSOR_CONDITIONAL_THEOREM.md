# Noncommuting sensor potentials: independent conditional theorem

2026-11-01. Reviewed the root's proposal, the prior exact local-expansion proof, `POISSON_SENSOR_ADMISSION.md`, and `ROOT_OVERLAPPING_PAULI_PROBE_ALGEBRA.md`.

**Finding:** noncommutation among different local sensor potentials is NOT an obstruction to the exact exponential expansion. The unresolved gate is an actual all-apparatus operator drift with a sufficiently small extensive floor, plus initialization and protected-factor admission. The legal-sector sensor identity alone does not establish the resulting memory theorem.

## 1. Exact conditional theorem

Let W be the protected base potential and P the admitted component below W<beta n. Let V be a Hermitian sum of bounded-support, bounded-incidence local terms, with term norms and counts bounded independently of n. Require, on P,

    [P,V]=0, [V,W]=0, V>=W>=0.

Suppose the ACTUAL full generator, including all physical apparatus and its noise, obeys the OPERATOR inequality

    P L*V P <=-c V_P+b n P,   c>0, b>=0.

This must hold for every state supported in P, including illegal clock patterns, corrupted flags, overlapping probes and arbitrary coherences—not only legal trajectories or classical mixtures. A proof outside P is unnecessary, but the local operators defining V and L must be defined on the full physical Hilbert space.

The previously independently proved local expansion needs NO pairwise commutation of the summands of V. With support <=s, incidence <=zeta, term norm <=v_*, and generator-term support <=r, choose

    C=2 zeta v_*(r+s),  a<=1/(2C),
    C2=C^2(H0+2R0),

where sum||h||<=H0 n and sum||l||^2<=R0 n for the ACTUAL generator terms. Then

    e^-aV/2 L*(e^aV)e^-aV/2 =a L*V+R_a,
    ||R_a||<=C2 a^2 n.

The proof counts nested local commutators: ||ad_V^k(O)||<=||O||C^k k!, with a uniform convergence radius. Neither mutually commuting r_p nor a classical state is used.

Set

    f(a)=b/c+(C2/c)a.

Choose theta satisfying f(a)<theta<beta, and an initial state supported in P with

    Tr(e^aV rho0)<=C0 exp(a theta0 n),  theta0<=theta.

By exact killed-subchannel compression and spectral splitting in V, its moment obeys

    L_kill*(e^aV_P)<=-k n e^aV_P+D n exp(a theta n)P,
    k=ac(theta-f(a)),  D=ac theta.

Consequently

    Tr(e^aV_P tau_t)
      <=[C0+theta/(theta-f(a))] exp(a theta n).

Since V and W commute and V>=W, e^aV>=e^aW by their JOINT spectral calculus. Thus, for a verified two-step W-shell S2=P 1_(W>=beta n-2b_W),

    Tr(S2 tau_t)<=[C0+theta/(theta-f(a))]
                     exp[-a((beta-theta)n-2b_W)].

Combine this with the received killed-channel comparison and full H/J/J†J protected factorization to get logical output error at most

    2n(2h_all+3Gamma_all)T
      sqrt(C0+theta/(theta-f(a)))
      exp(a b_W) exp[-a(beta-theta)n/2].

All ideal sensor/progress/reset terms as well as external noise are counted in h_all/Gamma_all. Initial truncation or readout errors are added separately. The same bath/reference qualifications as in the killed-subchannel receipt apply.

A clean sufficient asymptotic margin is

    max(b/c, actual initial exponential-moment density)<beta.

Choose a small fixed a so the C2a/c correction fits that margin. If an additional weighted noise bound nu(a)n is kept separate from the mean inequality, replace f(a) by [ab+C2a^2+nu(a)]/(ac).

## 2. What the upper comparison V<=c_W W+C_s n does—and does not—cost

For arbitrary P-supported apparatus initialization on W=0, commutation and this upper bound give the conservative initial density theta0=C_s. Then a sufficient criterion is max(b/c,C_s)<beta, with strict margins. A large C_s need not be fatal if the ACTUAL prepared exponential moment is much smaller; that smaller moment must be proved, not inferred from a small mean or an unjustified product formula for overlapping noncommuting sensors.

Using a V-threshold in Foster avoids unnecessarily carrying c_W into the boundary exponent. If the only available mean inequality is instead L*V<=-c W+b n, conversion through V<=c_W W+C_s n produces floor ratio C_s+c_W b/c. That larger floor must fit below beta. The two situations must not be conflated.

A floor matters even for commuting purely classical dynamics: n independent birth/death bits with birth rate p and death rate 1-p have W=sum bits and L*W=p n-W. If p>beta, the stationary probability of W>=beta n tends to one, despite exact extensive mean restoring drift and bounded local terms. Thus finite b, without b/c<beta, cannot imply the desired barrier tail.

## 3. Sensor commutation check and caveats

For the displayed probe defect X_p P_p(x) and dressed check

    Sbar_s=S_s product_q Z_q^[omega(P_q(x),S_s)],

the sign from P_p versus S_s cancels the sign from X_p versus its Z_p dressing. Hence r_p commutes with every Sbar_s. Its clock/active/bad masks and Poisson coefficients are diagonal in separate classical records. It also commutes with independent witness/actuation-flag/cache Z variables. Therefore the displayed sensor terms commute with a base W built from these dressed checks and virtual witnesses, even when r_p and r_q do not commute with one another.

This does NOT automatically cover altered constructions. A Boolean constraint using an UNDRESSED actual check S_s can fail to commute with r_p. A wire sharing a probe's incompatible quantum observable, or an undressed off-diagonal clock penalty, can also break the claim. Ordinary Boolean constraints using cache bits and separate classical roots are safe. Any off-diagonal progress penalty needs an explicit transport/commutation proof.

Moreover [V,W]=0 alone does not imply [P,V]=0 if P selects one component in a degenerate W sector. Exact counterexample: W=0 on a two-dimensional space, P=|0><0|, V=[[1,1],[1,1]]>=0. The required component commutation fails. Preserving ALL underlying component labels, not just their scalar energy, is a sufficient condition. The displayed r_p preserves the dressed check/witness labels when defined on all clock configurations as claimed.

Without [V,W]=0, the lower inequality V>=W does not generally imply e^aV>=e^aW: exponential is not operator monotone. A different proved shell domination would then be required.

## 4. What remains unearned for the actual source

The supplied Poisson identity is

    L(t e_p+xi r_p)=-e_p+b_p I

on the collision-safe LEGAL clock sector. It does not automatically give a negative multiple of t e_p+xi r_p. Bounding the uncontrolled xi r_p by its extensive maximum can add a floor large enough to destroy the criterion above. One possible legal-sector modification is xi=-K_D^-1(g+lambda0), lambda0>0, which would add -lambda0 r_p if the stated reward identities remain valid; this has not been received as a full physical-source derivation here.

Most importantly, the document explicitly leaves R_illegal from unmarked overlaps, malformed clocks, premature resets and corrupted active/bad flags unbounded by a negative apparatus drift. The noncommuting exponential theorem does NOT pay those terms. They must be dominated as an actual operator inequality with an explicitly acceptable b/c on all P-supported physical states. Classical legal-chain minorization or a good-sector scalar calculation is not a substitute.

Finally require actual finite-bandwidth shell identities and protected flatness for PHP, PJP AND PJ†JP. Progress dressing/non-Clifford apparatus does not inherit them from spatial locality alone. The old killed-channel counterexample shows why J†J cannot be omitted.

## Conclusion

The suggested noncommuting exponential extension is valid and removes that particular mathematical objection. The displayed sensor source has not yet earned the complete mean/floor/illegal-sector/protected-interface hypotheses. This receipt supplies a precise conditional consumer, not an accepted global native-sensor or memory implementation theorem.
