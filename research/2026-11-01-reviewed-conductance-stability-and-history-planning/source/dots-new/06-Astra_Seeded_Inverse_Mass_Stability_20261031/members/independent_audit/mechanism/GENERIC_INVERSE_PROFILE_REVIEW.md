# Mechanism check: generic common-seed inverse linear profile

No compiler/source freeze is accepted by this note. The finite profile test is sufficient; unrestricted rational-profile enumeration is not a general seeded-network termination theorem.

## Exact reduction

Every internal source and target contains A; removing one common A leaves a conservative unary or binary reaction in coordinates `(r,B)`, where `r=A-1`. On A>=1, the actual propensity is exactly A times the stripped falling-factorial propensity.

For a tested rational profile `0<=w_j<=1`, set `R=A+w dot B`. Let L be the largest absolute R increment of any raw internal channel and `ell=1+L`. Every internal move has both R,R' at least one, hence `R/ell<=R'<=ell R`. For `h=1+c/R`,

    h'-h=-c delta/[R R']
           <=-c rho(delta)/R^2,
    rho(delta)=delta/ell if delta>=0, and ell*delta otherwise.

Thus `L_internal h<=-c A Psi_w/R^2`, where Psi is the exact stripped-generator polynomial with effective channel increments rho. These are rational finite computations, even though the effective coefficients are not globally linear in w.

Aggregate rho coefficients by stripped source. Require each pure source `2B_j` to have coefficient `u_j>0` and every mixed satellite binary coefficient to be nonnegative. Let K1 be the maximum of zero and the negative unary coefficients, and K2 the analogous maximum over r-containing binary coefficients. At integer states,

    Psi >= sum_j u_j(B_j)_2-K1(r+b)-K2[(r)_2+r b].

Since r=A-1, A>=1 and `b=sum B_j`, this implies

    Psi>=sum_j u_j B_j^2-K0 A^2-A sum_j(u_j+K0)B_j,
    K0=K1+K2.

Completing squares proves

    Psi>=Q/2-Ktilde A^2,
    Q=sum_j u_j B_j^2,
    Ktilde=K0+sum_j (u_j+K0)^2/(2u_j).

Consequently, with `c=min(1,D/(4Ktilde))`, the core bounds from the inverse-mass note give

    LW/W<=C0-3D A/4-c A Q/[2(1+c)R^2]       on A>=1.

The A-zero patch gives quotient at most `-lambda/2` independently of satellite counts.

## Tail compatibility and acquired finite box

Set `S=sum_j w_j^2/u_j` and `A_cut=ceil[4(C0+zeta)/(3D)]`. If S positive, require

    c/[4(1+c)S]>=C0+zeta.

In the branch A<A_cut, Cauchy gives `w dot B<=sqrt(SQ)`. If `Q>=9 A_cut^2/S`, then `R<=(4/3)sqrt(SQ)` and `Q/R^2>=1/(2S)`. The negative term pays the entire constant plus zeta.

If S zero, then all w_j are zero, R=A, and it suffices that

    Q>=2(1+c)(C0+zeta) A_cut^2/c.

In either branch, exact integer cutoffs `B_j_cut=ceil_sqrt(threshold/u_j)` acquire a finite exception box without enumerating it. A finite factored Foster constant follows. All signs, first-layer behavior and the common-A propensity identity have been independently checked.

## Critical moment and completeness scope

An arbitrary accepted S-positive profile at one requested t certifies recurrence and the `t^N` invariant moment, not automatically every finite exponential moment. Its compatibility inequality need not remain true as `C0(t)` grows. A separate all-t acquisition theorem is required for the stronger conclusion.

For S zero, the same profile passes the structural coefficient conditions for every t and the separate Q cutoff always exists; that branch has all-exponent scope. The specific hard mediated family also has all-exponent scope because its eta-halving termination is proved for every requested t.

For the hard profile `(w_B,w_C)=(eta,0)`, ell is exactly two,

    u_B=beta2(1-2eta)/2>=beta2/4,
    u_C=beta3 eta/2,
    K1=0, K2<=2alpha, alpha=max(alpha1,alpha2).

For eta<=1/4 one may use

    Kbar=4alpha+2(beta2/2+2alpha)^2/beta2
                     +beta3/4+4alpha^2/beta3,
    Ktilde<=Kbar/eta.

Thus `c>=c0 eta`, with `c0=min(1,D/(4Kbar))`, and

    c/[4(1+c)S] = c u_B/[4(1+c)eta^2]
                     >=c0 beta2/(32eta),

which diverges. The all-t halving guarantee is earned here; it is not inherited by every generic accepted profile.

Finally, the opposing-ray common-seed network

    A+2B <-> A+B+C <-> A+2C,
    A+B+C <-> 2A+B

cannot pass this linear-profile test at any real weights: the two pure-source effective coefficients have the signs of `w_C-w_B` and `w_B-w_C`. This is only a profile-class obstruction and is not instability evidence.
